import json
from varname import nameof
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
    listings = listings.order_by("-rating").all()

    return JsonResponse([listing.serialize() for listing in listings], safe=False)

def createListing(request):
    # Creating a new Listing must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Load Listing JSON from request body
    data = json.loads(request.body)

    # Retrieve Listing details
    name = data.get("name")
    description = data.get("description")
    rating = data.get("rating")
    price_nightly = data.get("price_nightly")

    # Check for empty Listing details
    listingDetails = [name, description, rating, price_nightly]
    missingListingDetails = []

    for detail in listingDetails:
        if detail == "":
            missingListingDetails.append(nameof(detail))

    # Return error detailing missing Listing details
    if not missingListingDetails:
        return JsonResponse({
            "error": "Created Listing is missing details.",
            "missingDetails": listingDetails
        }, status=400)

    # Save Listing
    listing = Listing(
        name=name,
        description=description,
        rating=rating,
        price_nightly=price_nightly,
        owner=request.user
    )
    listing.save()

    return JsonResponse({"message": "Listing created successfully.", "listing": listing.serialize()}, status=201)
