# python_project/firebase_config.py
import os
import json
import firebase_admin
from firebase_admin import credentials
import logging

logger = logging.getLogger(__name__)

def init_firebase():
    """Initialise Firebase Admin SDK de manière sécurisée"""
    
    # Éviter les initialisations multiples
    if firebase_admin._apps:
        logger.info("✅ Firebase déjà initialisé")
        return
    
    # Mode développement : utiliser le fichier local
    if os.getenv('DEBUG', 'False').lower() == 'true':
        try:
            if os.path.exists('serviceAccountKey.json'):
                cred = credentials.Certificate('serviceAccountKey.json')
                firebase_admin.initialize_app(cred)
                logger.info("✅ Firebase initialisé avec fichier local (développement)")
                return
            else:
                logger.warning("⚠️  Fichier serviceAccountKey.json non trouvé en mode dev")
        except Exception as e:
            logger.error(f"❌ Erreur chargement fichier local: {e}")
    
    # Mode production : utiliser la variable d'environnement
    firebase_key_json = os.environ.get('FIREBASE_KEY_JSON')
    if firebase_key_json:
        try:
            # Nettoyer la chaîne JSON (enlever les retours à la ligne si présents)
            firebase_key_json = firebase_key_json.strip()
            
            # Convertir la chaîne JSON en dictionnaire
            firebase_key_dict = json.loads(firebase_key_json)
            
            # Initialiser Firebase avec les credentials
            cred = credentials.Certificate(firebase_key_dict)
            firebase_admin.initialize_app(cred)
            logger.info("✅ Firebase initialisé avec variables d'environnement (production)")
            
        except json.JSONDecodeError as e:
            logger.error(f"❌ Erreur de parsing JSON: {e}")
            logger.error("Vérifiez que FIREBASE_KEY_JSON contient un JSON valide")
        except Exception as e:
            logger.error(f"❌ Erreur initialisation Firebase: {e}")
    else:
        logger.warning("⚠️  FIREBASE_KEY_JSON non défini - Firebase non initialisé")