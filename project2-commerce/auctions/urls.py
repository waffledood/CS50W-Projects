from django.urls import path

from . import views

app_name = "auctions"

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categoriesMain", views.categoriesMain, name="categoriesMain"),
    path("categoriesIndv/<str:category>", views.categoriesIndv, name="categoriesIndv"),
    path("comment", views.comment, name="comment"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("createListing", views.createListing, name="createListing"),
    path("closeListing", views.closeListing, name="closeListing"),
    path("bid", views.bid, name="bid"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist_add", views.watchlist_add, name="watchlist_add"),
    path("watchlist_remove", views.watchlist_remove, name="watchlist_remove") 
]
