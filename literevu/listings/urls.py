from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
    path(
        "",
        LoginView.as_view(
            template_name="listings/login.html", redirect_authenticated_user=True
        ),
        name="login",
    ),
    path("logout/", views.logout_view, name="logout"),
    path("signup/", views.signup_page, name="signup"),
    path("feed/", views.feed, name="feed"),
    path("posts/", views.posts, name="posts"),
    path("follow-users/", views.follow_users, name="follow-users"),
    path("unfollow/<int:user_id>/", views.unfollow_user, name="unfollow"),
    path("block/<int:user_id>/", views.block_user, name="block"),
    path("unblock/<int:user_id>/", views.unblock_user, name="unblock"),
    path("ticket/create/", views.ticket_create, name="ticket-create"),
    path("ticket/<int:ticket_id>/edit/", views.ticket_edit, name="ticket-edit"),
    path("ticket/<int:ticket_id>/delete/", views.ticket_delete, name="ticket-delete"),
    path("review/create/", views.review_create, name="review-create"),
    path("review/create/<int:ticket_id>/", views.review_create, name="review-create"),
    path("review/<int:review_id>/edit/", views.review_edit, name="review-edit"),
    path("review/<int:review_id>/delete/", views.review_delete, name="review-delete"),
]
