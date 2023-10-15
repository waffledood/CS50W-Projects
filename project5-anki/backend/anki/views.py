import json
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Collection, Card

from .exceptions import StringLengthTooLongError

from .utils import check_string_length

from varname import nameof


@login_required
def index(request):
    # Retrieve existing Collections
    collections = list(Collection.objects.all())

    return render(request, "anki/index.html", {"collections": collections})


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
                username=username, email=email, password=password
            )
            user.save()
        except IntegrityError:
            return JsonResponse(
                {"error": "An account with similar username or email already exists!"},
                status=400,
            )

        # log the user in, after successful creation
        login(request, user)

        return JsonResponse(
            {"message": "New user registered successfully", "user": user.serialize()},
            status=200,
        )
    else:
        return render(request, "anki/register.html")


def login(request):
    if request.method == "POST":
        # Retrieve login details
        username = request.POST["username"]
        password = request.POST["password"]
        # Verify user's credentials
        user = authenticate(request, username=username, password=password)

        # Check if authentication failed
        if user is None:
            return render(
                request, "anki/login.html", {"error": "Credentials are invalid."}
            )
        # If authentication is successful, log user in
        else:
            auth_login(request, user)
            return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "anki/login.html")


def logout(request):
    if request.method == "POST":
        logout(request)
        return JsonResponse(
            {"message": "Logged out successfully", "user": request.user.serialize()},
            status=200,
        )
    else:
        return JsonResponse({"error": "POST request required."}, status=400)


def viewCollection(request, collectionId):
    return render(request, "anki/collection.html", {"collectionId": collectionId})


def addCollection(request):
    return render(request, "anki/addCollection.html", {})


# API endpoints


def user(request, userId):
    if request.method == "GET":
        # Return an error if the id doesn't exist in the database
        try:
            user = User.objects.get(id=userId)
        except User.DoesNotExist:
            return JsonResponse({"error": "User id does not exist."}, status=400)

        # Retrieve User with specified id
        return JsonResponse(user.serialize(), status=200)

    if request.method == "DELETE":
        # Return an error if the id doesn't exist in the database
        try:
            user = User.objects.get(id=userId)
        except User.DoesNotExist:
            return JsonResponse({"error": "User id does not exist."}, status=400)

        # Delete User with specified id
        user.delete()
        return JsonResponse({"message": "User deleted successfully"}, status=201)

    return JsonResponse(
        {"error": "Only GET & DELETE requests are allowed."}, status=400
    )


def users(request):
    if request.method == "GET":
        # Retrieve all users
        users = User.objects.all()

        return JsonResponse(
            [user.serialize() for user in users], safe=False, status=200
        )

    return JsonResponse({"error": "Only GET requests are allowed."}, status=400)


@csrf_exempt
def collection(request, collectionId):
    if request.method == "GET":
        # Return an error if the id doesn't exist in the database
        try:
            # Retrieve Collection with specified id
            collection = Collection.objects.get(id=collectionId)
        except Collection.DoesNotExist:
            return JsonResponse({"error": "Collection id does not exist."}, status=400)

        #  Retrieve Collection with specified id
        return JsonResponse(collection.serialize(), safe=False)

    if request.method == "DELETE":
        # Return an error if the id doesn't exist in the database
        try:
            collection = Collection.objects.get(id=collectionId)
        except Collection.DoesNotExist:
            return JsonResponse({"error": "Collection id does not exist."}, status=400)

        # Delete Collection with specified id
        collection.delete()
        return JsonResponse({"message": "Collection deleted successfully"}, status=201)

    return JsonResponse(
        {"error": "Only GET & DELETE requests are allowed."}, status=400
    )


def collections(request):
    if request.method == "GET":
        # Retrieve all Collections that exist
        collections = Collection.objects.all()

        return JsonResponse(
            [collection.serialize() for collection in collections],
            safe=False,
            status=200,
        )

    return JsonResponse({"error": "Only GET requests are allowed."}, status=400)


@csrf_exempt
def createCollection(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Load JSON from request.body as a dict
    data = json.loads(request.body)

    # Retrieve Collection details
    user = request.user
    name = data.get("name")
    description = data.get("description")

    # Check for & return missing Collection details, if any
    collectionDetails = [(name, "name"), (description, "description")]
    missingCollectionDetails = []

    for collectionDetailValue, collectionDetailVarName in collectionDetails:
        if collectionDetailValue == None:
            missingCollectionDetails.append(collectionDetailVarName)

    if missingCollectionDetails:
        return JsonResponse(
            {
                "error": "Created Collection is missing details",
                "missingDetails": missingCollectionDetails,
            },
            status=400,
        )

    # Validate Collection details
    try:
        # if name is an empty String '', raise an Error
        if not name:
            raise ValueError("Collection Name is empty")
        # if name is not a String, raise an Error
        if type(name) is not str:
            raise TypeError("Collection Name is not a String")
        # if name is longer than 64 characters, raise an Error
        check_string_length(
            variable=name, max_length=Collection._meta.get_field("name").max_length
        )

        # if description is an empty String '', raise an Error
        if not description:
            raise ValueError("Collection Description is empty")
        # if description is not a String, raise an Error
        if type(description) is not str:
            raise TypeError("Collection Description is not a String")
        # if description is longer than 128 characters, raise an Error
        check_string_length(
            variable=name,
            max_length=Collection._meta.get_field("description").max_length,
        )
    except (ValueError, TypeError, StringLengthTooLongError) as e:
        return JsonResponse({"error": f"{e}"}, status=400)

    # Create & save Collection object
    Collection = Collection(user=user, name=name, description=description)
    collection.save()

    return JsonResponse(
        {
            "message": "Collection saved successfully.",
            "collection": collection.serialize(),
        },
        status=201,
    )


@csrf_exempt
def card(request, cardId):
    if request.method == "GET":
        # Return an error if the id doesn't exist in the database
        try:
            card = Card.objects.get(id=cardId)
        except Card.DoesNotExist:
            return JsonResponse({"error": "Card id does not exist"}, status=400)

        return JsonResponse(card.serialize(), status=201)

    if request.method == "DELETE":
        # Return an error if the id doesn't exist in the database
        try:
            card = Card.objects.get(id=cardId)
        except Card.DoesNotExist:
            return JsonResponse({"error": "Card id does not exist"}, status=400)

        # delete the Card
        card.delete()
        return JsonResponse({"message": "Card deleted successfully"}, status=201)

    return JsonResponse(
        {"error": "Only GET & DELETE requests are allowed."}, status=400
    )


def cards(request):
    if request.method == "GET":
        # Retrieve all Cards that exist
        cards = Card.objects.all()

        return JsonResponse(
            [card.serialize() for card in cards], safe=False, status=200
        )

    return JsonResponse({"error": "Only GET requests are allowed."}, status=400)


def cardsOfCollection(request, collectionId):
    if request.method == "GET":
        # Retrieve all Cards that exist
        collection = Collection.objects.get(id=collectionId)
        cards = collection.cards.all()

        return JsonResponse(
            [card.serialize() for card in cards], safe=False, status=200
        )

    return JsonResponse({"error": "Only GET requests are allowed."}, status=400)


@csrf_exempt
def createCard(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Load JSON from request.body as a dict
    data = json.loads(request.body)

    # Retrieve Card details
    user = request.user
    collection_id = data.get("collection_id")
    question = data.get("question")
    answer = data.get("answer")

    # Validate request is coming from a User
    if not isinstance(user, User):
        return JsonResponse({"error": "User is not a valid User"}, status=400)

    # Validate User making request exists
    try:
        User.objects.get(id=user.id)
    except User.DoesNotExist:
        return JsonResponse({"error": "User doesn't exist in the database"}, status=400)

    # Check for & return missing Card details, if any
    cardDetails = [
        (collection_id, "collection_id"),
        (question, "question"),
        (answer, "answer"),
    ]
    missingCardDetails = []

    for cardDetailValue, cardDetailVarName in cardDetails:
        if cardDetailValue == None:
            missingCardDetails.append(cardDetailVarName)

    if missingCardDetails:
        return JsonResponse(
            {
                "error": "Created Card is missing details",
                "missingDetails": missingCardDetails,
            },
            status=400,
        )

    # Validate Card details
    try:
        collection = Collection.objects.get(id=collection_id)
        if not question:
            raise ValueError("question variable is empty")
        if not answer:
            raise ValueError("answer variable is empty")
    except Collection.DoesNotExist:
        return JsonResponse({"error": "Collection id does not exist"}, status=400)
    except ValueError as e:
        return JsonResponse({"error": f"{e}"}, status=400)

    # Create & save Card object
    card = Card(user=user, collection=collection, question=question, answer=answer)
    card.save()

    return JsonResponse(
        {"message": "Card saved successfully", "card": card.serialize()}, status=200
    )
