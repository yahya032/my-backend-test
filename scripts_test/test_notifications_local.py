#!/usr/bin/env python
"""
Script de test complet pour les notifications (Alert)
À exécuter après avoir lancé le serveur: python manage.py runserver
"""

import os
import django
import requests
import json
import time
from datetime import datetime, timedelta

# Configuration
BASE_URL = "http://127.0.0.1:8000"
API_URL = f"{BASE_URL}/api"

def setup_django():
    """Configurer Django pour les opérations directes sur la DB"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
    django.setup()

def test_alerts_api():
    """Tester l'API des alertes"""
    print("\n" + "="*50)
    print("TEST DE L'API DES ALERTES")
    print("="*50)
    
    # Test 1: Sans paramètre user (doit échouer)
    print("\n1. Test sans paramètre user:")
    response = requests.get(f"{API_URL}/alerts/")
    print(f"   Status: {response.status_code}")
    print(f"   Réponse: {response.json()}")
    
    # Test 2: Avec utilisateur inexistant
    print("\n2. Test avec utilisateur inexistant:")
    response = requests.get(f"{API_URL}/alerts/", params={"user": "user_inexistant_123"})
    print(f"   Status: {response.status_code}")
    print(f"   Réponse: {response.json()}")
    
    # Test 3: Avec utilisateur valide (après création d'alertes)
    print("\n3. Test avec utilisateur 'test_user_1':")
    response = requests.get(f"{API_URL}/alerts/", params={"user": "test_user_1"})
    print(f"   Status: {response.status_code}")
    alerts = response.json()
    print(f"   Nombre d'alertes: {len(alerts)}")
    for alert in alerts:
        print(f"   - [{alert['id']}] {alert['title']}: {alert['message'][:50]}...")

def create_alerts_via_django():
    """Créer des alertes directement via Django ORM"""
    print("\n" + "="*50)
    print("CRÉATION D'ALERTES VIA DJANGO")
    print("="*50)
    
    from python_project.models import Alert
    
    # Supprimer les anciennes alertes de test
    Alert.objects.filter(user_id__startswith='test_user').delete()
    print("✅ Anciennes alertes de test supprimées")
    
    # Créer des alertes pour différents utilisateurs
    test_users = [
        'test_user_1',
        'test_user_2',
        'firebase_user_123',
        'firebase_user_456'
    ]
    
    messages = [
        "Nouveau document disponible dans votre cours",
        "Mise à jour du calendrier universitaire",
        "Rappel: examen la semaine prochaine",
        "Note de frais à soumettre avant vendredi",
        "Changement de salle pour le cours de mathématiques",
        "Les notes sont maintenant disponibles"
    ]
    
    for user_id in test_users:
        for i in range(3):  # 3 alertes par utilisateur
            alert = Alert.objects.create(
                user_id=user_id,
                title=f"Notification {i+1} pour {user_id}",
                message=f"{messages[i % len(messages)]} - Message #{i+1}",
                created_at=datetime.now() - timedelta(hours=i*2)  # Décalage dans le temps
            )
            print(f"✅ Alerte créée: {alert.title} pour {user_id}")
    
    # Compter le total
    total = Alert.objects.filter(user_id__startswith='test_user').count()
    print(f"\n✅ Total alertes créées: {total}")

def test_specific_users():
    """Tester des utilisateurs spécifiques"""
    print("\n" + "="*50)
    print("TEST UTILISATEURS SPÉCIFIQUES")
    print("="*50)
    
    users = ['test_user_1', 'test_user_2', 'firebase_user_123', 'utilisateur_inconnu']
    
    for user in users:
        response = requests.get(f"{API_URL}/alerts/", params={"user": user})
        print(f"\nUtilisateur: {user}")
        print(f"  Status: {response.status_code}")
        if response.status_code == 200:
            alerts = response.json()
            print(f"  Alertes: {len(alerts)}")
            for alert in alerts[:2]:  # Afficher max 2 alertes
                print(f"    • {alert['title']} ({alert['created_at'][:10]})")

def test_admin_interface():
    """Tester l'accès à l'interface admin"""
    print("\n" + "="*50)
    print("INTERFACE D'ADMINISTRATION")
    print("="*50)
    
    print("\nAccédez à ces URLs dans votre navigateur:")
    print(f"  • Admin classique: {BASE_URL}/admin/")
    print(f"  • Dashboard personnalisé: {BASE_URL}/admin/dashboard/")
    print("\nIdentifiants: celui que vous avez créé avec createsuperuser")

def test_firebase_users_api():
    """Tester l'API Firebase si configurée"""
    print("\n" + "="*50)
    print("API FIREBASE (si configurée)")
    print("="*50)
    
    # Tester la liste des utilisateurs Firebase
    try:
        response = requests.get(f"{API_URL}/firebase-users/")
        if response.status_code == 200:
            users = response.json()
            print(f"✅ Utilisateurs Firebase trouvés: {len(users)}")
        else:
            print(f"⚠️  Firebase non configuré ou erreur: {response.status_code}")
    except Exception as e:
        print(f"⚠️  Erreur lors de l'appel Firebase: {e}")

def main():
    """Fonction principale"""
    print("\n" + "🚀"*10)
    print("TEST DES NOTIFICATIONS - SUPNUM")
    print("🚀"*10)
    
    # Vérifier que le serveur est accessible
    try:
        requests.get(BASE_URL, timeout=2)
        print(f"✅ Serveur accessible sur {BASE_URL}")
    except requests.exceptions.ConnectionError:
        print(f"❌ Impossible de joindre le serveur sur {BASE_URL}")
        print("   Assurez-vous que le serveur est lancé: python manage.py runserver")
        return
    
    # Configurer Django pour les opérations DB
    setup_django()
    
    # Créer des alertes de test
    create_alerts_via_django()
    
    # Tester l'API
    test_alerts_api()
    
    # Tester utilisateurs spécifiques
    test_specific_users()
    
    # Tester les APIs Firebase
    test_firebase_users_api()
    
    # Informations sur l'admin
    test_admin_interface()
    
    print("\n" + "="*50)
    print("✅ TESTS TERMINÉS")
    print("="*50)

if __name__ == "__main__":
    main()