from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveAPIView
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import filters
from rest_framework.exceptions import ValidationError, PermissionDenied

from offers_app.api.permissions import IsBusinessUser
from offers_app.models import Offer, OfferDetail
from offers_app.api.serializers import (
    OfferCreateSerializer,
    OfferDetailFullSerializer,
    OfferListSerializer,
    OfferRetrieveSerializer,
    OfferUpdateSerializer
)
from offers_app.api.paginations import DynamicPageSizePagination


class OfferListView(ListCreateAPIView):
    """
    API view to list and create offers.
    """
    queryset = Offer.objects.all()
    serializer_class = OfferListSerializer
    permission_classes = [AllowAny, IsBusinessUser]
    pagination_class = DynamicPageSizePagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    search_fields = ['title', 'description']
    ordering_fields = [
        'id', 'price',
        'delivery_time', 'created_at',
        'updated_at']

    # Determine the serializer class based on the request method
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OfferCreateSerializer
        return OfferListSerializer

    # Apply filtering based on query parameters
    def get_queryset(self):
        queryset = super().get_queryset()
        creator_id = self.request.query_params.get('creator_id')
        min_price = self.request.query_params.get('min_price')
        max_delivery_time = self.request.query_params.get('max_delivery_time')

        if creator_id:
            try:
                creator_id = int(creator_id)
            except (TypeError, ValueError):
                raise ValidationError({'creator_id': 'Must be an integer.'})
            queryset = queryset.filter(user_id=creator_id)
        if min_price:
            try:
                min_price = float(min_price)
            except (TypeError, ValueError):
                raise ValidationError({'min_price': 'Must be a number.'})
            queryset = queryset.filter(details__price__gte=min_price)
        if max_delivery_time:
            try:
                max_delivery_time = int(max_delivery_time)
            except (TypeError, ValueError):
                raise ValidationError(
                    {'max_delivery_time': 'Must be an integer.'}
                )
            queryset = queryset.filter(
                details__delivery_time_in_days__lte=max_delivery_time
            )
        return queryset.distinct()


class OfferDetailView(RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve and update an offer.
    """
    queryset = Offer.objects.all()
    serializer_class = OfferUpdateSerializer
    permission_classes = [IsAuthenticated]

    # Determine the serializer class based on the request method
    def get_serializer_class(self):
        if self.request.method in ['PATCH', 'PUT']:
            return OfferUpdateSerializer
        return OfferRetrieveSerializer

    # Ensure only the owner can update the offer
    def update(self, request, *args, **kwargs):
        offer = self.get_object()
        if offer.user != request.user:
            raise PermissionDenied(
                "You do not have permission to edit this offer."
            )
        return super().update(request, *args, **kwargs)

    # Ensure only the owner can delete the offer
    def destroy(self, request, *args, **kwargs):
        offer = self.get_object()
        if offer.user != request.user:
            raise PermissionDenied(
                "You do not have permission to delete this offer."
            )
        return super().destroy(request, *args, **kwargs)


class OfferDetailFullRetrieveView(RetrieveAPIView):
    """
    API view to retrieve a specific offer detail.
    """
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailFullSerializer
    permission_classes = [IsAuthenticated]
