from django.urls import path

from . import views

app_name = "wiki"

urlpatterns = [
    path("", views.index, name="index"),
    #path("error", views.error, name="error"),
    path("search", views.search, name="search"),
    path("newpage", views.newpage, name="newpage"),
    path("random", views.randomEntry, name="randomEntry"),
    path("<str:entry>/edit", views.edit, name="edit"),
    path("<str:entry>", views.entry, name="entry")
]
