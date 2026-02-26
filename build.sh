#!/usr/bin/env bash
# build.sh

echo "🚀 Début du build sur Render"
echo "📦 Installation des dépendances..."
pip install -r requirements.txt

echo "🗃️  Application des migrations..."
python manage.py migrate --noinput

echo "📦 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput

echo "✅ Build terminé avec succès !"