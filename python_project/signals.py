# python_project/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import University, Speciality, Level, Semester, Matiere, Document, Alert, UserUniversity

# Liste des utilisateurs de test par défaut
DEFAULT_TEST_USERS = ['test123', 'user456', 'firebase_user_123']

def get_users_for_university(university_id):
    """
    Récupère les utilisateurs associés à une université
    """
    if not university_id:
        return DEFAULT_TEST_USERS
    
    try:
        users = UserUniversity.objects.filter(university_id=university_id)
        if users.exists():
            return list(set([user.user_id for user in users]))
    except:
        pass
    
    return list(set(DEFAULT_TEST_USERS))

@receiver(post_save, sender=University)
def alert_university_created(sender, instance, created, **kwargs):
    """Alerte quand une nouvelle université est créée"""
    if created:
        users_to_notify = get_users_for_university(instance.id)
        for user_id in users_to_notify:
            Alert.objects.create(
                user_id=user_id,
                title="🏛️ Nouvelle université",
                message=f"L'université '{instance.name}' a été ajoutée"
            )
        print(f"✅ Alerte université créée pour {len(users_to_notify)} utilisateurs")

@receiver(post_save, sender=Speciality)
def alert_speciality_created(sender, instance, created, **kwargs):
    """Alerte quand une nouvelle spécialité est créée"""
    if created:
        university_name = instance.university.name if instance.university else "Université"
        users_to_notify = get_users_for_university(instance.university_id)
        for user_id in users_to_notify:
            Alert.objects.create(
                user_id=user_id,
                title="🎓 Nouvelle spécialité",
                message=f"La spécialité '{instance.name}' a été ajoutée à {university_name}"
            )
        print(f"✅ Alerte spécialité créée pour {len(users_to_notify)} utilisateurs")

@receiver(post_save, sender=Level)
def alert_level_created(sender, instance, created, **kwargs):
    """Alerte quand un nouveau niveau est créé"""
    if created:
        users_to_notify = list(set(DEFAULT_TEST_USERS))
        for user_id in users_to_notify:
            Alert.objects.create(
                user_id=user_id,
                title="📊 Nouveau niveau",
                message=f"Le niveau '{instance.name}' a été ajouté"
            )
        print(f"✅ Alerte niveau créée pour {len(users_to_notify)} utilisateurs")

@receiver(post_save, sender=Semester)
def alert_semester_created(sender, instance, created, **kwargs):
    """Alerte quand un nouveau semestre est créé"""
    if created:
        level_name = instance.level.name if instance.level else "Niveau"
        users_to_notify = list(set(DEFAULT_TEST_USERS))
        for user_id in users_to_notify:
            Alert.objects.create(
                user_id=user_id,
                title="📅 Nouveau semestre",
                message=f"Le semestre '{instance.name}' a été ajouté pour le niveau {level_name}"
            )
        print(f"✅ Alerte semestre créée pour {len(users_to_notify)} utilisateurs")

@receiver(post_save, sender=Matiere)
def alert_matiere_created(sender, instance, created, **kwargs):
    """Alerte quand une nouvelle matière est créée"""
    if created:
        university_name = "Université"
        university_id = None
        
        # Accès via la chaîne de relations : Matiere → semester → level → speciality → university
        if (instance.semester and 
            instance.semester.level and 
            instance.semester.level.speciality):
            university_name = instance.semester.level.speciality.university.name
            university_id = instance.semester.level.speciality.university.id
        
        users_to_notify = get_users_for_university(university_id) if university_id else list(set(DEFAULT_TEST_USERS))
        
        message = f"La matière '{instance.name}' a été ajoutée"
        if university_name != "Université":
            message += f" à {university_name}"
        
        for user_id in users_to_notify:
            Alert.objects.create(
                user_id=user_id,
                title="📚 Nouvelle matière",
                message=message
            )
        print(f"✅ Alerte matière créée pour {len(users_to_notify)} utilisateurs")

@receiver(post_save, sender=Document)
def alert_document_created(sender, instance, created, **kwargs):
    """Alerte quand un nouveau document est créé"""
    if created:
        university_name = "Université"
        university_id = None
        matiere_name = ""
        
        if instance.matiere:
            matiere_name = instance.matiere.name
            # Accès via la chaîne de relations : Document → matiere → semester → level → speciality → university
            if (instance.matiere.semester and 
                instance.matiere.semester.level and 
                instance.matiere.semester.level.speciality):
                university_name = instance.matiere.semester.level.speciality.university.name
                university_id = instance.matiere.semester.level.speciality.university.id
        
        users_to_notify = get_users_for_university(university_id) if university_id else list(set(DEFAULT_TEST_USERS))
        
        message = f"Le document '{instance.title}' a été ajouté"
        if university_name != "Université":
            message += f" à {university_name}"
        if matiere_name:
            message += f" dans la matière {matiere_name}"
        
        for user_id in users_to_notify:
            Alert.objects.create(
                user_id=user_id,
                title="📄 Nouveau document",
                message=message
            )
        print(f"✅ Alerte document créée pour {len(users_to_notify)} utilisateurs")