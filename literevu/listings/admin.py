"""
Configuration de l'interface d'administration pour l'application LITRevu.

Ce fichier définit comment les modèles sont affichés et gérés dans
l'interface d'administration Django. Il permet aux administrateurs de :
- Visualiser les tickets, critiques et relations entre utilisateurs
- Filtrer et rechercher les données
- Modifier ou supprimer des entrées
"""

from django.contrib import admin
from .models import Ticket, Review, UserFollows


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    """
    Configuration de l'interface d'administration pour les tickets.

    Fonctionnalités :
    - Liste les tickets avec leur titre, auteur et date de création
    - Permet de filtrer par utilisateur et date
    - Permet de rechercher dans les titres et descriptions
    """

    list_display = ("title", "user", "time_created")
    list_filter = ("user", "time_created")
    search_fields = ("title", "description")
    ordering = ("-time_created",)  # Tri par date décroissante


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    Configuration de l'interface d'administration pour les critiques.

    Fonctionnalités :
    - Liste les critiques avec leur titre, note, auteur, ticket associé et date
    - Permet de filtrer par note, utilisateur et date
    - Permet de rechercher dans les titres et contenus
    """

    list_display = ("headline", "rating", "user", "ticket", "time_created")
    list_filter = ("rating", "user", "time_created")
    search_fields = ("headline", "body")
    ordering = ("-time_created",)  # Tri par date décroissante


@admin.register(UserFollows)
class UserFollowsAdmin(admin.ModelAdmin):
    """
    Configuration de l'interface d'administration pour les abonnements.

    Fonctionnalités :
    - Liste les relations d'abonnement entre utilisateurs
    - Permet de filtrer par utilisateur (suiveur et suivi)
    - Affiche clairement qui suit qui
    """

    list_display = ("user", "followed_user")
    list_filter = ("user", "followed_user")
    search_fields = ("user__username", "followed_user__username")
    ordering = ("user__username", "followed_user__username")
