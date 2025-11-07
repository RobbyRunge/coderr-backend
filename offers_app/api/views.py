from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework import filters
from rest_framework.exceptions import ValidationError

from offers_app.api.permissions import IsBusinessUser
from offers_app.models import Offer
from offers_app.api.serializers import OfferSerializer
from offers_app.api.paginations import DynamicPageSizePagination


class OfferListView(ListCreateAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
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

    def get_queryset(self):
        queryset = super().get_queryset()
        creator_id = self.request.query_params.get('creator_id')
        min_price = self.request.query_params.get('min_price')
        max_delivery_time = self.request.query_params.get('max_delivery_time')

        if creator_id:
            try:
                creator_id = int(creator_id)
            except (TypeError, ValueError):
                raise ValidationError(
                    {'creator_id': 'Must be an integer.'})
            queryset = queryset.filter(user_id=creator_id)
        if min_price:
            try:
                min_price = float(min_price)
            except (TypeError, ValueError):
                raise ValidationError(
                    {'min_price': 'Must be a number.'})
            queryset = queryset.filter(price__gte=min_price)
        if max_delivery_time:
            try:
                max_delivery_time = int(max_delivery_time)
            except (TypeError, ValueError):
                raise ValidationError(
                    {'max_delivery_time': 'Must be an integer.'})
            queryset = queryset.filter(delivery_time__lte=max_delivery_time)
        return queryset
