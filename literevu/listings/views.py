from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import CharField, Value, Q
from django.contrib.auth.models import User
from django.contrib import messages
from itertools import chain
from . import forms
from .models import Ticket, Review, UserFollows, UserBlocks


@login_required
def feed(request):
    """
    Affiche le flux d'activité de l'utilisateur.
    Montre les tickets et critiques de l'utilisateur et des personnes qu'il suit,
    triés par date de création (du plus récent au plus ancien).

    Args:
        request: La requête HTTP

    Returns:
        HttpResponse: Page du flux d'activité
    """
    # Exclusion des utilisateurs bloqués
    blocked_users = request.user.blocking.values("blocked_user")
    users_blocking_me = request.user.blocked_by.values("user")

    # Récupération des tickets avec les utilisateurs associés
    tickets = (
        Ticket.objects.select_related("user")
        .filter(
            Q(user__in=request.user.following.values("followed_user"))
            | Q(user=request.user)
        )
        .exclude(Q(user__in=blocked_users) | Q(user__in=users_blocking_me))
    )

    # Récupération des critiques avec les utilisateurs et tickets associés
    reviews = (
        Review.objects.select_related("user", "ticket", "ticket__user")
        .filter(
            Q(user__in=request.user.following.values("followed_user"))
            | Q(user=request.user)
            | Q(ticket__user=request.user)
        )
        .exclude(Q(user__in=blocked_users) | Q(user__in=users_blocking_me))
    )

    tickets = tickets.annotate(content_type=Value("TICKET", CharField()))
    reviews = reviews.annotate(content_type=Value("REVIEW", CharField()))

    posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True
    )

    return render(request, "listings/feed.html", context={"posts": posts})


def signup_page(request):
    """
    Gère l'inscription des nouveaux utilisateurs.

    Args:
        request: La requête HTTP

    Returns:
        HttpResponse: Page d'inscription ou redirection vers le flux si
            inscription réussie
    """
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("feed")
    return render(request, "listings/signup.html", context={"form": form})


@login_required
def ticket_create(request):
    """
    Permet à l'utilisateur de créer un nouveau ticket (demande de critique).

    Args:
        request: La requête HTTP

    Returns:
        HttpResponse: Page de création de ticket ou redirection vers le flux si
            création réussie
    """
    form = forms.TicketForm()
    if request.method == "POST":
        form = forms.TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect("feed")
    return render(request, "listings/ticket_create.html", {"form": form})


@login_required
def review_create(request, ticket_id=None):
    """
    Permet à l'utilisateur de créer une critique, soit en réponse à un ticket
    existant, soit en créant un nouveau ticket simultanément.

    Args:
        request: La requête HTTP
        ticket_id: ID du ticket existant (optionnel)

    Returns:
        HttpResponse: Page de création de critique ou redirection vers le flux si
            création réussie
    """
    ticket_form = forms.TicketForm()
    review_form = forms.ReviewForm()
    if ticket_id:
        ticket = get_object_or_404(Ticket, id=ticket_id)
        if request.method == "POST":
            review_form = forms.ReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.user = request.user
                review.ticket = ticket
                review.save()
                return redirect("feed")
        return render(
            request,
            "listings/review_create.html",
            {"review_form": review_form, "ticket": ticket},
        )
    else:
        if request.method == "POST":
            ticket_form = forms.TicketForm(request.POST, request.FILES)
            review_form = forms.ReviewForm(request.POST)
            if all([ticket_form.is_valid(), review_form.is_valid()]):
                ticket = ticket_form.save(commit=False)
                ticket.user = request.user
                ticket.save()
                review = review_form.save(commit=False)
                review.user = request.user
                review.ticket = ticket
                review.save()
                return redirect("feed")
        context = {
            "ticket_form": ticket_form,
            "review_form": review_form,
        }
        return render(request, "listings/review_create.html", context=context)


@login_required
def posts(request):
    """
    Affiche tous les posts (tickets et critiques) de l'utilisateur connecté.

    Args:
        request: La requête HTTP

    Returns:
        HttpResponse: Page des posts de l'utilisateur
    """
    tickets = Ticket.objects.filter(user=request.user)
    reviews = Review.objects.filter(user=request.user)

    tickets = tickets.annotate(content_type=Value("TICKET", CharField()))
    reviews = reviews.annotate(content_type=Value("REVIEW", CharField()))

    posts = sorted(
        chain(reviews, tickets), key=lambda post: post.time_created, reverse=True
    )

    return render(request, "listings/posts.html", context={"posts": posts})


@login_required
def follow_users(request):
    """
    Permet à l'utilisateur de suivre d'autres utilisateurs et de voir
    ses abonnements et abonnés.

    Args:
        request: La requête HTTP

    Returns:
        HttpResponse: Page de gestion des abonnements
    """
    form = forms.UserFollowsForm(initial={"user": request.user.username})
    if request.method == "POST":
        form = forms.UserFollowsForm(
            request.POST,
            initial={"user": request.user.username}
        )
        if form.is_valid():
            user_to_follow = form.cleaned_data["followed_user"]
            if user_to_follow != request.user:
                if UserBlocks.objects.filter(
                    Q(user=request.user, blocked_user=user_to_follow)
                    | Q(user=user_to_follow, blocked_user=request.user)
                ).exists():
                    messages.error(
                        request,
                        "Impossible de suivre cet utilisateur car l'un de vous "
                        "a bloqué l'autre.",
                    )
                else:
                    UserFollows.objects.get_or_create(
                        user=request.user,
                        followed_user=user_to_follow
                    )
                    messages.success(
                        request,
                        f"Vous suivez maintenant {user_to_follow.username}"
                    )
            else:
                messages.error(request, "Vous ne pouvez pas vous suivre vous-même.")
            return redirect("follow-users")

    following = UserFollows.objects.select_related("followed_user").filter(
        user=request.user
    )
    followers = UserFollows.objects.select_related("user").filter(
        followed_user=request.user
    )
    blocked = UserBlocks.objects.select_related("blocked_user").filter(
        user=request.user
    )

    return render(
        request,
        "listings/follow_users.html",
        context={
            "form": form,
            "following": following,
            "followers": followers,
            "blocked": blocked,
        },
    )


@login_required
def unfollow_user(request, user_id):
    """
    Permet à l'utilisateur de ne plus suivre un autre utilisateur.

    Args:
        request: La requête HTTP
        user_id: ID de l'utilisateur à ne plus suivre

    Returns:
        HttpResponse: Redirection vers la page des abonnements
    """
    user_to_unfollow = get_object_or_404(User, id=user_id)
    UserFollows.objects.filter(
        user=request.user, followed_user=user_to_unfollow
    ).delete()
    messages.success(request, f"Vous ne suivez plus {user_to_unfollow.username}")
    return redirect("follow-users")


@login_required
def block_user(request, user_id):
    """
    Permet à l'utilisateur de bloquer un autre utilisateur.
    Si l'utilisateur suit déjà la personne qu'il bloque, l'abonnement est
    automatiquement supprimé.

    Args:
        request: La requête HTTP
        user_id: ID de l'utilisateur à bloquer

    Returns:
        HttpResponse: Redirection vers la page des abonnements
    """
    user_to_block = get_object_or_404(User, id=user_id)

    if user_to_block == request.user:
        messages.error(request, "Vous ne pouvez pas vous bloquer vous-même.")
        return redirect("follow-users")

    # Suppression des relations de suivi existantes
    UserFollows.objects.filter(
        Q(user=request.user, followed_user=user_to_block)
        | Q(user=user_to_block, followed_user=request.user)
    ).delete()

    # Création du blocage
    UserBlocks.objects.get_or_create(user=request.user, blocked_user=user_to_block)
    messages.success(request, f"Vous avez bloqué {user_to_block.username}")

    return redirect("follow-users")


@login_required
def unblock_user(request, user_id):
    """
    Permet à l'utilisateur de débloquer un autre utilisateur.

    Args:
        request: La requête HTTP
        user_id: ID de l'utilisateur à débloquer

    Returns:
        HttpResponse: Redirection vers la page des abonnements
    """
    user_to_unblock = get_object_or_404(User, id=user_id)
    UserBlocks.objects.filter(user=request.user, blocked_user=user_to_unblock).delete()
    messages.success(request, f"Vous avez débloqué {user_to_unblock.username}")
    return redirect("follow-users")


@login_required
def ticket_edit(request, ticket_id):
    """
    Permet à l'utilisateur de modifier un de ses tickets.

    Args:
        request: La requête HTTP
        ticket_id: ID du ticket à modifier

    Returns:
        HttpResponse: Page d'édition du ticket ou redirection vers les posts si
            modification réussie
    """
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)
    if request.method == "POST":
        form = forms.TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect("posts")
    else:
        form = forms.TicketForm(instance=ticket)
    return render(
        request, "listings/ticket_edit.html", {"form": form, "ticket": ticket}
    )


@login_required
def ticket_delete(request, ticket_id):
    """
    Permet à l'utilisateur de supprimer un de ses tickets.

    Args:
        request: La requête HTTP
        ticket_id: ID du ticket à supprimer

    Returns:
        HttpResponse: Page de confirmation ou redirection vers les posts si
            suppression effectuée
    """
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)
    if request.method == "POST":
        ticket.delete()
        return redirect("posts")
    return render(request, "listings/ticket_delete.html", {"ticket": ticket})


@login_required
def review_edit(request, review_id):
    """
    Permet à l'utilisateur de modifier une de ses critiques.

    Args:
        request: La requête HTTP
        review_id: ID de la critique à modifier

    Returns:
        HttpResponse: Page d'édition de la critique ou redirection vers les posts si
            modification réussie
    """
    review = get_object_or_404(Review, id=review_id, user=request.user)
    if request.method == "POST":
        form = forms.ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect("posts")
    else:
        form = forms.ReviewForm(instance=review)
    return render(
        request, "listings/review_edit.html", {"form": form, "review": review}
    )


@login_required
def review_delete(request, review_id):
    """
    Permet à l'utilisateur de supprimer une de ses critiques.

    Args:
        request: La requête HTTP
        review_id: ID de la critique à supprimer

    Returns:
        HttpResponse: Page de confirmation ou redirection vers les posts si
            suppression effectuée
    """
    review = get_object_or_404(Review, id=review_id, user=request.user)
    if request.method == "POST":
        review.delete()
        return redirect("posts")
    return render(request, "listings/review_delete.html", {"review": review})
