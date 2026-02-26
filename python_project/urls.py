# python_project/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'universities', views.UniversityViewSet, basename='university')
router.register(r'specialities', views.SpecialityViewSet, basename='speciality')
router.register(r'levels', views.LevelViewSet, basename='level')
router.register(r'semesters', views.SemesterViewSet, basename='semester')
router.register(r'matieres', views.MatiereViewSet, basename='matiere')
router.register(r'documents', views.DocumentViewSet, basename='document')
router.register(r'alerts', views.AlertViewSet, basename='alert')
router.register(r'favorites', views.FavoriteDocumentViewSet, basename='favorite')
router.register(r'profiles', views.UserProfileViewSet, basename='profile')

# Plus de préfixe 'api/' ici - les routes sont nues
urlpatterns = [
    path('', include(router.urls)),
]