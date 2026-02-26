#!/usr/bin/env python
"""
Script interactif pour tester les notifications
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000"
API_URL = f"{BASE_URL}/api"

def print_menu():
    print("\n" + "="*40)
    print("TEST INTERACTIF DES NOTIFICATIONS")
    print("="*40)
    print("1. Voir les alertes d'un utilisateur")
    print("2. Créer une alerte (via admin)")
    print("3. Lister tous les utilisateurs de test")
    print("4. Voir les stats (via admin)")
    print("5. Tester l'API Firebase")
    print("6. Quitter")
    print("="*40)

def get_user_alerts():
    user_id = input("Entrez l'ID de l'utilisateur: ")
    response = requests.get(f"{API_URL}/alerts/", params={"user": user_id})
    
    if response.status_code == 200:
        alerts = response.json()
        print(f"\n🔔 Alertes pour {user_id}: {len(alerts)}")
        for alert in alerts:
            print(f"\n  ID: {alert['id']}")
            print(f"  Titre: {alert['title']}")
            print(f"  Message: {alert['message']}")
            print(f"  Date: {alert['created_at']}")
            print("-"*30)
    else:
        print(f"❌ Erreur: {response.json()}")

def list_test_users():
    users = [
        'test_user_1',
        'test_user_2', 
        'firebase_user_123',
        'firebase_user_456'
    ]
    print("\n📋 Utilisateurs de test disponibles:")
    for user in users:
        response = requests.get(f"{API_URL}/alerts/", params={"user": user})
        if response.status_code == 200:
            count = len(response.json())
            print(f"  • {user}: {count} alertes")

def test_firebase():
    print("\n🔥 Test des endpoints Firebase:")
    
    # Liste des utilisateurs
    response = requests.get(f"{API_URL}/firebase-users/")
    if response.status_code == 200:
        users = response.json()
        print(f"  Utilisateurs Firebase: {len(users)}")
        for user in users[:3]:  # Afficher les 3 premiers
            print(f"    - {user.get('email', 'N/A')} (UID: {user.get('uid', 'N/A')[:8]}...)")
    else:
        print(f"  Firebase non disponible: {response.status_code}")

def main():
    while True:
        print_menu()
        choice = input("Votre choix (1-6): ")
        
        if choice == '1':
            get_user_alerts()
        elif choice == '2':
            print("\n📝 Pour créer une alerte:")
            print("1. Allez sur http://127.0.0.1:8000/admin/")
            print("2. Connectez-vous")
            print("3. Cliquez sur 'Alerts' puis 'Add Alert'")
        elif choice == '3':
            list_test_users()
        elif choice == '4':
            print("\n📊 Dashboard admin: http://127.0.0.1:8000/admin/dashboard/")
        elif choice == '5':
            test_firebase()
        elif choice == '6':
            print("Au revoir!")
            break
        else:
            print("Choix invalide")

if __name__ == "__main__":
    main()