from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Comment, Bid, Watchlist, Category

from . import util


class NewUserForm(forms.Form):
    username = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Username'
            }
        )
    )
    firstName = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={
                'placeholder': 'First Name'
            }
        )
    )
    lastName = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Last Name'
            }
        )
    )
    email = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Email'
            }
        )
    )
    password = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password'
            }
        )
    )
    passwordAgain = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Confirm Password'
            }
        )
    )


class NewListingForm(forms.Form):
    name = forms.CharField(
        label="Name of Listing:",
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter the name for your new listing...',
                'class': 'form-control w-75 mb-2'
            }
        )
    )

    price = forms.FloatField(
        label="Price of Listing:",
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control w-75 mb-2',
                'step': '0.01',
                'min': '0.0',
                'max': '100_000.0'
            }
        )
    )

    description = forms.CharField(
        label="Description of Listing:",
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Enter the description for your new listing...',
                'class': 'form-control w-75 mb-2'
            }
        )
    )

    category = forms.ChoiceField(
        label="Category:",
        choices=[
            ('BT', 'Beauty'),
            ('AM', 'Automotive'),
            ('ER', 'Electronics'),
            ('KD', 'Kids'),
            ('BK', 'Books'),
            ('MS', 'Misc'),
        ],
        widget=forms.Select(
            attrs={
                'class': 'form-select mb-2'
            }
        )
    )


class NewBidForm(forms.Form):
    # bid = forms.FloatField(
    #     label="Enter your bid:",
    #     widget=forms.NumberInput(
    #         attrs={
    #             'placeholder': Listing.price + 1.0,
    #             'class': 'form-control w-75 mb-2'
    #         }
    #     )
    # )

    # def __init__(self,*args,**kwargs):
    #     self.listingPrice = kwargs.pop('listingPrice')
    #     super(NewBidForm,self).__init__(*args,**kwargs)
    #     self.fields['bid'].widget = forms.NumberInput(
    #         attrs={
    #             'placeholder': listingPrice + 1.0,
    #             'class': 'form-control w-75 mb-2'
    #         }
    #     )

    def __init__(self, *, listingPrice, **kwargs):
        super().__init__(**kwargs)
        self.fields['bid'].widget = forms.NumberInput(
            attrs={
                'placeholder': listingPrice + 1.0,
                'value': listingPrice + 1.0,
                'min': listingPrice + 1.0,
                'step': 0.01,
                'class': 'form-control w-25 mb-2'
            }
        )

    bid = forms.FloatField()


class NewCommentForm(forms.Form):
    commentDetails = forms.CharField(
        label="",
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Add a comment...',
                'rows': 2,
                'class': 'form-control w-25 mt-2 mb-2'
            }
        )
    )


def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        'listings': listings
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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html", {
            'userForm': NewUserForm()
        })


@login_required(login_url='/register')
def create(request):
    if request.method == "POST":
        form = NewListingForm(request.POST)
        if form.is_valid():
            # retrieve the form's data
            name = form.cleaned_data["name"]
            price = form.cleaned_data["price"]
            description = form.cleaned_data["description"]
            type = form.cleaned_data["category"]
            # create & save the Listing object
            listing = Listing(name=name, price=price, user=request.user, description=description)
            listing.save()
            # create & save the Watchlist object
            category = Category(type=type, listing=listing)
            category.save()
        else:
            return render(request, "auctions/create.html", {
                'form': form
            })
    
    return render(request, "auctions/create.html", {
        'form': NewListingForm()
    })


def listing(request, listId):
    try:
        listing = Listing.objects.get(pk=listId)
    except Listing.DoesNotExist:
        return render(request, "auctions/error.html")
    # check if the owner of the listing is the current user
    ownerOfListing = True if listing.user == request.user else False
    # get the list of Comments for the Listing
    try:
        comments = Comment.objects.filter(listing=listId)
    except ObjectDoesNotExist:
        comments = None
    # get the list of Bids for the Listing
    try:
        bids = Bid.objects.filter(listing=listId).order_by('-price')
    except ObjectDoesNotExist:
        bids = None
    # check if this listing is on the user's watchlist 
    listingWatchlistedByUser = True if request.user.is_authenticated and Watchlist.objects.filter(listing=listing).filter(user=request.user).exists() else False

    # get the highest Bid for the listing, if any
    highestBid = bids.order_by('-price').first().price if bids.exists() else listing.price

    # check if the current user is the highest bidder for the listing (if listing is closed)
    highestBidder = bids.order_by('-price').first().bidder if bids.exists() else None
    highestBidderIsCurrentUser = True if highestBidder == request.user and not listing.active and bids.exists() else False

    if request.method == "POST":
        # if the POST request is for a bid
        if "bid" in request.POST:
            bidForm = NewBidForm(data=request.POST, listingPrice=listing.price)
            if bidForm.is_valid():
                # retrieve the form's data
                bid = bidForm.cleaned_data["bid"]
                newBid = Bid(bidder=request.user, listing=listing, price=bid)
                newBid.save()
                return HttpResponseRedirect(reverse('listing', kwargs={'listId':listId}))
            # return the same page, with the incorrect form
            return render(request, "auctions/listing.html", {
                'bidForm': bidForm,
                'comments': comments,
                'commentForm': NewCommentForm()
            })
        # if the POST request is for a comment
        if "commentDetails" in request.POST:
            commentForm = NewCommentForm(data=request.POST)
            if commentForm.is_valid():
                # retrieve the form's data
                commentDetails = commentForm.cleaned_data["commentDetails"]
                newComment = Comment(user=request.user, description=commentDetails, listing=listing)
                newComment.save()
                return HttpResponseRedirect(reverse('listing', kwargs={'listId':listId}))
            # return the same page, with incorrect form
            return render(request, "auctions/listing.html", {
                'bidForm': NewBidForm(listingPrice=listing.price),
                'comments': comments,
                'commentForm': commentForm
            })
        # if the POST request is for adding listing to watchlist
        if "watchlist" in request.POST:
            # if the listing is already in the user's watchlist, remove it
            if listingWatchlistedByUser:
                Watchlist.objects.filter(listing=listing).filter(user=request.user).delete()
                return HttpResponseRedirect(reverse('listing', kwargs={'listId':listId}))
            # if the listing is not in the user's watchlist, add it
            else:
                watchlist = Watchlist(user=request.user, listing=listing)
                watchlist.save()
                return HttpResponseRedirect(reverse('listing', kwargs={'listId':listId}))
        # if the POST request is for closing the listing
        if "closeListing" in request.POST and ownerOfListing:
            listing.active = False
            listing.save()
            return HttpResponseRedirect(reverse('listing', kwargs={'listId': listId}))

    return render(request, "auctions/listing.html", {
        'listing': listing,
        'bids': bids,
        'highestBid': highestBid,
        'bidForm': NewBidForm(listingPrice=highestBid),
        'comments': comments,
        'commentForm': NewCommentForm(),
        'listingWatchlistedByUser': listingWatchlistedByUser,
        'ownerOfListing': ownerOfListing,
        'listingStatus': listing.active,
        'highestBidderIsCurrentUser': highestBidderIsCurrentUser
    })


@login_required(login_url='/register')
def watchlist(request):
    listings = Listing.objects.filter(watchlist__in=Watchlist.objects.filter(user=request.user))
    return render(request, "auctions/watchlist.html", {
        'watchlist': listings
    })


@login_required(login_url='/register')
def categories(request, category=None):
    if category != None and category not in util.CATEGORY_VALUES:
        return render(request, "auctions/error.html")
    if category in util.CATEGORY_VALUES:
        categories = Category.objects.filter(type=category)
        categoryListings = Listing.objects.filter(category__in=categories)
        return render(request, "auctions/categories.html", {
            'categoryListings': categoryListings,
            'categorySelected': util.getOption(category),
            'categories': util.CATEGORY_CHOICES
        })
    return render(request, "auctions/categories.html", {
        'categoryListings': Listing.objects.all(),
        'categorySelected': None,
        'categories': util.CATEGORY_CHOICES
    })

