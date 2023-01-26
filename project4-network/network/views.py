import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.db.models import Subquery
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse

from .models import User, Follower, Tweet


def index(request):
    
    # Retrieve all Tweets
    tweets = Tweet.objects.all()

    # Return emails in reverse chronologial order
    tweets = tweets.order_by("-date").all()

    paginator = Paginator(tweets, 10) # Show 10 tweets per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        'page_obj': page_obj,
        'numPages': paginator.page_range
    })


@login_required
def following(request):

    # Retrieve all users followed by current user
    usersFollowedByCurrentUser = Follower.objects.all().filter(user=request.user.id)

    # Retrieve all Tweets
    tweets = Tweet.objects.all().filter(user_id__in=Subquery(usersFollowedByCurrentUser.values('userFollowing')))

    # Return emails in reverse chronologial order
    tweets = tweets.order_by("-date").all()

    paginator = Paginator(tweets, 10) # Show 10 tweets per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        'page_obj': page_obj,
        'numPages': paginator.page_range
    })


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

@login_required
def editTweet(request, id):
    # Retrieve Tweet with specified id
    tweetQuerySet = Tweet.objects.filter(id=id)
    tweet = tweetQuerySet.first()

    # Only a user can edit their own tweet
    if request.user != tweet.user:
        return JsonResponse({"error": "Only a user can edit their own tweet."}, status=400)
    
    # Editing a tweet must be via PATCH
    if request.method != "PATCH":
        return JsonResponse({"error": "PATCH request required."}, status=400)

    # Load data from request body
    data = json.loads(request.body)

    editedTweetContent = data.get("editedTweetContent")
    if editedTweetContent == "":
        return JsonResponse({
            "error": "Edited tweet is missing content."
        }, status=400)

    # update Tweet with edited content
    tweetQuerySet.update(content=editedTweetContent)

    return JsonResponse({"message": "Tweet edited successfully."}, status=201)

@login_required
def likeTweet(request):

def profile(request, username):

    # retrieve User object
    user = User.objects.all().get(username=username)

    # retrieve users following & followed by user
    following = Follower.objects.all().filter(user=user.id)
    followers = Follower.objects.all().filter(userFollowing=user.id)

    # retrieve user's tweets
    tweets = Tweet.objects.all().filter(user=user)

    # check if current user is following this user
    isFollowingUser = True if request.user in followers else False
    
    return render(request, "network/profile.html", {
        'profile': user,
        'following': following,
        'followers': followers,
        'tweets': tweets,
        'isFollowingUser': isFollowingUser
    })
