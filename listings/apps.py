from django.apps import AppConfig


class ListingsConfig(AppConfig):
    """
    Configuration de l'application Listings.
    Cette application gère les tickets, critiques et abonnements entre utilisateurs.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "listings"
