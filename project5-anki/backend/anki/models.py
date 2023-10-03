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
            "date_joined": self.date_joined,
        }


class Collection(models.Model):
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="collections"
    )
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=128)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Collection ({self.id}), by User ({self.user_id}), name: {self.name}, description: {self.description}, date_created: {self.date_created}, date_modified: {self.date_modified}"

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "description": self.description,
            "date_created": self.date_created,
            "date_modified": self.date_modified,
        }


class Card(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="cards")
    collection = models.ForeignKey(
        to=Collection, on_delete=models.CASCADE, related_name="cards"
    )
    question = models.CharField(max_length=400)
    answer = models.CharField(max_length=400)

    def __self__(self):
        return f"Card ({self.id}), of Collection({self.collection_id}), question: {self.question}, answer: {self.answer}"

    def serialize(self):
        return {
            "id": self.id,
            "collection_id": self.collection_id,
            "question": self.question,
            "answer": self.answer,
        }
