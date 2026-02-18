# django_project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin par défaut de Django
    path('django-admin/', admin.site.urls),
    
    # Inclusion de toutes les URLs de l'application
    path('', include('python_project.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)