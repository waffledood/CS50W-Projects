from django.urls import path

from . import views

urlpatterns = [
    # API Routes
    path("", views.index, name="index"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("register", views.register, name="register"),
    path("user/<int:id>", views.user, name="user"),
    path("users", views.users, name="users"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("listings", views.listings, name="listings"),
    path("createListing", views.createListing, name="createListing"),
    path("booking/<int:id>", views.booking, name="booking"),
    path("bookings", views.bookings, name="bookings"),
    path("createBooking", views.createBooking, name="createBooking")
]
