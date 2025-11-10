from django.db import models
from django.conf import settings


class Order(models.Model):
    """
    Model representing an order in the system.
    """
    customer_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='customer_orders', on_delete=models.CASCADE)
    business_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='business_orders', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    revisions = models.IntegerField()
    delivery_time_in_days = models.IntegerField()
    price = models.IntegerField()
    features = models.JSONField(default=list)
    offer_type = models.CharField(max_length=20)
    status = models.CharField(max_length=20, default='in_progress')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
