from django.db import models


class Review(models.Model):
    """
    Represents a review with a rating.
    """
    rating = models.FloatField()


class BusinessProfile(models.Model):
    """
    Represents a business profile.
    """
    pass


class Offer(models.Model):
    """
    Represents an offer.
    """
    pass
