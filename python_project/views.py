from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from django.http import FileResponse
from django.db.models import Q
import os

from .models import University, Speciality, Level, Semester, Matiere, Document, Alert
from .serializers import (
    UniversitySerializer, SpecialitySerializer, LevelSerializer,
    SemesterSerializer, MatiereSerializer, DocumentSerializer,
    FirebaseUserSerializer, FirebaseCreateUserSerializer, AlertSerializer
)
from firebase_admin import auth as firebase_auth


# ---------------- ALERT ----------------
@api_view(['GET'])
def user_alerts(request):
    user_id = request.query_params.get('user')
    if not user_id:
        return Response({"error": "user parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

    alerts = Alert.objects.filter(user_id=user_id).order_by('-created_at')
    serializer = AlertSerializer(alerts, many=True)
    return Response(serializer.data)


# ---------------- BASE VIEWSET ----------------
class BaseViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]

    def get_serializer_context(self):
        return {'request': self.request}


# ---------------- UNIVERSITY ----------------
class UniversityViewSet(BaseViewSet):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer

    @action(detail=True, methods=['get'], url_path='download-calendar')
    def download_calendar(self, request, pk=None):
        university = self.get_object()

        # Si le fichier calendar est défini
        if university.calendar and university.calendar.name:
            file_path = university.calendar.path
            if os.path.exists(file_path):
                return FileResponse(open(file_path, 'rb'), content_type='application/pdf')

        # fallback: chercher un document PDF nommé "calendrier"
        calendar_doc = Document.objects.filter(
            matiere__speciality__university=university,
            file__endswith='.pdf',
            title__icontains='calendrier'
        ).first()

        if calendar_doc and calendar_doc.file:
            return FileResponse(calendar_doc.file.open(), content_type='application/pdf')

        return Response({"error": "Calendrier non trouvé."}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'], url_path='calendar-url')
    def calendar_url(self, request, pk=None):
        university = self.get_object()
        if university.calendar and university.calendar.name:
            return Response({"url": request.build_absolute_uri(university.calendar.url)})
        return Response({"url": None, "error": "Calendrier non trouvé."}, status=status.HTTP_404_NOT_FOUND)


# ---------------- SPECIALITY ----------------
class SpecialityViewSet(BaseViewSet):
    queryset = Speciality.objects.all()
    serializer_class = SpecialitySerializer

    def get_queryset(self):
        qs = super().get_queryset()
        university_id = self.request.query_params.get('university_id')
        if university_id:
            qs = qs.filter(university_id=university_id)
        return qs.order_by('id')


# ---------------- LEVEL ----------------
class LevelViewSet(BaseViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer


# ---------------- SEMESTER ----------------
class SemesterViewSet(BaseViewSet):
    queryset = Semester.objects.all()
    serializer_class = SemesterSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        level_id = self.request.query_params.get('level_id')
        if level_id:
            qs = qs.filter(level_id=level_id)
        return qs.order_by('id')


# ---------------- MATIERE ----------------
class MatiereViewSet(BaseViewSet):
    queryset = Matiere.objects.all()
    serializer_class = MatiereSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        level_id = self.request.query_params.get('level_id')
        semester_id = self.request.query_params.get('semester_id')
        speciality_id = self.request.query_params.get('speciality_id')
        university_id = self.request.query_params.get('university_id')

        if level_id:
            qs = qs.filter(Q(semester__level_id=level_id) | Q(semester__level__isnull=True))
        if semester_id:
            qs = qs.filter(Q(semester_id=semester_id) | Q(semester__isnull=True))
        if speciality_id:
            qs = qs.filter(Q(speciality_id=speciality_id) | Q(speciality__isnull=True))
        if university_id:
            qs = qs.filter(Q(speciality__university_id=university_id) | Q(speciality__university__isnull=True))

        return qs.order_by('semester__level__id', 'semester__id', 'id')


# ---------------- DOCUMENT ----------------
class DocumentViewSet(BaseViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        level_id = self.request.query_params.get('level_id')
        semester_id = self.request.query_params.get('semester_id')
        speciality_id = self.request.query_params.get('speciality_id')
        university_id = self.request.query_params.get('university_id')
        matiere_id = self.request.query_params.get('matiere_id')

        if matiere_id:
            qs = qs.filter(matiere_id=matiere_id)
        if semester_id:
            qs = qs.filter(Q(matiere__semester_id=semester_id) | Q(matiere__semester__isnull=True))
        if level_id:
            qs = qs.filter(Q(matiere__semester__level_id=level_id) | Q(matiere__semester__level__isnull=True))
        if speciality_id:
            qs = qs.filter(Q(matiere__speciality_id=speciality_id) | Q(matiere__speciality__isnull=True))
        if university_id:
            qs = qs.filter(Q(matiere__speciality__university_id=university_id) | Q(matiere__speciality__university__isnull=True))

        return qs.order_by(
            'matiere__speciality__university__id',
            'matiere__speciality__id',
            'matiere__semester__level_id',
            'matiere__semester_id',
            'matiere_id',
            'id'
        )


# ================ FIREBASE FUNCTIONS ================

@api_view(['GET'])
def list_firebase_users(request):
    """
    Liste tous les utilisateurs Firebase (max 100 par défaut)
    """
    try:
        # Récupérer la liste des utilisateurs
        users = []
        page = firebase_auth.list_users()
        
        for user in page.iterate_all():
            users.append({
                'uid': user.uid,
                'email': user.email,
                'display_name': user.display_name,
                'disabled': user.disabled,
                'created_at': user.user_metadata.creation_timestamp if user.user_metadata else None
            })
        
        serializer = FirebaseUserSerializer(users, many=True)
        return Response(serializer.data)
        
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def create_firebase_user(request):
    """
    Crée un nouvel utilisateur Firebase
    """
    serializer = FirebaseCreateUserSerializer(data=request.data)
    
    if serializer.is_valid():
        try:
            # Créer l'utilisateur dans Firebase
            user = firebase_auth.create_user(
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password'],
                display_name=serializer.validated_data.get('display_name', ''),
                disabled=serializer.validated_data.get('disabled', False)
            )
            
            return Response({
                'uid': user.uid,
                'email': user.email,
                'display_name': user.display_name,
                'message': 'Utilisateur créé avec succès'
            }, status=status.HTTP_201_CREATED)
            
        except firebase_auth.EmailAlreadyExistsError:
            return Response(
                {"error": "Un utilisateur avec cet email existe déjà"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_firebase_user(request, uid):
    """
    Récupère les détails d'un utilisateur Firebase spécifique
    """
    try:
        user = firebase_auth.get_user(uid)
        
        return Response({
            'uid': user.uid,
            'email': user.email,
            'display_name': user.display_name,
            'disabled': user.disabled,
            'created_at': user.user_metadata.creation_timestamp if user.user_metadata else None,
            'last_sign_in': user.user_metadata.last_sign_in_timestamp if user.user_metadata else None
        })
        
    except firebase_auth.UserNotFoundError:
        return Response(
            {"error": "Utilisateur non trouvé"},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['DELETE'])
def delete_firebase_user(request, uid):
    """
    Supprime un utilisateur Firebase par son UID
    """
    try:
        firebase_auth.delete_user(uid)
        return Response(
            {"message": f"Utilisateur {uid} supprimé avec succès"},
            status=status.HTTP_200_OK
        )
    except firebase_auth.UserNotFoundError:
        return Response(
            {"error": "Utilisateur non trouvé"},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def disable_firebase_user(request, uid):
    """
    Désactive ou active un utilisateur Firebase
    """
    try:
        disabled = request.data.get('disabled', True)
        user = firebase_auth.update_user(uid, disabled=disabled)
        
        return Response({
            'uid': user.uid,
            'email': user.email,
            'disabled': user.disabled,
            'message': f"Utilisateur {'désactivé' if disabled else 'activé'} avec succès"
        })
        
    except firebase_auth.UserNotFoundError:
        return Response(
            {"error": "Utilisateur non trouvé"},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )