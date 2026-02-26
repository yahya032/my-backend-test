# create_user_links.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()

from python_project.models import University, UserUniversity

def create_user_university_links():
    """Crée des liens entre utilisateurs de test et universités"""
    
    print("🔗 CRÉATION DES LIENS UTILISATEUR-UNIVERSITÉ")
    print("="*50)
    
    # Utilisateurs de test
    test_users = ['test123', 'user456', 'firebase_user_123']
    
    # Récupérer toutes les universités
    universities = University.objects.all()
    
    if not universities:
        print("❌ Aucune université trouvée.")
        print("   Veuillez d'abord créer des universités:")
        print("   1. python manage.py shell")
        print("   2. from python_project.models import University")
        print("   3. University.objects.create(name='Université Test')")
        return
    
    print(f"\n📚 Universités trouvées: {universities.count()}")
    
    liens_crees = 0
    liens_existants = 0
    
    for uni in universities:
        print(f"\n📌 Université: {uni.name}")
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
    
    print("\n" + "="*50)
    print(f"📊 RÉSULTATS:")
    print(f"   • Nouveaux liens créés: {liens_crees}")
    print(f"   • Liens déjà existants: {liens_existants}")
    print(f"   • Total dans la base: {UserUniversity.objects.count()}")
    print("="*50)

if __name__ == "__main__":
    create_user_university_links()
    print("\n✅ Script terminé!")