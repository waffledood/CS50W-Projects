from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register, name="register"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("user", views.user, name="user"),
    path("users", views.users, name="users"),
    path("collection", views.collection, name="collection"),
    path("collections", views.collections, name="collections")
]
