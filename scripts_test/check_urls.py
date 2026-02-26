# check_urls.py
import requests

BASE_URL = "http://127.0.0.1:8000"

urls_to_test = [
    ("/admin/", "Admin personnalisé"),
    ("/admin/dashboard/", "Dashboard admin"),
    ("/django-admin/", "Admin Django"),
    ("/api/universities/", "API Universities"),
    ("/api/alerts/?user=test123", "API Alertes"),
]

print("Vérification des URLs...")
print("="*50)

for url, description in urls_to_test:
    full_url = f"{BASE_URL}{url}"
    try:
        response = requests.get(full_url)
        status = "✅" if response.status_code < 400 else "❌"
        print(f"{status} {description}: {full_url} ({response.status_code})")
    except requests.exceptions.ConnectionError:
        print(f"❌ {description}: {full_url} (Serveur non accessible - lancez d'abord python manage.py runserver)")
    except Exception as e:
        print(f"❌ {description}: {full_url} (Erreur: {e})")

print("="*50)