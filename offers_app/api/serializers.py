from rest_framework import serializers
from offers_app.models import Offer, OfferDetail


class OfferDetailShortSerializer(serializers.ModelSerializer):
    """
    Serializer for offer detail representation in the offer list.
    """
    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = ['id', 'url']

    # Get the URL for the offer detail
    def get_url(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(f'/api/offerdetails/{obj.id}/')
        return f'/api/offerdetails/{obj.id}/'


class OfferDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and representing offer details.
    """
    class Meta:
        model = OfferDetail
        fields = [
            'id', 'title', 'revisions', 'delivery_time_in_days',
            'price', 'features', 'offer_type'
        ]


class OfferDetailResponseSerializer(serializers.ModelSerializer):
    """
    Serializer for representing offers with summary information.
    """
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    details = OfferDetailShortSerializer(many=True, read_only=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = [
            'id', 'user', 'title', 'image',
            'description', 'created_at', 'updated_at',
            'details', 'min_price', 'min_delivery_time',
        ]

    # Get the minimum price from the offer details
    def get_min_price(self, obj):
        prices = [detail.price for detail in obj.details.all()]
        return min(prices) if prices else None

    # Get the minimum delivery time from the offer details
    def get_min_delivery_time(self, obj):
        times = [detail.delivery_time_in_days for detail in obj.details.all()]
        return min(times) if times else None

    # Get user details associated with the offer
    def get_user_details(self, obj):
        user = obj.user
        profile = getattr(user, 'profile', None)
        if profile:
            return {
                "first_name": profile.first_name,
                "last_name": profile.last_name,
                "username": user.username
            }
        return {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username
        }


class OfferSerializer(serializers.ModelSerializer):
    """
    Serializer for representing offers with summary information.
    """
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    details = OfferDetailShortSerializer(many=True, read_only=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    user_details = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = [
            'id', 'user', 'title', 'image', 'description',
            'created_at', 'updated_at', 'details',
            'min_price', 'min_delivery_time', 'user_details'
        ]

    # Get the minimum price from the offer details
    def get_min_price(self, obj):
        prices = [detail.price for detail in obj.details.all()]
        return min(prices) if prices else None

    # Get the minimum delivery time from the offer details
    def get_min_delivery_time(self, obj):
        times = [detail.delivery_time_in_days for detail in obj.details.all()]
        return min(times) if times else None

    # Get user details associated with the offer
    def get_user_details(self, obj):
        user = obj.user
        profile = getattr(user, 'profile', None)
        if profile:
            return {
                "first_name": profile.first_name,
                "last_name": profile.last_name,
                "username": user.username
            }
        return {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username
        }


class OfferCreateSerializer(serializers.ModelSerializer):
    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = [
            'id', 'title', 'image', 'description', 'details'
        ]

    # Validate that at least three details are provided
    def validate_details(self, value):
        if len(value) < 3:
            raise serializers.ValidationError(
                "An offer must have at least three details.")
        return value

    # Create an offer along with its details
    def create(self, validated_data):
        details_data = validated_data.pop('details')
        user = self.context['request'].user
        offer = Offer.objects.create(user=user, **validated_data)
        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)
        return offer
