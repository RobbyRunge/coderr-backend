from django.conf import settings
from django.db import models


class Review(models.Model):
    business_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='business_reviews', on_delete=models.CASCADE
    )
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='given_reviews', on_delete=models.CASCADE
    )
    rating = models.IntegerField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f'Review by {self.reviewer} for {self.business_user} - Rating: {self.rating}'
