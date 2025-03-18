# LITRevu

Application web Django permettant le partage et la critique de livres entre utilisateurs.

## Fonctionnalités

- **Système d'authentification**
  - Inscription et connexion des utilisateurs
  - Protection des routes pour utilisateurs authentifiés

- **Gestion des tickets**
  - Création de demandes de critique
  - Modification et suppression de ses tickets
  - Upload d'images de couverture

- **Gestion des critiques**
  - Création de critiques en réponse aux tickets
  - Création de critiques avec ticket simultané
  - Système de notation (0-5 étoiles)
  - Modification et suppression de ses critiques

- **Système de suivi**
  - Abonnement à d'autres utilisateurs
  - Gestion des abonnements et abonnés
  - Système de blocage d'utilisateurs

- **Flux d'activité**
  - Affichage des tickets et critiques des utilisateurs suivis
  - Tri chronologique des publications
  - Filtrage selon les relations (blocages)

## Installation

1. Cloner le projet
```bash
git clone <url-du-repo>
cd project9
```

2. Créer et activer l'environnement virtuel
```bash
python -m venv env
source env/bin/activate  # Linux/MacOS
# ou
env\Scripts\activate     # Windows
```

3. Installer les dépendances
```bash
pip install -r requirements.txt
```

4. Initialiser le projet
```bash
./init_project.sh
```

## Scripts utilitaires

- `init_project.sh` : Initialise/réinitialise le projet
  - Crée les migrations
  - Configure la base de données
  - Crée un superutilisateur
  - Crée des utilisateurs de test

- `clean_project.sh` : Nettoie le projet
  - Supprime l'environnement virtuel
  - Supprime la base de données
  - Supprime les fichiers cache
  - Supprime les migrations

## Comptes de test

| Identifiant | Mot de passe |
|-------------|--------------|
| user1       | testpass123  |
| user2       | testpass123  |

## Technologies

- Python 3.9+
- Django 5.0
- Bootstrap 5.1
- SQLite3

## Qualité du code

Le projet utilise :
- Black pour le formatage
- Flake8 pour le linting

## Accessibilité

L'application respecte les normes WCAG :
- Navigation au clavier
- Contraste suffisant
- Textes alternatifs
- Structure sémantique HTML5 