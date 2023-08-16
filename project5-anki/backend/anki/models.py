from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from .managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=64, unique=True)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    email = models.EmailField(unique=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.username}, {self.email}"

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "last_login": self.last_login,
            "is_staff": self.is_staff,
            "is_active": self.is_active,
            "date_joined": self.date_joined
        }


class Collection(models.Model):
    user_id = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="collections")
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=128)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)


class Card(models.Model):
    collection_id = models.ForeignKey(
        to=Collection, on_delete=models.CASCADE, related_name="cards")
    question = models.CharField(max_length=400)
    answer = models.CharField(max_length=400)
