# views.py
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db.models import Q, Count
from django.utils import timezone
from .models import *
from .serializers import *
import logging

logger = logging.getLogger(__name__)


class UniversityViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet pour les universités (lecture seule)"""
    queryset = University.objects.all().order_by('name')
    serializer_class = UniversitySerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class SpecialityViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet pour les spécialités"""
    serializer_class = SpecialitySerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'code']
    
    def get_queryset(self):
        queryset = Speciality.objects.all().order_by('name')
        university_id = self.request.query_params.get('university_id')
        if university_id:
            queryset = queryset.filter(university_id=university_id)
        return queryset


class LevelViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet pour les niveaux"""
    serializer_class = LevelSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = Level.objects.all().order_by('order', 'name')
        speciality_id = self.request.query_params.get('speciality_id')
        if speciality_id:
            queryset = queryset.filter(speciality_id=speciality_id)
        return queryset


class SemesterViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet pour les semestres"""
    serializer_class = SemesterSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = Semester.objects.all().order_by('order')
        level_id = self.request.query_params.get('level_id')
        if level_id:
            queryset = queryset.filter(level_id=level_id)
        return queryset


class MatiereViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet pour les matières"""
    serializer_class = MatiereSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = Matiere.objects.all().order_by('name')
        
        # Filtres multiples
        university_id = self.request.query_params.get('university_id')
        semester_id = self.request.query_params.get('semester_id')
        speciality_id = self.request.query_params.get('speciality_id')
        level_id = self.request.query_params.get('level_id')
        
        if university_id:
            queryset = queryset.filter(semester__level__speciality__university_id=university_id)
        if semester_id:
            queryset = queryset.filter(semester_id=semester_id)
        if speciality_id:
            queryset = queryset.filter(semester__level__speciality_id=speciality_id)
        if level_id:
            queryset = queryset.filter(semester__level_id=level_id)
            
        return queryset


class DocumentViewSet(viewsets.ModelViewSet):
    """ViewSet pour les documents"""
    serializer_class = DocumentSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']
    
    def get_queryset(self):
        queryset = Document.objects.filter(is_published=True).order_by('-created_at')
        
        # Filtres
        university_id = self.request.query_params.get('university_id')
        speciality_id = self.request.query_params.get('speciality_id')
        level_id = self.request.query_params.get('level_id')
        semester_id = self.request.query_params.get('semester_id')
        matiere_id = self.request.query_params.get('matiere_id')
        
        if university_id:
            queryset = queryset.filter(
                matiere__semester__level__speciality__university_id=university_id
            )
        if speciality_id:
            queryset = queryset.filter(
                matiere__semester__level__speciality_id=speciality_id
            )
        if level_id:
            queryset = queryset.filter(matiere__semester__level_id=level_id)
        if semester_id:
            queryset = queryset.filter(matiere__semester_id=semester_id)
        if matiere_id:
            queryset = queryset.filter(matiere_id=matiere_id)
            
        return queryset
    
    @action(detail=True, methods=['post'])
    def increment_download(self, request, pk=None):
        """Incrémente le compteur de téléchargements"""
        document = self.get_object()
        document.download_count += 1
        document.save()
        return Response({'download_count': document.download_count})


class AlertViewSet(viewsets.ModelViewSet):
    """ViewSet pour les alertes"""
    serializer_class = AlertSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = Alert.objects.all().order_by('-created_at')
        user_id = self.request.query_params.get('user')
        
        if user_id:
            # Alertes globales OU pour cet utilisateur spécifique
            queryset = queryset.filter(
                Q(is_global=True) | Q(user_id=user_id)
            ).filter(
                Q(expires_at__isnull=True) | Q(expires_at__gte=timezone.now())
            )
            
            # Ajouter le statut de lecture
            for alert in queryset:
                try:
                    read_status = AlertReadStatus.objects.get(
                        alert=alert, user_id=user_id
                    )
                    alert.is_read = read_status.is_read
                except AlertReadStatus.DoesNotExist:
                    alert.is_read = False
                    
        return queryset
    
    @action(detail=False, methods=['get'], url_path='stats')
    def get_stats(self, request):
        """Récupère les statistiques des alertes pour un utilisateur"""
        user_id = request.query_params.get('user')
        if not user_id:
            return Response({'error': 'user_id required'}, status=400)
            
        alerts = self.get_queryset()
        
        # Compter par type (simulé via le titre)
        universities_count = alerts.filter(title__icontains='🏛️').count()
        specialities_count = alerts.filter(title__icontains='🎓').count()
        others_count = alerts.exclude(
            Q(title__icontains='🏛️') | Q(title__icontains='🎓')
        ).count()
        
        # Compter les lus/non lus
        read_count = sum(1 for a in alerts if getattr(a, 'is_read', False))
        unread_count = alerts.count() - read_count
        
        return Response({
            'total': alerts.count(),
            'read': read_count,
            'unread': unread_count,
            'universities': universities_count,
            'specialities': specialities_count,
            'others': others_count,
        })
    
    @action(detail=True, methods=['patch'])
    def mark_as_read(self, request, pk=None):
        """Marque une alerte comme lue"""
        alert = self.get_object()
        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response({'error': 'user_id required'}, status=400)
            
        read_status, created = AlertReadStatus.objects.get_or_create(
            alert=alert,
            user_id=user_id,
            defaults={'is_read': True, 'read_at': timezone.now()}
        )
        
        if not created and not read_status.is_read:
            read_status.is_read = True
            read_status.read_at = timezone.now()
            read_status.save()
            
        return Response({'status': 'marked as read'})


class FavoriteDocumentViewSet(viewsets.ModelViewSet):
    """ViewSet pour les documents favoris"""
    serializer_class = FavoriteDocumentSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = FavoriteDocument.objects.all().order_by('-created_at')
        user_id = self.request.query_params.get('user_id')
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        return queryset
    
    @action(detail=False, methods=['delete'], url_path='remove')
    def remove_favorite(self, request):
        """Supprime un favori"""
        user_id = request.query_params.get('user_id')
        document_id = request.query_params.get('document_id')
        
        if not user_id or not document_id:
            return Response({'error': 'user_id and document_id required'}, status=400)
            
        deleted = FavoriteDocument.objects.filter(
            user_id=user_id,
            document_id=document_id
        ).delete()
        
        return Response({'deleted': deleted[0] > 0})


class UserProfileViewSet(viewsets.ModelViewSet):
    """ViewSet pour les profils utilisateur"""
    serializer_class = UserProfileSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = UserProfile.objects.all()
        user_id = self.request.query_params.get('user_id')
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        return queryset
    
    @action(detail=False, methods=['get'], url_path='by-firebase-id')
    def get_by_firebase_id(self, request):
        """Récupère un profil par Firebase ID"""
        user_id = request.query_params.get('firebase_id')
        if not user_id:
            return Response({'error': 'firebase_id required'}, status=400)
            
        try:
            profile = UserProfile.objects.get(user_id=user_id)
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=404)
    
    @action(detail=False, methods=['post'], url_path='create-or-update')
    def create_or_update(self, request):
        """Crée ou met à jour un profil"""
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'error': 'user_id required'}, status=400)
            
        profile, created = UserProfile.objects.update_or_create(
            user_id=user_id,
            defaults=request.data
        )
        
        serializer = self.get_serializer(profile)
        return Response(serializer.data, status=201 if created else 200)