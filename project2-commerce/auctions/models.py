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

