
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("following", views.following, name="following"),

    # API Routes
    path("tweet", views.tweet, name="tweet"),
    path("tweets", views.tweets, name="tweets"),
    path("editTweet/<int:id>", views.editTweet, name="editTweet"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("likeTweet", views.likeTweet, name="likeTweet")
]
