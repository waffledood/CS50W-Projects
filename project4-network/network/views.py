import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse

from .models import User, Tweet


def index(request):
    return render(request, "network/index.html")


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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required
def tweet(request):

    # Composing a new email must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Load Tweet JSON from request body
    data = json.loads(request.body)

    # Check Tweet content
    tweetContent = data.get("tweetContent")
    if tweetContent == "":
        return JsonResponse({
            "error": "Tweet is missing content."
        }, status=400)

    # Save Tweet
    tweet = Tweet(
        user=request.user,
        content=tweetContent
    )
    tweet.save()

    print(tweet)

    return JsonResponse({"message": "Tweet sent successfully."}, status=201)

def tweets(request):

    # Retrieve all Tweets
    tweets = Tweet.objects.all()

    # Return emails in reverse chronologial order
    tweets = tweets.order_by("-date").all()

    return JsonResponse([tweet.serialize() for tweet in tweets], safe=False)
