from python_project.models import UserUniversity

# Voir tous les liens
print("=== LIENS UTILISATEUR-UNIVERSITÉ ===")
liens = UserUniversity.objects.all()
for lien in liens:
    print(f"  • {lien.user_id} -> {lien.university.name}")

print(f"\nTotal: {liens.count()} liens")

# Vérifier pour un utilisateur spécifique
user = 'test123'
liens_user = UserUniversity.objects.filter(user_id=user)
print(f"\n=== LIENS POUR {user} ===")
for lien in liens_user:
    print(f"  • {lien.university.name}")

exit()