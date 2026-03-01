# django_project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# IMPORTANT: Décommentez cette ligne si vous voulez utiliser l'admin personnalisé
# from python_project.admin import admin_site

urlpatterns = [
    # Utilisez soit l'admin par défaut (déjà fonctionnel)
    path('admin/', admin.site.urls),
    
    # OU décommentez ceci pour l'admin personnalisé avec dashboard
    # path('admin/', admin_site.urls),
    
    path('api/', include('python_project.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)