from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Review(models.Model):
    """
    Model representing a review given by a customer to a business user.
    """
    business_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='business_reviews', on_delete=models.CASCADE
    )
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='given_reviews', on_delete=models.CASCADE
    )
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f'Review by {self.reviewer} for {self.business_user} - Rating: {self.rating}'
