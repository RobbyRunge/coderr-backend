from rest_framework import serializers

from offers_app.models import Offer


class OfferSerializer(serializers.ModelSerializer):
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    user_details = serializers.SerializerMethodField()
    details = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = [
            'id', 'title', 'description',
            'price', 'created_at', 'updated_at',
            'min_price', 'min_delivery_time', 'user_details',
            'details'
        ]

    def get_min_price(self, obj):
        return obj.price

    def get_min_delivery_time(self, obj):
        return obj.delivery_time

    def get_user_details(self, obj):
        return {
            "first_name": getattr(obj.user, "first_name", ""),
            "last_name": getattr(obj.user, "last_name", ""),
            "username": getattr(obj.user, "username", ""),
        }

    def get_details(self, obj):
        return f"{obj.title} - {obj.description}"
