from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    name = models.CharField(max_length=64)
    price = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    # image = models.ImageField()
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Listing ({self.id}): {self.name} of ${self.price}"

class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    price = models.FloatField()

    def __str__(self):
        return f"Bid ({self.id}): By {self.bidder.first_name} of ${self.price} for {self.listing.name}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    description = models.CharField(max_length=64)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f"{self.user.first_name}: {self.description}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="watchlist")

    def __str__(self):
        return f"id: {self.id}, user: {self.user}, listing: {self.listing}"

class Category(models.Model):
    BEAUTY = 'BT'
    AUTOMOTIVE = 'AM'
    ELECTRONICS = 'ER'
    KIDS = 'KD'
    BOOKS = 'BK'
    MISC = 'MS'
    CATEGORY_CHOICES = [
        (BEAUTY, 'Beauty'),
        (AUTOMOTIVE, 'Automotive'),
        (ELECTRONICS, 'Electronics'),
        (KIDS, 'Kids'),
        (BOOKS, 'Books'),
        (MISC, 'Misc'),
    ]
    year_in_school = models.CharField(
        max_length=2,
        choices=CATEGORY_CHOICES,
        default=MISC,
    )
    listing = models.ForeignKey(Listing, on_delete=models.SET_NULL, name="category", null=True)
