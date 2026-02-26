# executer_commandes.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()

from python_project.models import University, Alert, UserUniversity

def executer():
    print("="*60)
    print("🚀 EXÉCUTION DES COMMANDES")
    print("="*60)
    
    # 1. Voir les universités
    print("\n1. 🏛️ UNIVERSITÉS EXISTANTES")
    universites = University.objects.all()
    for uni in universites:
        print(f"   • ID {uni.id}: {uni.name}")
    print(f"   Total: {universites.count()}")
    
    # 2. Voir les liens
    print("\n2. 🔗 LIENS UTILISATEUR-UNIVERSITÉ")
    liens = UserUniversity.objects.all()
    if liens:
        for lien in liens:
            print(f"   • {lien.user_id} -> {lien.university.name}")
    else:
        print("   Aucun lien trouvé")
    
    # 3. Créer une université de test
    print("\n3. 🆕 CRÉATION D'UNE UNIVERSITÉ TEST")
    uni = University.objects.create(name="Université Test Alerte")
    print(f"   ✅ Université créée: {uni.name}")
    
    # 4. Vérifier les alertes
    print("\n4. 📝 VÉRIFICATION DES ALERTES")
    for user in ['test123', 'user456', 'firebase_user_123']:
        count = Alert.objects.filter(user_id=user).count()
        print(f"   • {user}: {count} alertes")
        for alert in Alert.objects.filter(user_id=user).order_by('-created_at')[:3]:
            print(f"      - {alert.title}: {alert.message[:50]}...")

if __name__ == "__main__":
    executer()