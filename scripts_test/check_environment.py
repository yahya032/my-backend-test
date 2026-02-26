#!/usr/bin/env python
"""
Script de vérification de l'environnement
"""

import os
import sys
import django

def check_environment():
    print("\n🔍 VÉRIFICATION DE L'ENVIRONNEMENT")
    print("="*50)
    
    # Vérifier Python
    print(f"✅ Python: {sys.version}")
    
    # Vérifier Django
    print(f"✅ Django: {django.get_version()}")
    
    # Vérifier les variables d'environnement
    print("\n📋 Variables d'environnement:")
    env_vars = ['DATABASE_URL', 'SECRET_KEY', 'DEBUG', 'FIREBASE_KEY_JSON']
    for var in env_vars:
        value = os.getenv(var, 'Non défini')
        if var == 'FIREBASE_KEY_JSON' and value != 'Non défini':
            print(f"  • {var}: [DÉFINI - caché]")
        else:
            print(f"  • {var}: {value}")
    
    # Vérifier la base de données
    print("\n💾 Base de données:")
    print(f"  • DB par défaut: {os.getenv('DATABASE_URL', 'sqlite:///db.sqlite3')}")
    
    # Tenter de configurer Django
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
        django.setup()
        print("  ✅ Django configuré avec succès")
    except Exception as e:
        print(f"  ❌ Erreur Django: {e}")
    
    print("\n" + "="*50)

if __name__ == "__main__":
    check_environment()