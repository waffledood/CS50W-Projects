from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register, name="register"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("user/<int:userId>", views.user, name="user"),
    path("users", views.users, name="users"),
    path("collection/<int:collectionId>", views.collection, name="collection"),
    path("collections", views.collections, name="collections"),
    path("createCollection", views.createCollection, name="createCollection"),
    path("card/<int:cardId>", views.card, name="card"),
    path("cards", views.cards, name="cards"),
    path("cards/<int:collectionId>", views.cardsOfCollection, name="cards"),
    path("createCard", views.createCard, name="createCard")
]
