# python_project/apps.py
from django.apps import AppConfig

class PythonProjectConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'python_project'

    def ready(self):
        import python_project.signals  # Important pour charger les signaux