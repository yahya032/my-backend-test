from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db.models import Q, Count, Prefetch
from django.utils import timezone
from .models import *
from .serializers import *
import logging

logger = logging.getLogger(__name__)


class UniversityViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet pour les universités (lecture seule)
    Endpoints : /api/universities/
    """
    queryset = University.objects.all().order_by('name')
    serializer_class = UniversitySerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']  # ✅ AJOUT de 'description'
    ordering_fields = ['name', 'created_at']
    
    @action(detail=True, methods=['get'], url_path='stats')
    def get_stats(self, request, pk=None):
        """Statistiques d'une université (spécialités, niveaux, documents)"""
        university = self.get_object()
        
        specialities_count = university.specialities.count()
        levels_count = Level.objects.filter(speciality__university=university).count()
        documents_count = Document.objects.filter(
            matiere__semester__level__speciality__university=university,
            is_published=True
        ).count()
        
        return Response({
            'university_id': university.id,
            'university_name': university.name,
            'specialities_count': specialities_count,
            'levels_count': levels_count,
            'documents_count': documents_count,
        })


class SpecialityViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet pour les spécialités
    Endpoints : /api/specialities/?university_id=1
    """
    serializer_class = SpecialitySerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'code', 'description']  # ✅ AJOUT de 'description'
    ordering_fields = ['name', 'created_at']
    
    def get_queryset(self):
        queryset = Speciality.objects.all().order_by('name')
        university_id = self.request.query_params.get('university_id')
        
        if university_id:
            queryset = queryset.filter(university_id=university_id)
            
        # Optimisation avec select_related
        queryset = queryset.select_related('university')
        
        return queryset
    
    @action(detail=True, methods=['get'], url_path='levels')
    def get_levels(self, request, pk=None):
        """Récupère tous les niveaux d'une spécialité"""
        speciality = self.get_object()
        levels = speciality.levels.all().order_by('order')
        serializer = LevelSerializer(levels, many=True, context={'request': request})
        return Response(serializer.data)


class LevelViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet pour les niveaux
    Endpoints : /api/levels/?speciality_id=1
    """
    serializer_class = LevelSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']  # ✅ AJOUT de 'description'
    ordering_fields = ['order', 'name']
    
    def get_queryset(self):
        queryset = Level.objects.all().order_by('order', 'name')
        speciality_id = self.request.query_params.get('speciality_id')
        
        if speciality_id:
            queryset = queryset.filter(speciality_id=speciality_id)
            
        # Optimisation
        queryset = queryset.select_related('speciality')
        
        return queryset
    
    @action(detail=True, methods=['get'], url_path='semesters')
    def get_semesters(self, request, pk=None):
        """Récupère tous les semestres d'un niveau"""
        level = self.get_object()
        semesters = level.semesters.all().order_by('order')
        serializer = SemesterSerializer(semesters, many=True, context={'request': request})
        return Response(serializer.data)


class SemesterViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet pour les semestres
    Endpoints : /api/semesters/?level_id=1
    """
    serializer_class = SemesterSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['order', 'name']
    
    def get_queryset(self):
        queryset = Semester.objects.all().order_by('order')
        level_id = self.request.query_params.get('level_id')
        
        if level_id:
            queryset = queryset.filter(level_id=level_id)
            
        # Optimisation
        queryset = queryset.select_related('level')
        
        return queryset
    
    @action(detail=True, methods=['get'], url_path='matieres')
    def get_matieres(self, request, pk=None):
        """Récupère toutes les matières d'un semestre"""
        semester = self.get_object()
        matieres = semester.matieres.all().order_by('name')
        serializer = MatiereSerializer(matieres, many=True, context={'request': request})
        return Response(serializer.data)


class MatiereViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet pour les matières
    Endpoints : /api/matieres/?semester_id=1&university_id=1
    """
    serializer_class = MatiereSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'credits', 'coefficient']
    
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
            
        # Optimisation
        queryset = queryset.select_related('semester__level__speciality__university')
        
        return queryset
    
    @action(detail=True, methods=['get'], url_path='documents')
    def get_documents(self, request, pk=None):
        """Récupère tous les documents d'une matière"""
        matiere = self.get_object()
        documents = matiere.documents.filter(is_published=True).order_by('-created_at')
        serializer = DocumentSerializer(documents, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'], url_path='stats')
    def get_stats(self, request, pk=None):
        """Statistiques d'une matière (nombre de documents, total downloads)"""
        matiere = self.get_object()
        
        documents_count = matiere.documents.filter(is_published=True).count()
        total_downloads = matiere.documents.aggregate(total=Count('download_count'))['total'] or 0
        
        return Response({
            'matiere_id': matiere.id,
            'matiere_name': matiere.name,
            'documents_count': documents_count,
            'total_downloads': total_downloads,
        })


class DocumentViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour les documents
    Endpoints : /api/documents/?matiere_id=1&university_id=1
    """
    serializer_class = DocumentSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'download_count', 'title']
    
    def get_queryset(self):
        queryset = Document.objects.filter(is_published=True).order_by('-created_at')
        
        # Filtres
        university_id = self.request.query_params.get('university_id')
        speciality_id = self.request.query_params.get('speciality_id')
        level_id = self.request.query_params.get('level_id')
        semester_id = self.request.query_params.get('semester_id')
        matiere_id = self.request.query_params.get('matiere_id')
        document_type = self.request.query_params.get('document_type')  # ✅ NOUVEAU : filtre par type (CM, TD, TP)
        file_type = self.request.query_params.get('file_type')  # ✅ NOUVEAU : filtre par type de fichier (pdf, ppt)
        
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
        if document_type:
            queryset = queryset.filter(document_type=document_type)  # ✅ NOUVEAU
        if file_type:
            queryset = queryset.filter(file_type=file_type)  # ✅ NOUVEAU
            
        # Optimisation
        queryset = queryset.select_related('matiere__semester__level__speciality__university')
        
        return queryset
    
    @action(detail=True, methods=['post'])
    def increment_download(self, request, pk=None):
        """Incrémente le compteur de téléchargements"""
        document = self.get_object()
        document.download_count += 1
        document.save()
        return Response({'download_count': document.download_count})


class AlertViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour les alertes
    Endpoints : /api/alerts/?user=firebase_user_id
    """
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
                    
        # Optimisation
        queryset = queryset.select_related('university', 'speciality', 'level')
        
        return queryset
    
    @action(detail=False, methods=['get'], url_path='stats')
    def get_stats(self, request):
        """Statistiques des alertes pour un utilisateur"""
        user_id = request.query_params.get('user')
        if not user_id:
            return Response({'error': 'user_id required'}, status=400)
            
        alerts = self.get_queryset()
        
        # Compter par type
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
    """
    ViewSet pour les documents favoris
    Endpoints : /api/favorites/?user_id=firebase_user_id
    """
    serializer_class = FavoriteDocumentSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = FavoriteDocument.objects.all().order_by('-created_at')
        user_id = self.request.query_params.get('user_id')
        
        if user_id:
            queryset = queryset.filter(user_id=user_id)
            
        # Optimisation
        queryset = queryset.select_related('document__matiere')
        
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
    
    @action(detail=False, methods=['get'], url_path='check')
    def check_favorite(self, request):
        """Vérifie si un document est en favori"""
        user_id = request.query_params.get('user_id')
        document_id = request.query_params.get('document_id')
        
        if not user_id or not document_id:
            return Response({'error': 'user_id and document_id required'}, status=400)
            
        exists = FavoriteDocument.objects.filter(
            user_id=user_id,
            document_id=document_id
        ).exists()
        
        return Response({'is_favorite': exists})


class UserProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour les profils utilisateur
    Endpoints : /api/profiles/?user_id=firebase_user_id
    """
    serializer_class = UserProfileSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = UserProfile.objects.all()
        user_id = self.request.query_params.get('user_id')
        
        if user_id:
            queryset = queryset.filter(user_id=user_id)
            
        # Optimisation
        queryset = queryset.select_related('university', 'speciality', 'level')
        
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
    
    @action(detail=True, methods=['get'], url_path='favorites')
    def get_favorites(self, request, pk=None):
        """Récupère les favoris d'un utilisateur"""
        profile = self.get_object()
        favorites = FavoriteDocument.objects.filter(user_id=profile.user_id).select_related('document')
        serializer = FavoriteDocumentSerializer(favorites, many=True, context={'request': request})
        return Response(serializer.data)