from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from reviews_app.models import Review
from reviews_app.api.serializers import ReviewSerializer


class ReviewListCreateAPIView(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['business_user', 'reviewer']
    ordering_fields = ['updated_at', 'rating']
