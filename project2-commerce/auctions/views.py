from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from django import forms

from django.contrib.auth.decorators import login_required

from .models import User, Auction, Comment, Bid

#userGlobal = None

class NewListing(forms.Form):
    title = forms.CharField(label="Auction Title")
    description = forms.CharField(label="Auction Description", widget=forms.Textarea)
    price = forms.IntegerField(min_value=0)
    picture = forms.URLField()
    #category = forms.CharField(max_length=32)
    #category = forms.ChoiceField(required=False, widget=forms.Select, choices=FAVORITE_COLORS_CHOICES)
    category = forms.ChoiceField(required=False, widget=forms.Select, choices=Auction.CATEGORIES_CHOICES)


class NewComment(forms.Form):
    comment = forms.CharField(widget=forms.Textarea)

def index(request):
    return render(request, "auctions/index.html", {
        "auctions": Auction.objects.all()
    })
# https://docs.djangoproject.com/en/3.0/topics/auth/default/#the-login-required-decorator


@login_required(login_url='/accounts/login/')
def createListing(request):
    if request.method == "POST":
        #listing = NewListing(request.POST)
        '''
        if listing.is_valid():
            title = listing.cleaned_data["title"]
            description = listing.cleaned_data["description"]
            price = listing.cleaned_data["price"]
            url = listing.cleaned_data["url"] '''
        if True:
            title = request.POST["title"]
            description = request.POST["description"]
            price = request.POST["price"]
            picture = request.POST["picture"]
            cat = request.POST["category"]

            #auction = Auction.objects.create(title, description, 1, price, cat)
            
            user = User.objects.get(pk=request.user.id)
            #user = User.objects.get(pk=userGlobal.id)

            auction = Auction.create(title, description, user, price, picture, cat)
            auction.save()

            # ref: these 2 links & also the example from the register view
            # https://docs.djangoproject.com/en/3.1/ref/models/instances/
            # https://www.informit.com/articles/article.aspx?p=1175564&seqNum=5 
            
            print("saved!")

            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/createListing.html", {
                "listing": listing
            })
    return render(request, "auctions/createListing.html", {
        "listing": NewListing()
    })


@login_required()
def comment(request):
    if request.method == "POST":
        comment_text = request.POST["comment"]
        id_user_listing = request.POST["user"]
        listing_id = request.POST["listingID"]

        user_bidding = request.user
        
        comment_by_bidder = Comment.create(user_bidding, listing_id, comment_text)
        comment_by_bidder.save()

        listing = Auction.objects.get(pk=listing_id)
        
        comments = Comment.objects.all()

        ls = [x for x in comments if x.listing_id == int(listing_id)]

        print(ls)

        return render(request, "auctions/listing.html", {
            "listing": listing,
            "in_watchlist": user_bidding in listing.watchlist.all(),
            "listing_owner": listing.user.id == request.user.id,
            "comment_form": NewComment(),
            "comments": ls
        })

        #return HttpResponseRedirect(reverse("auctions:index"))
    return render(request, "auctions/listing.html", {
        "comment_form": NewComment(),
        "bool": True
    })



@login_required(login_url='/accounts/login/')
def listing(request, listing_id):

    listing = Auction.objects.get(pk=listing_id)

    if request.user in listing.watchlist.all():
        in_watchlist = True
    else:
        in_watchlist = False 

    #print (in_watchlist, "ANSWER IS HEREEEE")
    print("Active:", listing.active)

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "in_watchlist": in_watchlist,
        "listing_owner": listing.user.id == request.user.id,
        "comment_form": NewComment()
    })


@login_required(login_url='/accounts/login/')
def closeListing(request):
    if request.method=="POST":
        id_user_listing = request.POST["user"]
        listing_id = request.POST["listingID"]
        close_listing = request.POST["close"]

        user_bidding = request.user

        '''
        print("close_listing:",close_listing)
        print("close_listing boolean check:",close_listing == "True")
        print("id boolean check:", id_user_listing == user_bidding.id)

        print("id of listing user:", id_user_listing, ", id of bidding user", user_bidding.id)

        print("listing: ", type(id_user_listing), ", bidding:", type(user_bidding.id))
        '''

        listing = Auction.objects.get(pk=listing_id)

        if int(id_user_listing) == user_bidding.id and bool(close_listing):
            listing.active = False
            listing.save() 
            
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "in_watchlist": user_bidding in listing.watchlist.all(),
                "listing_owner": listing.user.id == request.user.id
            })

    return HttpResponseRedirect(reverse("auctions:listing", args=(request.POST["listingID"],)))


@login_required(login_url='/accounts/login/')
def categoriesMain(request):
    return render(request, "auctions/categoriesMain.html", {
        "categories": Auction.CATEGORIES_CHOICES
    })

@login_required(login_url='/accounts/login/')
def categoriesIndv(request, category):
    listings = Auction.objects.all()

    relevantLisings = []

    for listing in listings:
        if listing.category == category:
            relevantLisings.append(listing)
    
    return render(request, "auctions/categoriesIndv.html", {
        "listings": relevantLisings,
        "category": category
    })

@login_required(login_url='/accounts/login/')
def bid(request):
    #pass
    if request.method=="POST":

        bid = request.POST["Bid"]
        user_listing_id = request.POST["user"]
        listing_id = request.POST["listingID"]

        user_bidding = request.user

        print("user of listing:", user_listing_id)
        print("user bidding:", user_bidding)

        listing = Auction.objects.get(pk=listing_id)

        if float(bid) >= listing.price and float(bid) > listing.bid:

            #user_listing = Auction.objects.get(pk=user_listing_id)
            listing.bid = float(bid)
            listing.bidder = user_bidding
            #user_listing.bidder.set(user_bidding) #issues
            listing.save()

            return HttpResponseRedirect(reverse("auctions:listing", args=(listing_id,)))

        else:
            return render(request, "auctions/listing.html", {
                "listing": Auction.objects.get(pk=listing_id),
                "in_watchlist": user_bidding in listing.watchlist.all(),
                "error": True
            })
            #return HttpResponseRedirect(reverse("auctions:listing", args=(listing_id,)))


@login_required(login_url='/accounts/login/')
def watchlist(request):

    user = request.user 
    
    watchlist = user.watchlist.all()

    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist
    })


@login_required(login_url='/accounts/login/')
def watchlist_add(request):
    #return render(request, "auctions/watchlist.html")
    if request.method=="POST":
        listing = Auction.objects.get(pk=request.POST["listingID"])

        print("***")
        print(request.POST)
        #print( int(request.POST["user"]) )

        user = request.user
        user = User.objects.get(pk=int(user.id))
        #user = User.objects.get(pk=int(request.POST["user"]))
        #user = User.objects.get(pk=int(request.POST.get("user")))
        user.watchlist.add(listing)
        #return HttpResponseRedirect(reverse("auctions:index"))
        return HttpResponseRedirect(reverse("auctions:listing", args=(request.POST["listingID"],)))

    else:
        return render(request, "auctions/watchlist.html")


@login_required(login_url='/accounts/login/')
def watchlist_remove(request):
    if request.method=="POST":
        listing = Auction.objects.get(pk=request.POST["listingID"])

        # https://docs.djangoproject.com/en/3.1/ref/models/relations/#django.db.models.fields.related.RelatedManager.remove

        user = request.user.id
        listing.watchlist.remove(user)
        return HttpResponseRedirect(reverse("auctions:listing", args=(request.POST["listingID"],)))
    else:
        return render(request, "auctions/watchlist.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        #userGlobal = user 

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


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
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")
