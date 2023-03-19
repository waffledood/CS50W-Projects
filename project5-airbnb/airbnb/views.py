import json
from varname import nameof
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from .models import Booking, Listing, User


def index(request):
    return HttpResponse("Hello, world!")


def user(request, id):
    if request.method == "GET":
        # Return an error if the id doesn't exist in the database
        try:
            User.objects.get(id=id)
        except User.DoesNotExist:
            return JsonResponse({"error": "User id does not exist."}, status=400)

        # Retrieve User with specified id
        user = User.objects.get(id=id)
        return JsonResponse([user.serialize()], safe=False)

    if request.method == "DELETE":
        # Return an error if the id doesn't exist in the database
        try:
            User.objects.get(id=id)
        except User.DoesNotExist:
            return JsonResponse({"error": "User id does not exist."}, status=400)

        # Delete User with specified id
        User.objects.get(id=id).delete()
        return JsonResponse({"message": "User deleted successfully"}, status=201)

    return JsonResponse({"error": "Only GET & DELETE requests are allowed."}, status=400)


def users(request):
    if request.method == "GET":
        # Retrieve all users
        users = User.objects.all()
        return JsonResponse([user.serialize() for user in users], safe=False)

    return JsonResponse({"error": "Only GET requests are allowed."}, status=400)


def listing(request, id):
    if request.method == "GET":
        # Return an error if the id doesn't exist in the database
        try:
            Listing.objects.get(id=id)
        except Listing.DoesNotExist:
            return JsonResponse({"error": "Listing id does not exist."}, status=400)

        #  Retrieve Listing with specified id
        listing = Listing.objects.get(id=id)
        return JsonResponse([listing.serialize()], safe=False)

    if request.method == "DELETE":
        # Return an error if the id doesn't exist in the database
        try:
            Listing.objects.get(id=id)
        except Listing.DoesNotExist:
            return JsonResponse({"error": "Listing id does not exist."}, status=400)

        # Delete Listing with specified id
        Listing.objects.get(id=id).delete()
        return JsonResponse({"message": "Listing deleted successfully"}, status=201)

    return JsonResponse({"error": "Only GET & DELETE requests are allowed."}, status=400)


def listings(request):
    if request.method == "GET":
        # Retrieve all listings
        listings = Listing.objects.all()

        # Order listings by ratings
        listings = listings.order_by("-rating").all()

        return JsonResponse([listing.serialize() for listing in listings], safe=False)

    return JsonResponse({"error": "Only GET requests are allowed."}, status=400)


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


def booking(request, id):
    if request.method == "GET":
        # Return an error if the id doesn't exist in the database
        try:
            # Retrieve Booking with specified id
            Booking.objects.get(id)
        except Booking.DoesNotExist:
            return JsonResponse({"error": "Booking id does not exist."}, status=400)

        #  Retrieve Booking with specified id
        booking = Booking.objects.get(id=id)
        return JsonResponse([booking.serialize()], safe=False)

    if request.method == "DELETE":
        # Return an error if the id doesn't exist in the database
        try:
            Booking.objects.get(id=id)
        except Booking.DoesNotExist:
            return JsonResponse({"error": "Booking id does not exist."}, status=400)

        # Delete Booking with specified id
        Booking.objects.get(id=id).delete()
        return JsonResponse({"message": "Booking deleted successfully"}, status=201)

    return JsonResponse({"error": "Only GET & DELETE requests are allowed."}, status=400)


def bookings(request):
    # Retrieve all bookings
    bookings = Booking.objects.all()

    return JsonResponse([booking.serialize() for booking in bookings], safe=False)
