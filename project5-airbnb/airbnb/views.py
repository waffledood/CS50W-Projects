from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from .models import Listing, User


def index(request):
    return HttpResponse("Hello, world!")

def user(request, id):
    # Retrieve User with specified id
    user = User.objects.get(id=id)

    return JsonResponse([user.serialize()], safe=False)

def users(request):
    # Retrieve all users
    users = User.objects.all()

    return JsonResponse([user.serialize() for user in users], safe=False)

def listing(request, id):
    #  Retrieve Listing with specified id
    listing = Listing.objects.get(id=id)

    return JsonResponse([listing.serialize()], safe=False)

def listings(request):
    # Retrieve all listings
    listings = Listing.objects.all()

    # Order listings by ratings
    listings.order_by("-rating").all()

    return JsonResponse([listing.serialize() for listing in listings], safe=False)

