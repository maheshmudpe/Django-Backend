from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import UserManager


class User(AbstractUser):
    # Remove Django's default username field
    username = None

    # Use email as the unique login identifier
    email = models.EmailField(unique=True)

    # Store the user's full name
    name = models.CharField(max_length=150)

    # Configure email-based authentication
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    # Attach our custom manager
    objects = UserManager()

    def __str__(self):
        return self.email