#!/bin/bash

echo "🧹 Nettoyage complet du projet LITRevu..."

# Supprimer l'environnement virtuel
echo "🗑️  Suppression de l'environnement virtuel..."
rm -rf env/
rm -rf venv/

# Supprimer la base de données
echo "🗑️  Suppression de la base de données..."
rm -f literevu/db.sqlite3

# Supprimer les fichiers de migrations
echo "🗑️  Suppression des fichiers de migrations..."
rm -f literevu/listings/migrations/0*.py

# Supprimer tous les __pycache__
echo "🗑️  Suppression des fichiers cache Python..."
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

# Supprimer les fichiers média uploadés
echo "🗑️  Suppression des fichiers média..."
rm -rf literevu/media/*

# Supprimer les fichiers statiques collectés
echo "🗑️  Suppression des fichiers statiques collectés..."
rm -rf literevu/staticfiles/

# Supprimer les fichiers .egg-info
echo "🗑️  Suppression des fichiers .egg-info..."
rm -rf *.egg-info/

# NE PLUS SUPPRIMER les fichiers de configuration WSGI/ASGI car ils sont nécessaires !
# echo "🗑️  Suppression des fichiers WSGI/ASGI..."
# rm -f literevu/literevu/wsgi.py
# rm -f literevu/literevu/asgi.py

echo "✨ Nettoyage terminé !"
echo "
Pour réinitialiser le projet :
1. Créer un nouvel environnement virtuel :
   python -m venv env
   source env/bin/activate  # Linux/MacOS
   # ou
   env\\Scripts\\activate  # Windows

2. Installer les dépendances :
   pip install -r requirements.txt

3. Exécuter le script d'initialisation :
   ./init_project.sh
" 