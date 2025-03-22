#!/bin/bash

echo "🚀 Initialisation du projet LITRevu..."

# Se placer dans le bon répertoire
echo "📂 Changement vers le répertoire literevu..."
cd literevu || {
    echo "❌ Erreur : Impossible d'accéder au répertoire literevu"
    exit 1
}

# Supprimer l'ancienne base de données, les migrations et les fichiers cache
echo "🗑️  Nettoyage des fichiers..."
rm -f db.sqlite3
rm -f listings/migrations/0*.py
find . -type d -name "__pycache__" -exec rm -r {} +

# Créer les migrations
echo "📝 Création des nouvelles migrations..."
python3 manage.py makemigrations listings

# Appliquer les migrations
echo "⚙️  Application des migrations..."
python3 manage.py migrate

# Créer le superutilisateur
echo "👤 Création du superutilisateur..."
python3 manage.py createsuperuser

# Créer les utilisateurs de test
echo "👥 Création des utilisateurs de test..."
python3 manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_user('user1', password='testpass123'); User.objects.create_user('user2', password='testpass123')"

echo "✅ Initialisation terminée !"
echo "
Comptes créés :
- Superutilisateur : celui que vous venez de créer
- user1 / testpass123
- user2 / testpass123

⚠️  IMPORTANT : Toutes les commandes doivent être exécutées depuis le répertoire 'literevu'
Pour lancer le serveur :
cd literevu  # Si vous n'y êtes pas déjà
python3 manage.py runserver 8080

L'application sera accessible à l'adresse : http://127.0.0.1:8080/
"

# Rester dans le répertoire literevu
exec $SHELL 