from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    location = models.CharField(max_length=64)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] 
    # REQUIRED_FIELDS = a list of fields that will be prompted for when creating user via createsuperuser command

    objects = UserManager()

class Listing(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    price_nightly = models.DecimalField(max_digits=5, decimal_places=0)
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    
    def __str__(self):
        return f"Listing ({self.id}): {self.name}, {self.rating} stars, ${self.price_nightly}"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "rating": self.rating,
            "price_nightly": self.price_nightly,
            "owner_id": self.owner.id
        }

class Booking(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listings")

    def __str__(self):
        return f"Booking ({self.id}): {self.start_date} -- {self.end_date} by User {self.user.id} for Listing {self.listing.id}"
    
    def serialize(self):
        return {
            "id": self.id,
            "start_date": self.start_date.strftime('%Y-%m-%d'),
            "end_date": self.end_date.strftime('%Y-%m-%d'),
            "user_id": self.user.id,
            "listing_id": self.user.listing.id,
        }
