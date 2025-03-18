"""
Modèles de données pour l'application LITRevu.

Ce fichier définit la structure de la base de données de l'application.
Il contient quatre modèles principaux :
- Ticket : pour les demandes de critique
- Review : pour les critiques
- UserFollows : pour les abonnements entre utilisateurs
- UserBlocks : pour les blocages entre utilisateurs
"""

from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models


class Ticket(models.Model):
    """
    Modèle représentant une demande de critique.

    Un ticket est créé par un utilisateur pour demander des critiques sur un
    livre ou un article. Il contient :
    - Un titre obligatoire
    - Une description optionnelle
    - Une image de couverture optionnelle
    - Une référence à l'utilisateur qui l'a créé
    - La date et l'heure de création
    """

    title = models.CharField(
        max_length=128, help_text="Le titre du livre ou de l'article"
    )
    description = models.TextField(
        max_length=2048, blank=True, help_text="La description du livre ou de l'article"
    )
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        help_text="L'utilisateur qui a créé le ticket",
    )
    image = models.ImageField(
        null=True,
        blank=True,
        upload_to="tickets/",
        help_text="La couverture du livre ou une image de l'article",
    )
    time_created = models.DateTimeField(
        auto_now_add=True, help_text="La date et l'heure de création du ticket"
    )

    def __str__(self):
        """Représentation textuelle du ticket"""
        return f"{self.title}"


class Review(models.Model):
    """
    Modèle représentant une critique.

    Une critique est créée par un utilisateur en réponse à un ticket.
    Elle contient :
    - Une référence au ticket concerné
    - Une note de 0 à 5 étoiles
    - Un titre (headline)
    - Un contenu détaillé
    - Une référence à l'utilisateur qui l'a créée
    - La date et l'heure de création
    """

    ticket = models.ForeignKey(
        to=Ticket,
        on_delete=models.CASCADE,
        help_text="Le ticket auquel cette critique répond",
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text="La note attribuée (entre 0 et 5 étoiles)",
    )
    headline = models.CharField(max_length=128, help_text="Le titre de la critique")
    body = models.TextField(
        max_length=8192, blank=True, help_text="Le contenu détaillé de la critique"
    )
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        help_text="L'utilisateur qui a écrit la critique",
    )
    time_created = models.DateTimeField(
        auto_now_add=True, help_text="La date et l'heure de création de la critique"
    )

    def __str__(self):
        """Représentation textuelle de la critique"""
        return f"Critique de {self.ticket.title} par {self.user.username}"


class UserFollows(models.Model):
    """
    Modèle représentant une relation d'abonnement entre deux utilisateurs.

    Permet à un utilisateur de suivre les publications d'autres utilisateurs.
    La relation est unidirectionnelle : si A suit B, B ne suit pas automatiquement A.

    Attributs :
    - user : l'utilisateur qui suit
    - followed_user : l'utilisateur qui est suivi
    """

    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="following",
        help_text="L'utilisateur qui suit",
    )
    followed_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="followed_by",
        help_text="L'utilisateur qui est suivi",
    )

    class Meta:
        """
        Métadonnées du modèle.
        Garantit qu'un utilisateur ne peut pas suivre plusieurs fois la même personne.
        """

        unique_together = ("user", "followed_user")

    def __str__(self):
        """Représentation textuelle de la relation de suivi"""
        return f"{self.user} suit {self.followed_user}"


class UserBlocks(models.Model):
    """
    Modèle représentant une relation de blocage entre deux utilisateurs.

    Permet à un utilisateur de bloquer les publications d'autres utilisateurs.
    Quand un utilisateur en bloque un autre :
    - Il ne voit plus ses publications
    - Il ne peut plus le suivre
    - L'autre utilisateur ne peut plus le suivre

    Attributs :
    - user : l'utilisateur qui bloque
    - blocked_user : l'utilisateur qui est bloqué
    - time_created : date et heure du blocage
    """

    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="blocking",
        help_text="L'utilisateur qui bloque",
    )
    blocked_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="blocked_by",
        help_text="L'utilisateur qui est bloqué",
    )
    time_created = models.DateTimeField(
        auto_now_add=True, help_text="La date et l'heure du blocage"
    )

    class Meta:
        """
        Métadonnées du modèle.
        Garantit qu'un utilisateur ne peut pas bloquer plusieurs fois la même personne.
        """

        unique_together = ("user", "blocked_user")

    def __str__(self):
        """Représentation textuelle de la relation de blocage"""
        return f"{self.user} bloque {self.blocked_user}"
