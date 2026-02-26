# test_alerts.py
import os
import django
import requests
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()

from python_project.models import Alert, University, Speciality, Level, Semester, Matiere, Document

def test_alerts_for_user(user_id):
    """Teste les alertes pour un utilisateur spécifique"""
    
    print(f"\n{'='*50}")
    print(f"🔔 Alertes pour l'utilisateur: {user_id}")
    print(f"{'='*50}")
    
    try:
        response = requests.get(f"http://127.0.0.1:8000/api/alerts/?user={user_id}")
        
        if response.status_code == 200:
            alerts = response.json()
            print(f"Nombre d'alertes: {len(alerts)}")
            
            for alert in alerts:
                print(f"\n  📌 {alert['title']}")
                print(f"     {alert['message']}")
                print(f"     🕐 {alert['created_at']}")
        else:
            print(f"❌ Erreur: {response.status_code}")
            print(response.json())
            
    except requests.exceptions.ConnectionError:
        print("❌ Serveur non accessible. Lancez d'abord: python manage.py runserver")

def create_sample_data():
    """Crée des données d'exemple pour tester les alertes"""
    
    print("\n📝 Création de données d'exemple...")
    
    # Créer une université
    uni, created = University.objects.get_or_create(
        name="Université de Nouakchott"
    )
    if created:
        print(f"✅ Université créée: {uni.name}")
    
    # Créer un niveau
    level, created = Level.objects.get_or_create(name="L3")
    if created:
        print(f"✅ Niveau créé: {level.name}")
    
    # Créer une spécialité
    spec, created = Speciality.objects.get_or_create(
        university=uni,
        name="Informatique"
    )
    if created:
        print(f"✅ Spécialité créée: {spec.name}")
    
    # Créer un semestre
    sem, created = Semester.objects.get_or_create(
        level=level,
        name="S1"
    )
    if created:
        print(f"✅ Semestre créé: {sem.name}")
    
    # Créer une matière
    mat, created = Matiere.objects.get_or_create(
        name="Programmation Python",
        semester=sem,
        speciality=spec
    )
    if created:
        print(f"✅ Matière créée: {mat.name}")
    
    # Créer un document
    # Note: Pour vraiment tester, créez un document via l'admin

def main():
    print("\n🚀 TEST DU SYSTÈME D'ALERTES")
    print("="*50)
    
    # Créer des données de test
    create_sample_data()
    
    # Tester pour différents utilisateurs
    test_users = ['test123', 'user456', 'firebase_user_123']
    
    for user in test_users:
        test_alerts_for_user(user)
    
    print("\n" + "="*50)
    print("✅ Pour créer de nouvelles alertes:")
    print("1. Allez sur http://127.0.0.1:8000/admin/")
    print("2. Ajoutez une université, spécialité, niveau, etc.")
    print("3. Les alertes seront créées automatiquement")
    print("="*50)

if __name__ == "__main__":
    main()