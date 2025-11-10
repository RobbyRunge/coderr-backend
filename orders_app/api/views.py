from django.db.models import Q

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from orders_app.models import Order
from orders_app.api.serializers import OrderSerializer
from offers_app.models import OfferDetail
from profiles_app.models import Profile


class OrderListCreateView(generics.ListCreateAPIView):
    """
    View to list all orders for a user and create new orders.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(
            Q(customer_user=user) | Q(business_user=user)
        )

    def create(self, request, *args, **kwargs):
        # Check if user is a customer
        offer_detail_id = request.data.get('offer_detail_id')
        offer_detail = OfferDetail.objects.get(id=offer_detail_id)
        business_user = offer_detail.offer.user

    # NEU: Verhindere, dass Kunde und Anbieter identisch sind!
        if request.user == business_user:
            return Response(
                {'detail': 'Kunde und Anbieter dürfen nicht identisch sein.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return Response({'detail': 'Profile not found.'}, status=status.HTTP_403_FORBIDDEN)
        if getattr(profile, 'type', None) != 'customer':
            return Response({'detail': 'Only customers can create orders.'}, status=status.HTTP_403_FORBIDDEN)

        offer_detail_id = request.data.get('offer_detail_id')
        if not offer_detail_id:
            return Response({'detail': 'offer_detail_id is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            offer_detail = OfferDetail.objects.get(id=offer_detail_id)
        except OfferDetail.DoesNotExist:
            return Response({'detail': 'OfferDetail not found.'}, status=status.HTTP_404_NOT_FOUND)

        business_user = offer_detail.offer.user

        print("customer_user:", request.user)
        print("business_user:", business_user)
        print("features:", offer_detail.features)

        order = Order.objects.create(
            customer_user=request.user,
            business_user=business_user,
            title=offer_detail.title,
            revisions=offer_detail.revisions,
            delivery_time_in_days=offer_detail.delivery_time_in_days,
            price=offer_detail.price,
            features=offer_detail.features,
            offer_type=offer_detail.offer_type,
            status='in_progress'
        )
        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
