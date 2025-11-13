from django.db import models


class Review(models.Model):
    rating = models.FloatField()


class BusinessProfile(models.Model):
    pass


class Offer(models.Model):
    pass
