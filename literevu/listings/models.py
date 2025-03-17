from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models


class Ticket(models.Model):
    """
    Modèle représentant une demande de critique.
    Un ticket est créé par un utilisateur pour demander des critiques sur un
    livre/article.
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
        return f"{self.title}"


class Review(models.Model):
    """
    Modèle représentant une critique.
    Une critique est créée par un utilisateur en réponse à un ticket.
    Elle contient une note et un commentaire sur le livre/article.
    """

    ticket = models.ForeignKey(
        to=Ticket,
        on_delete=models.CASCADE,
        help_text="Le ticket auquel cette critique répond",
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text="La note attribuée (entre 0 et 5)",
    )
    headline = models.CharField(max_length=128, help_text="Le titre de la critique")
    body = models.CharField(
        max_length=8192, blank=True, help_text="Le contenu de la critique"
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
        return f"Review of {self.ticket.title} by {self.user.username}"


class UserFollows(models.Model):
    """
    Modèle représentant une relation d'abonnement entre deux utilisateurs.
    Permet de suivre les publications d'autres utilisateurs.
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
        # ensures we don't get multiple UserFollows instances
        # for unique user-user_followed pairs
        unique_together = (
            "user",
            "followed_user",
        )

    def __str__(self):
        return f"{self.user} follows {self.followed_user}"


class UserBlocks(models.Model):
    """
    Modèle représentant une relation de blocage entre deux utilisateurs.
    Permet de bloquer les publications d'autres utilisateurs.
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
        unique_together = (
            "user",
            "blocked_user",
        )

    def __str__(self):
        return f"{self.user} blocks {self.blocked_user}"
