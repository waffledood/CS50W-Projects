from django import forms
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Comment, Bid


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
        return render(request, "auctions/register.html")


def create(request):
    if request.method == "POST":
        form = NewListingForm(request.POST)
        if form.is_valid():
            # retrieve the form's data
            name = form.cleaned_data["name"]
            price = form.cleaned_data["price"]
            description = form.cleaned_data["description"]
            # create & save the Listing object
            listing = Listing(name=name, price=price, user=request.user, description=description)
            listing.save()
        else:
            return render(request, "auctions/create.html", {
                'form': form
            })
    
    return render(request, "auctions/create.html", {
        'form': NewListingForm()
    })


def listing(request, listId):
    listing = Listing.objects.get(pk=listId)
    # get the list of Comments for the Listing
    try:
        comments = Comment.objects.filter(listing=listId)
    except ObjectDoesNotExist:
        comments = None
    # get the list of Bids for the Listing
    try:
        bids = Bid.objects.filter(listing=listId)
    except ObjectDoesNotExist:
        bids = None

    if request.method == "POST":
        # if the POST request is for a bid
        if "bid" in request.POST:
            form = NewBidForm(data=request.POST, listingPrice=listing.price)
            if form.is_valid():
                # retrieve the form's data
                bid = form.cleaned_data["bid"]
                newBid = Bid(bidder=request.user, listing=listing, price=bid)
                newBid.save()
                return HttpResponseRedirect(reverse('listing', kwargs={'listId':listId}))
            # return the same page, with the incorrect form
            return render(request, "auctions/listing.html", {
                'form': form,
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
                'form': NewBidForm(listingPrice=listing.price),
                'comments': comments,
                'commentForm': commentForm
            })
        
    return render(request, "auctions/listing.html", {
        'listing': listing,
        'bids': bids,
        'form': NewBidForm(listingPrice=listing.price),
        'comments': comments,
        'commentForm': NewCommentForm()
    })

