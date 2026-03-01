# django_project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from python_project.admin import admin_site  # ← IMPORT À AJOUTER

urlpatterns = [
    # path('admin/', admin.site.urls),  # ← À COMMENTER
    path('admin/', admin_site.urls),  # ← À DÉCOMMENTER
    path('api/', include('python_project.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)