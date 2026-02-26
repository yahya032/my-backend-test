import os
import django

# Configuration de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()

from python_project.models import Speciality, Level, Semester

def setup_academic_structure():
    """Crée tous les niveaux et semestres pour toutes les spécialités"""
    
    print("🚀 CRÉATION DE LA STRUCTURE ACADÉMIQUE")
    print("=" * 60)
    
    # Configuration des niveaux avec leurs semestres
    niveaux_config = [
        {
            'name': 'L1',
            'description': 'Licence 1 - Premier cycle',
            'order': 1,
            'semestres': [
                {'name': 'Semestre 1', 'code': 'S1', 'order': 1},
                {'name': 'Semestre 2', 'code': 'S2', 'order': 2},
            ]
        },
        {
            'name': 'L2',
            'description': 'Licence 2 - Deuxième année',
            'order': 2,
            'semestres': [
                {'name': 'Semestre 3', 'code': 'S3', 'order': 3},
                {'name': 'Semestre 4', 'code': 'S4', 'order': 4},
            ]
        },
        {
            'name': 'L3',
            'description': 'Licence 3 - Troisième année',
            'order': 3,
            'semestres': [
                {'name': 'Semestre 5', 'code': 'S5', 'order': 5},
                {'name': 'Semestre 6', 'code': 'S6', 'order': 6},
            ]
        },
        {
            'name': 'M1',
            'description': 'Master 1 - Première année',
            'order': 4,
            'semestres': [
                {'name': 'Semestre 1', 'code': 'S1', 'order': 1},
                {'name': 'Semestre 2', 'code': 'S2', 'order': 2},
            ]
        },
        {
            'name': 'M2',
            'description': 'Master 2 - Deuxième année',
            'order': 5,
            'semestres': [
                {'name': 'Semestre 3', 'code': 'S3', 'order': 3},
                {'name': 'Semestre 4', 'code': 'S4', 'order': 4},
            ]
        },
    ]
    
    total_niveaux = 0
    total_semestres = 0
    
    # Récupérer toutes les spécialités
    specialites = Speciality.objects.all()
    print(f"📚 {specialites.count()} spécialités trouvées\n")
    
    if not specialites:
        print("❌ Aucune spécialité trouvée. Veuillez d'abord créer des spécialités.")
        return
    
    for specialite in specialites:
        print(f"\n🏫 Spécialité: {specialite.name}")
        print("-" * 40)
        
        for niveau_config in niveaux_config:
            # Créer ou récupérer le niveau
            niveau, created = Level.objects.get_or_create(
                speciality=specialite,
                name=niveau_config['name'],
                defaults={
                    'description': f"{niveau_config['description']} - {specialite.name}",
                    'order': niveau_config['order']
                }
            )
            
            if created:
                total_niveaux += 1
                print(f"  ✅ Niveau créé: {niveau.name}")
            else:
                print(f"  ⚠️ Niveau existant: {niveau.name}")
            
            # Créer les semestres pour ce niveau
            for semestre_config in niveau_config['semestres']:
                semestre, created = Semester.objects.get_or_create(
                    level=niveau,
                    code=semestre_config['code'],
                    defaults={
                        'name': semestre_config['name'],
                        'order': semestre_config['order']
                    }
                )
                
                if created:
                    total_semestres += 1
                    print(f"    ✅ Semestre créé: {semestre.name} ({semestre.code})")
    
    # Statistiques finales
    print("\n" + "=" * 60)
    print("📊 STATISTIQUES FINALES")
    print("=" * 60)
    print(f"🏫 Spécialités: {Speciality.objects.count()}")
    print(f"📚 Niveaux: {Level.objects.count()} (dont {total_niveaux} nouveaux)")
    print(f"📅 Semestres: {Semester.objects.count()} (dont {total_semestres} nouveaux)")
    
    # Vérification
    print("\n🔍 VÉRIFICATION")
    print("=" * 60)
    for specialite in specialites[:3]:  # Afficher pour les 3 premières spécialités
        print(f"\n{specialite.name}:")
        niveaux = Level.objects.filter(speciality=specialite).order_by('order')
        for niveau in niveaux:
            semestres = Semester.objects.filter(level=niveau).order_by('order')
            print(f"  {niveau.name}: {semestres.count()} semestres")

if __name__ == "__main__":
    setup_academic_structure()