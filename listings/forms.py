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
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "image": forms.FileInput(attrs={
                "class": "form-control",
                "accept": "image/*"
            })
        }


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
        error_messages={
            'invalid_choice': "Cet utilisateur n'existe pas.",
            'required': "Veuillez sélectionner un utilisateur à suivre."
        }
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['followed_user'].queryset = User.objects.exclude(
                id__in=[self.user.id] + list(self.user.following.values_list('followed_user', flat=True))
            )

    def clean_followed_user(self):
        followed_user = self.cleaned_data['followed_user']
        if followed_user == self.user:
            raise forms.ValidationError("Vous ne pouvez pas vous suivre vous-même.")
        return followed_user
