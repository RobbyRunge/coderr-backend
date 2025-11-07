from django.contrib import admin
from .models import Offer, OfferDetail


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'user', 'created_at', 'updated_at')


@admin.register(OfferDetail)
class OfferDetailAdmin(admin.ModelAdmin):
    list_display = ('title', 'offer', 'price', 'delivery_time_in_days', 'id')
