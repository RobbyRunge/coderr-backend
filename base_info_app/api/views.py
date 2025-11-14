from django.db import models

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from reviews_app.models import Review
from profiles_app.models import Profile as BusinessProfile
from offers_app.models import Offer


class BaseInfoAPIView(APIView):
    """
    Provides base information about reviews, business profiles, and offers.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        review_count = Review.objects.count()
        average_rating = (
            round(Review.objects.aggregate(avg=models.Avg('rating'))['avg'] or 0, 1)
            if review_count > 0 else 0
        )
        business_profile_count = BusinessProfile.objects.filter(
            user__user_type='business'
        ).count()
        offer_count = Offer.objects.count()
        return Response({
            "review_count": review_count,
            "average_rating": average_rating,
            "business_profile_count": business_profile_count,
            "offer_count": offer_count
        })
