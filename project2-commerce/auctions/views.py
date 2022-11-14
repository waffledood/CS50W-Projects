from django import forms
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

class NewListingForm(forms.Form):
    name = forms.CharField(
        label="Name of Listing:",
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter the name for your new listing...',
                'class': 'form-control w-75 mb-2'
            }
        )
    )

    price = forms.FloatField(
        label="Price of Listing:",
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control w-75 mb-2',
                'step': '0.01',
                'min': '0.0',
                'max': '100_000.0'
            }
        )
    )

    description = forms.CharField(
        label="Description of Listing:",
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Enter the description for your new listing...',
                'class': 'form-control w-75 mb-2'
            }
        )
    )


def index(request):
    return render(request, "auctions/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def create(request):
    pass
