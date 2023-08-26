import json
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import User, Collection, Card

from varname import nameof


@login_required
def index(request):
    return render(request, "anki/index.html")


def register(request):
    if request.method == "POST":
        # Retrieve registration details
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        # Ensure password matches confirmation
        if password != confirmation:
            return JsonResponse({"error": "Passwords must match"}, status=400)

        # Attempt to create new user
        try:
            user = User.objects.create_user(
                username=username, email=email, password=password)
            user.save()
        except IntegrityError:
            return JsonResponse({"error": "An account with similar username or email already exists!"}, status=400)

        # log the user in, after successful creation
        login(request, user)

        return JsonResponse({"message": "New user registered successfully", "user": user.serialize()}, status=200)
    else:
        return render(request, "anki/register.html")


def login(request):
    if request.method == "POST":

        # Verify user's credentials
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication failed
        if user is None:
            return JsonResponse({"error": "Invalid username and/or password."}, status=400)
        # If authentication is successful, log user in
        else:
            auth_login(request, user)
            return JsonResponse({"message": "Logged in successfully", "user": user.serialize()}, status=200)
    else:
        return render(request, "anki/login.html")


def logout(request):
    if request.method == "POST":
        logout(request)
        return JsonResponse({"message": "Logged out successfully", "user": request.user.serialize()}, status=200)
    else:
        return JsonResponse({"error": "POST request required."}, status=400)


def user(request, id):
    if request.method == "GET":
        # Return an error if the id doesn't exist in the database
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return JsonResponse({"error": "User id does not exist."}, status=400)

        # Retrieve User with specified id
        return JsonResponse([user.serialize()], safe=False)

    if request.method == "DELETE":
        # Return an error if the id doesn't exist in the database
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return JsonResponse({"error": "User id does not exist."}, status=400)

        # Delete User with specified id
        user.delete()
        return JsonResponse({"message": "User deleted successfully"}, status=201)

    return JsonResponse({"error": "Only GET & DELETE requests are allowed."}, status=400)


def users(request):
    if request.method == "GET":
        # Retrieve all users
        users = User.objects.all()

        return JsonResponse({"users": [user.serialize() for user in users]}, status=200)

    return JsonResponse({"error": "Only GET requests are allowed."}, status=400)


def collection(request, id):
    if request.method == "GET":
        # Return an error if the id doesn't exist in the database
        try:
            # Retrieve Collection with specified id
            collection = Collection.objects.get(id)
        except Collection.DoesNotExist:
            return JsonResponse({"error": "Collection id does not exist."}, status=400)

        #  Retrieve Collection with specified id
        return JsonResponse([collection.serialize()], safe=False)

    if request.method == "DELETE":
        # Return an error if the id doesn't exist in the database
        try:
            collection = Collection.objects.get(id=id)
        except Collection.DoesNotExist:
            return JsonResponse({"error": "Collection id does not exist."}, status=400)

        # Delete Collection with specified id
        collection.delete()
        return JsonResponse({"message": "Collection deleted successfully"}, status=201)

    return JsonResponse({"error": "Only GET & DELETE requests are allowed."}, status=400)


def collections(request):
    if request.method == "GET":
        # Retrieve all Collections that exist
        collections = Collection.objects.all()

        return JsonResponse({"collections": [collection.serialize() for collection in collections]}, status=200)

    return JsonResponse({"error": "Only GET requests are allowed."}, status=400)


@csrf_exempt
def createCollection(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Load JSON from request body
    data = json.loads(request.body)

    # Retrieve Collection details
    user = request.user
    name = data.get("name")
    description = data.get("description")

    # Check for & return missing Collection details, if any
    collectionDetails = [name, description]
    missingCollectionDetails = []

    for detail in collectionDetails:
        if detail == None:
            missingCollectionDetails.append(nameof(detail))

    if not missingCollectionDetails:
        return JsonResponse({
            "error": "Created Collection is missing details",
            "missingDetails": missingCollectionDetails
        }, status=400)

    # Validate Collection details
    try:
        # if name is empty, raise an Error
        if not name:
            raise ValueError("name variable is empty")
        # if description is empty, raise an Error
        if not description:
            raise ValueError("description variable is empty")
    except ValueError as e:
        return JsonResponse({"error": f"{e}"}, status=400)

    # Create & save Collection object
    Collection = Collection(
        user=user,
        name=name,
        description=description
    )
    collection.save()

    return JsonResponse({"message": "Collection saved successfully.", "collection": collection.serialize()}, status=201)


def card(request, id):
    if request.method == "GET":
        # Return an error if the id doesn't exist in the database
        try:
            card = Card.objects.get(id=id)
        except Card.DoesNotExist:
            return JsonResponse({"error": "Card id does not exist"}, status=400)

        return JsonResponse({"user": card.serialize()}, status=201)

    if request.method == "DELETE":
        # Return an error if the id doesn't exist in the database
        try:
            card = Card.objects.get(id=id)
        except Card.DoesNotExist:
            return JsonResponse({"error": "Card id does not exist"}, status=400)

        # delete the Card
        card.delete()
        return JsonResponse({"message": "Card deleted successfully"}, status=201)

    return JsonResponse({"error": "Only GET & DELETE requests are allowed."}, status=400)


def cards(request):
    if request.method == "GET":
        # Retrieve all Cards that exist
        cards = Card.objects.all()

        return JsonResponse({"cards": [card.serialize() for card in cards]}, status=200)

    return JsonResponse({"error": "Only GET requests are allowed."}, status=400)


@csrf_exempt
def createCard(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Load JSON from request.body
    data = json.loads(request.body)

    # Retrieve Card details
    user = request.user
    collection_id = data["collection_id"]
    question = data["question"]
    answer = data["answer"]

    # Check for & return missing Card details, if any
    cardDetails = [collection_id, question, answer]
    missingCardDetails = []

    for detail in cardDetails:
        if detail == None:
            missingCardDetails.append(nameof(detail))

    if not missingCardDetails:
        return JsonResponse({
            "error": "Created Card is missing details",
            "missingDetails": missingCardDetails
        }, status=400)

    # Validate Card details
    try:
        collection = Collection.objects.get(collection_id)
        if not question:
            raise ValueError("question variable is empty")
        if not answer:
            raise ValueError("answer variable is empty")
    except Collection.DoesNotExist:
        return JsonResponse({"error": "Collection id does not exist"}, status=400)
    except ValueError as e:
        return JsonResponse({"error": f"{e}"}, status=400)

    # Create & save Card object
    card = Card(
        user=user,
        collection=collection,
        question=question,
        answer=answer
    )
    card.save()

    return JsonResponse({"message": "Card saved successfully", "card": card.serialize()}, status=200)
