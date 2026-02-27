import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()

from python_project.models import Level, Semester

def fix_all_semesters():
    """Corrige tous les semestres : noms, ordres, et supprime les doublons"""
    
    print("🚀 CORRECTION COMPLÈTE DES SEMESTRES")
    print("=" * 60)
    
    # 1. Standardiser les noms des semestres
    print("\n📝 STANDARDISATION DES NOMS")
    print("-" * 40)
    
    semestres_corriges = 0
    for sem in Semester.objects.all():
        ancien_nom = sem.name
        if sem.name == 'Semester 1':
            sem.name = 'Semestre 1'
            sem.save()
            semestres_corriges += 1
            print(f"  ✅ {sem.code} - {sem.level.name}: '{ancien_nom}' → '{sem.name}'")
    
    # 2. Définir les ordres corrects pour chaque code
    ordres_corrects = {
        'S1': 1,
        'S2': 2,
        'S3': 3,
        'S4': 4,
        'S5': 5,
        'S6': 6,
    }
    
    print("\n🔄 CORRECTION DES ORDRES")
    print("-" * 40)
    
    ordres_corriges = 0
    for sem in Semester.objects.all():
        if sem.code in ordres_corrects:
            nouvel_ordre = ordres_corrects[sem.code]
            if sem.order != nouvel_ordre:
                print(f"  ✅ {sem.level.speciality.name} - {sem.level.name} - {sem.code}: order {sem.order} → {nouvel_ordre}")
                sem.order = nouvel_ordre
                sem.save()
                ordres_corriges += 1
    
    # 3. Vérifier les doublons (même level + même code)
    print("\n🔍 RECHERCHE DES DOUBLONS")
    print("-" * 40)
    
    vus = set()
    doublons_supprimes = 0
    
    for sem in Semester.objects.all().order_by('level', 'code'):
        key = f"{sem.level.id}_{sem.code}"
        if key in vus:
            print(f"  ❌ Doublon supprimé: {sem.level.speciality.name} - {sem.level.name} - {sem.code} (ID: {sem.id})")
            sem.delete()
            doublons_supprimes += 1
        else:
            vus.add(key)
    
    # 4. Vérifier le nombre de semestres par niveau
    print("\n📊 VÉRIFICATION PAR NIVEAU")
    print("-" * 40)
    
    for level in Level.objects.all().order_by('speciality', 'order'):
        semestres = Semester.objects.filter(level=level).order_by('code')
        codes = [s.code for s in semestres]
        
        # Déterminer les codes attendus selon le niveau
        if level.name in ['L1', 'M1']:
            attendus = ['S1', 'S2']
        elif level.name in ['L2', 'M2']:
            attendus = ['S3', 'S4']
        elif level.name == 'L3':
            attendus = ['S5', 'S6']
        else:
            attendus = []
        
        if set(codes) == set(attendus):
            print(f"  ✅ {level.speciality.name} - {level.name}: {codes}")
        else:
            print(f"  ⚠️ {level.speciality.name} - {level.name}: trouvé {codes}, attendu {attendus}")
    
    # 5. Statistiques finales
    print("\n" + "=" * 60)
    print("📊 STATISTIQUES FINALES")
    print("=" * 60)
    print(f"📝 Noms corrigés: {semestres_corriges}")
    print(f"🔄 Ordres corrigés: {ordres_corriges}")
    print(f"🗑️ Doublons supprimés: {doublons_supprimes}")
    print(f"📅 Total semestres après correction: {Semester.objects.count()}")

if __name__ == "__main__":
    fix_all_semesters()