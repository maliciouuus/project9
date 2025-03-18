"""
Configuration Django pour le projet literevu.

Ce fichier contient tous les paramètres de configuration du projet Django.
Il définit notamment :
- Les applications installées
- La configuration de la base de données
- Les paramètres de sécurité
- La gestion des fichiers statiques et médias
- Les paramètres d'authentification
"""

from pathlib import Path

# Construction des chemins de fichiers
# BASE_DIR représente le répertoire racine du projet
BASE_DIR = Path(__file__).resolve().parent.parent


# Paramètres de développement rapide - à ne pas utiliser en production
# Voir https://docs.djangoproject.com/fr/5.0/howto/deployment/checklist/

# AVERTISSEMENT : gardez la clé secrète secrète en production !
SECRET_KEY = "django-insecure-vau$wjl-p86p7**k2s^3j*ejodf5*=l%2xmx=k7*k#7bm=r@%o"

# AVERTISSEMENT : ne pas activer le mode debug en production !
DEBUG = True

# Liste des hôtes autorisés à servir l'application
ALLOWED_HOSTS = []


# Définition des applications

INSTALLED_APPS = [
    # Applications Django par défaut
    "django.contrib.admin",  # Interface d'administration
    "django.contrib.auth",  # Système d'authentification
    "django.contrib.contenttypes",  # Gestion des types de contenu
    "django.contrib.sessions",  # Gestion des sessions
    "django.contrib.messages",  # Système de messages
    "django.contrib.staticfiles",  # Gestion des fichiers statiques
    # Nos applications
    "listings",  # Application principale de LITRevu
]

# Middleware - Composants qui traitent les requêtes/réponses
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",  # Sécurité
    "django.contrib.sessions.middleware.SessionMiddleware",  # Sessions
    "django.middleware.common.CommonMiddleware",  # Fonctionnalités communes
    "django.middleware.csrf.CsrfViewMiddleware",  # Protection CSRF
    "django.contrib.auth.middleware.AuthenticationMiddleware",  # Authentification
    "django.contrib.messages.middleware.MessageMiddleware",  # Messages
    "django.middleware.clickjacking.XFrameOptionsMiddleware",  # Protection clickjacking
]

# Configuration des URLs racines
ROOT_URLCONF = "literevu.urls"

# Configuration des templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],  # Répertoires supplémentaires pour les templates
        "APP_DIRS": True,  # Chercher les templates dans les applications
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Configuration WSGI pour le déploiement
WSGI_APPLICATION = "literevu.wsgi.application"


# Configuration de la base de données
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",  # Utilisation de SQLite
        "NAME": BASE_DIR / "db.sqlite3",  # Chemin vers le fichier de base de données
    }
}


# Validation des mots de passe
AUTH_PASSWORD_VALIDATORS = [
    {
        # Vérifie que le mot de passe n'est pas trop similaire aux données de l'user
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        # Vérifie la longueur minimale du mot de passe
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        # Vérifie que le mot de passe n'est pas trop commun
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        # Vérifie que le mot de passe n'est pas entièrement numérique
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Paramètres d'internationalisation
LANGUAGE_CODE = "fr-fr"  # Langue par défaut : français
TIME_ZONE = "UTC"  # Fuseau horaire
USE_I18N = True  # Activation de l'internationalisation
USE_TZ = True  # Activation des fuseaux horaires


# Configuration des fichiers statiques
STATIC_URL = "static/"  # URL pour accéder aux fichiers statiques
STATIC_ROOT = BASE_DIR / "staticfiles"  # Répertoire de collecte des fichiers statiques
STATICFILES_DIRS = [
    BASE_DIR / "static"
]  # Répertoires supplémentaires de fichiers statiques

# Configuration des fichiers média (uploadés par les utilisateurs)
MEDIA_URL = "/media/"  # URL pour accéder aux fichiers média
MEDIA_ROOT = BASE_DIR / "media"  # Répertoire de stockage des fichiers média

# Configuration de l'authentification
LOGIN_URL = "login"  # URL de la page de connexion
LOGIN_REDIRECT_URL = "feed"  # Redirection après connexion
LOGOUT_REDIRECT_URL = "login"  # Redirection après déconnexion

# Type de clé primaire par défaut
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
