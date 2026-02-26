# diagnostic_complet.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()

from python_project.models import *
from django.db.models import Count

def diagnostic_complet():
    print("="*70)
    print("🔍 DIAGNOSTIC COMPLET DU SYSTÈME D'ALERTES")
    print("="*70)
    
    # 1. VÉRIFICATION DES MODÈLES
    print("\n1. 📦 MODÈLES ET BASE DE DONNÉES")
    print("-"*50)
    
    modeles = [
        ("Universités", University),
        ("Spécialités", Speciality),
        ("Niveaux", Level),
        ("Semestres", Semester),
        ("Matières", Matiere),
        ("Documents", Document),
        ("Liens User-University", UserUniversity),
        ("Alertes", Alert),
    ]
    
    for nom, modele in modeles:
        count = modele.objects.count()
        status = "✅" if count > 0 else "⚠️"
        print(f"  {status} {nom}: {count}")
    
    # 2. VÉRIFICATION DES LIENS
    print("\n2. 🔗 LIENS UTILISATEUR-UNIVERSITÉ")
    print("-"*50)
    
    users = ['test123', 'user456', 'firebase_user_123']
    for user in users:
        liens = UserUniversity.objects.filter(user_id=user)
        count = liens.count()
        if count > 0:
            print(f"  ✅ {user}: {count} universités")
            for lien in liens[:3]:  # Afficher max 3
                print(f"     • {lien.university.name}")
            if count > 3:
                print(f"     ... et {count-3} autres")
        else:
            print(f"  ⚠️ {user}: aucun lien")
    
    # 3. VÉRIFICATION DES ALERTES
    print("\n3. 📝 ALERTES PAR UTILISATEUR")
    print("-"*50)
    
    for user in users:
        alerts = Alert.objects.filter(user_id=user).order_by('-created_at')
        count = alerts.count()
        if count > 0:
            print(f"  ✅ {user}: {count} alertes")
            for alert in alerts[:3]:  # 3 dernières alertes
                print(f"     • {alert.title}: {alert.message[:50]}...")
            if count > 3:
                print(f"     ... et {count-3} autres")
        else:
            print(f"  ⚠️ {user}: aucune alerte")
    
    # 4. TEST DE CRÉATION
    print("\n4. 🧪 TEST DE CRÉATION D'UNE NOUVELLE ENTITÉ")
    print("-"*50)
    
    # Tester la création d'un niveau
    try:
        level, created = Level.objects.get_or_create(name="M2")
        print(f"  ✅ Niveau M2: {'créé' if created else 'existe déjà'}")
    except Exception as e:
        print(f"  ❌ Erreur niveau: {e}")
    
    # Tester la création d'une spécialité
    try:
        uni = University.objects.first()
        if uni:
            spec, created = Speciality.objects.get_or_create(
                name="Test Diagnostic",
                university=uni
            )
            print(f"  ✅ Spécialité Test: {'créée' if created else 'existe déjà'}")
    except Exception as e:
        print(f"  ❌ Erreur spécialité: {e}")
    
    # 5. VÉRIFICATION DES SIGNAUX
    print("\n5. ⚡ VÉRIFICATION DES SIGNAUX")
    print("-"*50)
    
    # Compter les alertes avant
    avant = Alert.objects.count()
    
    # Créer une université test
    uni_test = University.objects.create(name="Université Diagnostic")
    print(f"  ✅ Université de test créée")
    
    # Compter les alertes après
    apres = Alert.objects.count()
    if apres > avant:
        print(f"  ✅ {apres - avant} nouvelle(s) alerte(s) générée(s)")
    else:
        print(f"  ⚠️ Aucune alerte générée")
    
    # 6. VÉRIFICATION DE L'API
    print("\n6. 🌐 VÉRIFICATION DE L'API")
    print("-"*50)
    
    import requests
    try:
        for user in users:
            url = f"http://127.0.0.1:8000/api/alerts/?user={user}"
            response = requests.get(url, timeout=2)
            if response.status_code == 200:
                data = response.json()
                print(f"  ✅ API {user}: {len(data)} alertes")
            else:
                print(f"  ⚠️ API {user}: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("  ⚠️ Serveur non accessible (lancez python manage.py runserver)")
    except Exception as e:
        print(f"  ⚠️ Erreur API: {e}")
    
    # 7. RÉSUMÉ FINAL
    print("\n" + "="*70)
    print("📊 RÉSUMÉ GÉNÉRAL")
    print("="*70)
    
    total_points = 0
    max_points = 0
    
    # Vérification des modèles
    if University.objects.count() > 0: total_points += 1
    max_points += 1
    if Speciality.objects.count() > 0: total_points += 1
    max_points += 1
    if Level.objects.count() > 0: total_points += 1
    max_points += 1
    if Semester.objects.count() > 0: total_points += 1
    max_points += 1
    if Matiere.objects.count() > 0: total_points += 1
    max_points += 1
    if Document.objects.count() > 0: total_points += 1
    max_points += 1
    
    # Vérification des liens
    if UserUniversity.objects.count() >= 8: total_points += 2
    elif UserUniversity.objects.count() > 0: total_points += 1
    max_points += 2
    
    # Vérification des alertes
    if Alert.objects.count() >= 10: total_points += 2
    elif Alert.objects.count() > 0: total_points += 1
    max_points += 2
    
    # Vérification des signaux
    if apres > avant: total_points += 1
    max_points += 1
    
    score = (total_points / max_points) * 100
    
    print(f"\n  Score de santé: {score:.1f}%")
    print(f"  Points: {total_points}/{max_points}")
    
    if score >= 90:
        print("\n  🏆 STATUT: PARFAIT ! Tout fonctionne correctement")
    elif score >= 70:
        print("\n  ✅ STATUT: BON - Quelques améliorations possibles")
    elif score >= 50:
        print("\n  ⚠️ STATUT: MOYEN - Des problèmes à corriger")
    else:
        print("\n  ❌ STATUT: CRITIQUE - Système non fonctionnel")
    
    print("\n" + "="*70)
    print("🏁 DIAGNOSTIC TERMINÉ")
    print("="*70)

if __name__ == "__main__":
    diagnostic_complet()