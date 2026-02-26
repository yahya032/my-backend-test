# python_project/apps.py
from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)

class PythonProjectConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'python_project'

    def ready(self):
        """Méthode appelée au démarrage de l'application"""
        
        # 1. Charger les signaux
        try:
            import python_project.signals
            logger.info("✅ Signaux chargés avec succès")
        except Exception as e:
            logger.error(f"❌ Erreur chargement signaux: {e}")
        
        # 2. Initialiser Firebase
        try:
            from .firebase_config import init_firebase
            init_firebase()
        except ImportError as e:
            logger.error(f"❌ Module firebase_config non trouvé: {e}")
        except Exception as e:
            logger.warning(f"⚠️  Firebase non initialisé: {e}")