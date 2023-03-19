from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from .models import Listing


def index(request):
    return HttpResponse("Hello, world!")

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

