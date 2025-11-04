from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """
    Custom user model that extends Django's AbstractUser.
    Adds a 'user_type' field to distinguish between customers and business
    users.

    Fields inherited from AbstractUser:
        - username
        - email
        - password
        - first_name
        - last_name
        - etc.

    Additional fields:
        - user_type: 'customer' or 'business'
    """
    USER_TYPE_CHOICES = (
        ('customer', 'Customer'),
        ('business', 'Business'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
