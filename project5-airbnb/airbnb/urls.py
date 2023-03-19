from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),

    # API Routes
    path("listing/<int:id>", views.listing, name="listing"),
    path("listings", views.listings, name="listings"),
]