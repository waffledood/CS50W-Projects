from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register, name="register"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("collection/<int:collectionId>", views.viewCollection, name="viewCollection"),
    path("addCollection", views.addCollection, name="addCollection"),
    path("activeRecall/<int:collectionId>", views.activeRecall, name="activeRecall"),
    # API endpoints
    path("api/user/<int:userId>", views.user, name="user"),
    path("api/users", views.users, name="users"),
    path("api/collection/<int:collectionId>", views.collection, name="collection"),
    path("api/collections", views.collections, name="collections"),
    path("api/createCollection", views.createCollection, name="createCollection"),
    path("api/card/<int:cardId>", views.card, name="card"),
    path("api/cards", views.cards, name="cards"),
    path("api/cards/<int:collectionId>", views.cardsOfCollection, name="cards"),
    path("api/createCard", views.createCard, name="createCard"),
]
