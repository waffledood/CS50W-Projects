from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tweets")
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return f"Tweet ({self.id}): { self.content[:10] + '...' if len(self.content) >= 10 else self.content } by {self.user}"

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "date": self.date.strftime("%b %d %Y, %I:%M %p"),
            "likes": self.likes
        }
