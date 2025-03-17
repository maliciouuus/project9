from django import forms
from django.contrib.auth.models import User
from . import models


class TicketForm(forms.ModelForm):
    """
    Formulaire pour créer ou modifier un ticket.
    Permet de spécifier le titre, la description et une image optionnelle.
    """

    class Meta:
        model = models.Ticket
        fields = ["title", "description", "image"]


class ReviewForm(forms.ModelForm):
    """
    Formulaire pour créer ou modifier une critique.
    Permet de spécifier la note (0-5), le titre et le contenu de la critique.
    """

    class Meta:
        model = models.Review
        fields = ["headline", "rating", "body"]
        widgets = {"rating": forms.RadioSelect(choices=[(i, str(i)) for i in range(6)])}


class UserFollowsForm(forms.Form):
    """
    Formulaire pour suivre un nouvel utilisateur.
    Permet de sélectionner un utilisateur à suivre parmi ceux qui ne sont pas
    déjà suivis.
    """

    followed_user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="Utilisateur à suivre",
        help_text="Sélectionnez l'utilisateur que vous souhaitez suivre",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["followed_user"].queryset = User.objects.exclude(
            username=kwargs.get("initial", {}).get("user", "")
        )
