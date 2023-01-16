from django.contrib import admin

from .models import User, Follower, Tweet

# Register your models here.
admin.site.register(User)
admin.site.register(Follower)
admin.site.register(Tweet)
