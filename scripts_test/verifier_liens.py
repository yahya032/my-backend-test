# verifier_liens.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()

from python_project.models import University, UserUniversity, Alert

def verifier():
    print("="*60)
    print("🔍 VÉRIFICATION DES LIENS ET ALERTES")
    print("="*60)
    
    # 1. Voir les liens
    print("\n1. 🔗 LIENS UTILISATEUR-UNIVERSITÉ")
    liens = UserUniversity.objects.all()
    if liens:
        for lien in liens:
            print(f"   • {lien.user_id} -> {lien.university.name}")
        print(f"   Total: {liens.count()} liens")
    else:
        print("   ⚠️ Aucun lien trouvé - exécutez d'abord python create_liens.py")
    
    # 2. Voir les alertes par utilisateur
    print("\n2. 📝 ALERTES PAR UTILISATEUR")
    for user in ['test123', 'user456', 'firebase_user_123']:
        count = Alert.objects.filter(user_id=user).count()
        print(f"\n   {user}: {count} alertes")
        for alert in Alert.objects.filter(user_id=user).order_by('-created_at')[:3]:
            print(f"      • {alert.title}: {alert.message}")
    
    # 3. Test de création d'une spécialité
    print("\n3. 🧪 TEST DE CRÉATION D'UNE SPÉCIALITÉ")
    from python_project.models import Speciality
    uni = University.objects.first()
    if uni:
        spec = Speciality.objects.create(
            name="Informatique",
            university=uni
        )
        print(f"   ✅ Spécialité créée: {spec.name}")
        
        # Voir les nouvelles alertes
        print("\n   Nouvelles alertes générées:")
        for user in ['test123', 'user456']:
            nouvelles = Alert.objects.filter(
                user_id=user,
                title="🎓 Nouvelle spécialité"
            ).order_by('-created_at')[:1]
            for alert in nouvelles:
                print(f"      • {user}: {alert.message}")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    verifier()