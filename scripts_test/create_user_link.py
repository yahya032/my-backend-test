# create_user_university.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()

from python_project.models import University, UserUniversity

def create_user_university_links():
    # Récupérer les universités
    universities = University.objects.all()
    
    # Utilisateurs de test
    test_users = ['test123', 'user456', 'firebase_user_123']
    
    for uni in universities:
        for user_id in test_users:
            UserUniversity.objects.get_or_create(
                user_id=user_id,
                university=uni
            )
        print(f"✅ Liens créés pour {uni.name}")

if __name__ == "__main__":
    create_user_university_links()
    print("✅ Relations utilisateur-université créées")