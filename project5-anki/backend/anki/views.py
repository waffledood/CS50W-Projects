import json
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import User


def index(request):
    # return HttpResponse(f"Hello World!")
    return render(request, "anki/index.html")


def register(request):
    if request.method == "POST":
        # Load JSON from request body
        data = json.loads(request.body)
        username = data.get("username")
        email = data.get("email")
        password = request.get("password")
        confirmation = request.get("confirmation")

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
        return JsonResponse({"error": "POST request required."}, status=400)


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
            login(request, user)
            return JsonResponse({"message": "Logged in successfully", "user": user.serialize()}, status=200)
    else:
        return JsonResponse({"error": "POST request required."}, status=400)


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
        return JsonResponse([user.serialize() for user in users], safe=False)

    return JsonResponse({"error": "Only GET requests are allowed."}, status=400)
