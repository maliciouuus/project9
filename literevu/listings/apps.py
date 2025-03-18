"""
Configuration de l'application Listings pour le projet LITRevu.

Cette application gère :
- Les tickets (demandes de critique)
- Les critiques de livres et articles
- Les relations entre utilisateurs (abonnements et blocages)
- L'interface utilisateur et les formulaires associés
"""

from django.apps import AppConfig


class ListingsConfig(AppConfig):
    """
    Configuration principale de l'application Listings.

    Cette classe définit :
    - Le type de clé primaire par défaut (BigAutoField)
    - Le nom de l'application pour Django
    - Les paramètres spécifiques à l'application
    """

    # Utilisation de BigAutoField pour supporter un grand nombre d'entrées
    default_auto_field = "django.db.models.BigAutoField"

    # Nom de l'application tel qu'utilisé par Django
    name = "listings"

    # Nom plus lisible pour l'interface d'administration
    verbose_name = "LITRevu - Critiques de livres"
