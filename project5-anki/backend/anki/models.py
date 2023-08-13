from django.db import models


class Collection(models.Model):
    user_id = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="collections")
    name = models.CharField(max_length=64)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)


class Card(models.Model):
    collection_id = models.ForeignKey(
        to=Collection, on_delete=models.CASCADE, related_name="cards")
    question = models.CharField(max_length=400)
    answer = models.CharField(max_length=400)
