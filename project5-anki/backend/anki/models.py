from django.db import models


class Card(models.Model):
    collection_id = models.ForeignKey(
        to=Collection, on_delete=models.CASCADE, related_name="cards")
    question = models.CharField(max_length=400)
    answer = models.CharField(max_length=400)
