from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import widgets
from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator 

class User(AbstractUser):
    # check 0001_initial.py for other fields in User
    '''
    id, password, last_login, is_superuser, username, first_name, 
    last_name, email, is_staff, is_active, date_joined, groups, user_permissions
    '''
    country = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.username} ({self.id})"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    listing_id = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(100)])
    comment = models.TextField(max_length=None)

    @classmethod
    def create(cls, user, listing_id, comment):
        comment_item = cls(user=user, listing_id=listing_id, comment=comment)
        return comment_item

    def __str__(self):
        return f"{self.comment}"


class Auction(models.Model):
    BOOKS = 'Books'
    AUTOMOBILE = 'Automobile'
    TOYS = 'Toys'
    FOOD = 'Food'
    CLOTHING = 'Clothing'
    OTHERS = 'Others'
    CATEGORIES_CHOICES = [
        (BOOKS, 'Books'),
        (AUTOMOBILE, 'Automobile'),
        (TOYS, 'Toys'),
        (FOOD, 'Food'),
        (CLOTHING, 'Clothing'),
        (OTHERS, 'Others'),
    ]

    title = models.CharField(max_length=32)
    #description = models.CharField(widget=forms.Textarea)
    #description = forms.CharField(widget=forms.Textarea) # this doesn't work, description doesn't show up in the admin interface
    description = models.TextField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    #user_watchlist = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    watchlist = models.ManyToManyField(User, blank=True, related_name="watchlist")
    price = models.DecimalField(max_digits=5, decimal_places=2) # initial price
    bid = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    #bidder = models.ManyToManyField(User, blank=True, related_name="bidder")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings_bidded")
    picture = models.URLField()
    category = models.CharField(max_length=32, choices=CATEGORIES_CHOICES, default=OTHERS)
    active = models.BooleanField(default=True) # the status of the listing, if it's active or not 
    #comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="comment_made")
    #comment = models.ManyToManyField(Comment, blank=True, related_name="comment_made")

    @classmethod
    def create(cls, title, desc, user, price, url, cat):
        listing = cls(title=title, description=desc, user=user, price=price, picture=url, category=cat)
        return listing 


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    time = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid_time") # need to fix this because it's wrong (can check in admin interface to be sure)
