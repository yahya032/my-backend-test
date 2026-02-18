# python_project/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

from .admin import admin_site
from .views import (
    UniversityViewSet,
    SpecialityViewSet,
    LevelViewSet,
    SemesterViewSet,
    MatiereViewSet,
    DocumentViewSet,
    list_firebase_users,
    create_firebase_user,
    get_firebase_user,
    delete_firebase_user,
    disable_firebase_user,
    user_alerts,
)

# ================== ROUTER DRF ==================
router = DefaultRouter()
router.register(r'universities', UniversityViewSet, basename='university')
router.register(r'specialities', SpecialityViewSet, basename='speciality')
router.register(r'levels', LevelViewSet, basename='level')
router.register(r'semesters', SemesterViewSet, basename='semester')
router.register(r'matieres', MatiereViewSet, basename='matiere')
router.register(r'documents', DocumentViewSet, basename='document')

# ================== URLS ==================
urlpatterns = [
    # Admin personnalisé - accessible via /admin/ (pas /api/admin/)
    path('admin/', admin_site.urls),
    
    # API REST - accessible via /api/
    path('api/', include(router.urls)),
    
    # Firebase users - accessible via /api/
    path('api/firebase-users/', list_firebase_users, name='firebase-users'),
    path('api/firebase-create-user/', create_firebase_user, name='firebase-create-user'),
    path('api/firebase-user/<str:uid>/', get_firebase_user, name='firebase-user-detail'),
    path('api/firebase-user/<str:uid>/delete/', delete_firebase_user, name='firebase-user-delete'),
    path('api/firebase-user/<str:uid>/disable/', disable_firebase_user, name='firebase-user-disable'),
    
    # Alertes - accessible via /api/alerts/ (correction: alerts, pas alerte)
    path('api/alerts/', user_alerts, name='user-alerts'),
]

# Servir les fichiers médias en développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)