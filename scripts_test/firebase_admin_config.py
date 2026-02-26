import os
import json
import firebase_admin
from firebase_admin import credentials

# Charger la clé depuis la variable d'environnement
firebase_key_json = os.environ.get("FIREBASE_KEY_JSON")

if not firebase_key_json:
    raise ValueError("FIREBASE_KEY_JSON n'est pas défini sur Render")

try:
    # Convertir la chaîne JSON en dictionnaire Python
    cred_dict = json.loads(firebase_key_json)
except json.JSONDecodeError as e:
    raise ValueError(f"Erreur lors du décodage de FIREBASE_KEY_JSON: {e}")

# Initialiser Firebase avec le dict
cred = credentials.Certificate(cred_dict)
firebase_admin.initialize_app(cred)
