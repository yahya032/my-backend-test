# create_liens.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()

from python_project.models import University, UserUniversity

def create_liens():
    print("="*60)
    print("🔗 CRÉATION DES LIENS UTILISATEUR-UNIVERSITÉ")
    print("="*60)
    
    # Utilisateurs de test
    test_users = ['test123', 'user456', 'firebase_user_123']
    
    # Récupérer toutes les universités
    universites = University.objects.all()
    print(f"\n📚 Universités trouvées: {universites.count()}")
    
    liens_crees = 0
    liens_existants = 0
    
    for uni in universites:
        print(f"\n📌 {uni.name}")
        for user_id in test_users:
            obj, created = UserUniversity.objects.get_or_create(
                user_id=user_id,
                university=uni
            )
            if created:
                print(f"  ✅ Lien créé: {user_id}")
                liens_crees += 1
            else:
                print(f"  ⏩ Lien existant: {user_id}")
                liens_existants += 1
    
    print("\n" + "="*60)
    print(f"📊 RÉSULTATS:")
    print(f"  • Nouveaux liens créés: {liens_crees}")
    print(f"  • Liens déjà existants: {liens_existants}")
    print(f"  • Total dans la base: {UserUniversity.objects.count()}")
    print("="*60)

if __name__ == "__main__":
    create_liens()