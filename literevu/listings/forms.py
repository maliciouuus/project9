"""
Formulaires pour l'application LITRevu.

Ce fichier définit les formulaires utilisés dans l'application :
- TicketForm : création et modification de tickets
- ReviewForm : création et modification de critiques
- UserFollowsForm : gestion des abonnements entre utilisateurs
"""

from django import forms
from django.contrib.auth.models import User
from . import models


class TicketForm(forms.ModelForm):
    """
    Formulaire pour créer ou modifier un ticket.

    Ce formulaire permet aux utilisateurs de :
    - Donner un titre au livre/article
    - Ajouter une description détaillée
    - Télécharger une image de couverture

    Tous les champs utilisent les classes Bootstrap pour le style.
    """

    class Meta:
        model = models.Ticket
        fields = ["title", "description", "image"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Titre du livre ou de l'article",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Ajoutez une description...",
                }
            ),
            "image": forms.FileInput(
                attrs={"class": "form-control", "accept": "image/*"}
            ),
        }


class ReviewForm(forms.ModelForm):
    """
    Formulaire pour créer ou modifier une critique.

    Ce formulaire permet aux utilisateurs de :
    - Donner un titre à leur critique
    - Attribuer une note de 0 à 5 étoiles
    - Rédiger le contenu de leur critique

    La note est présentée sous forme de boutons radio pour une meilleure
    expérience utilisateur.
    """

    class Meta:
        model = models.Review
        fields = ["headline", "rating", "body"]
        widgets = {
            "headline": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Titre de votre critique",
                }
            ),
            "rating": forms.RadioSelect(
                choices=[(i, f"{i} étoile{'s' if i > 1 else ''}") for i in range(6)]
            ),
            "body": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 6,
                    "placeholder": "Rédigez votre critique...",
                }
            ),
        }


class UserFollowsForm(forms.Form):
    """
    Formulaire pour suivre un nouvel utilisateur.

    Ce formulaire permet aux utilisateurs de :
    - Voir la liste des utilisateurs qu'ils peuvent suivre
    - Sélectionner un utilisateur à suivre

    Caractéristiques :
    - Exclut l'utilisateur courant de la liste
    - Exclut les utilisateurs déjà suivis
    - Utilise un menu déroulant avec autocomplétion
    """

    followed_user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="Utilisateur à suivre",
        help_text="Sélectionnez l'utilisateur que vous souhaitez suivre",
        widget=forms.Select(
            attrs={"class": "form-control", "placeholder": "Choisir un utilisateur"}
        ),
        error_messages={
            "invalid_choice": "Cet utilisateur n'existe pas.",
            "required": "Veuillez sélectionner un utilisateur à suivre.",
        },
    )

    def __init__(self, *args, **kwargs):
        """
        Initialisation du formulaire.

        Personnalise la liste des utilisateurs disponibles en :
        - Excluant l'utilisateur courant
        - Excluant les utilisateurs déjà suivis

        Args:
            user: L'utilisateur courant
        """
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if self.user:
            # Récupère la liste des utilisateurs déjà suivis
            followed_users = self.user.following.values_list("followed_user", flat=True)
            # Exclut l'utilisateur courant et les utilisateurs déjà suivis
            exclude_ids = [self.user.id] + list(followed_users)
            self.fields["followed_user"].queryset = User.objects.exclude(
                id__in=exclude_ids
            )

    def clean_followed_user(self):
        """
        Validation du champ followed_user.

        Vérifie que l'utilisateur ne tente pas de se suivre lui-même.

        Returns:
            User: L'utilisateur à suivre

        Raises:
            ValidationError: Si l'utilisateur tente de se suivre lui-même
        """
        followed_user = self.cleaned_data["followed_user"]
        if followed_user == self.user:
            raise forms.ValidationError("Vous ne pouvez pas vous suivre vous-même.")
        return followed_user
