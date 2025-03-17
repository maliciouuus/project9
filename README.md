# LITRevu

Application web de partage de critiques de livres développée avec Django.

## Fonctionnalités

- Système d'authentification (inscription, connexion, déconnexion)
- Création de tickets (demandes de critique)
- Création de critiques (avec ou sans ticket associé)
- Système de notation (0 à 5 étoiles)
- Flux d'activité personnalisé
- Système d'abonnement entre utilisateurs
- Gestion des posts (modification, suppression)

## Installation

1. Cloner le repository
```bash
git clone <repository-url>
cd literevu
```

2. Créer un environnement virtuel
```bash
python -m venv env
source env/bin/activate  # Linux/MacOS
# ou
env\Scripts\activate  # Windows
```

3. Installer les dépendances
```bash
pip install -r requirements.txt
```

4. Appliquer les migrations
```bash
python manage.py migrate
```

5. Créer un superutilisateur
```bash
python manage.py createsuperuser
```

6. (Optionnel) Créer des utilisateurs de test
```bash
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_user('user1', password='testpass123'); User.objects.create_user('user2', password='testpass123')"
```
Cette commande créera deux utilisateurs de test :
- user1 (mot de passe : testpass123)
- user2 (mot de passe : testpass123)

7. Lancer le serveur
```bash
python manage.py runserver
```

L'application sera accessible à l'adresse : http://127.0.0.1:8000/

## Qualité du code

Le projet utilise Black et Flake8 pour maintenir un code propre et cohérent.

Pour formater le code avec Black :
```bash
black .
```

Pour vérifier le code avec Flake8 :
```bash
flake8
```

## Comptes de test

| Identifiant | Mot de passe |
|-------------|--------------|
| admin       | admin123     |
| user1       | testpass123  |
| user2       | testpass123  |

## Structure du projet

```
literevu/
├── listings/              # Application principale
│   ├── models.py         # Modèles de données
│   ├── views.py          # Vues
│   ├── forms.py          # Formulaires
│   ├── urls.py           # URLs
│   └── templates/        # Templates HTML
├── static/               # Fichiers statiques
├── media/               # Fichiers uploadés
└── manage.py            # Script de gestion Django
```

## Technologies utilisées

- Python 3.9+
- Django 5.0
- Bootstrap 5.1
- SQLite3
- Black (formatage de code)
- Flake8 (linting)

## Accessibilité

L'application respecte les normes WCAG :
- Navigation au clavier
- Contraste suffisant
- Textes alternatifs pour les images
- Labels explicites pour les formulaires
- Structure sémantique HTML5 