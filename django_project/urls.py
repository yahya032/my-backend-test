# django_project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin par défaut de Django
    path('django-admin/', admin.site.urls),
    
    # Inclusion des URLs de l'application avec le préfixe 'api/'
    path('api/', include('python_project.urls')),  # ← AJOUT du préfixe api/ ici
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)