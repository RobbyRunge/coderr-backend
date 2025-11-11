from django.db.models import Q

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from orders_app.api.permissions import IsBusinessUserOfOrder, IsCustomerUser
from orders_app.models import Order
from orders_app.api.serializers import OrderSerializer
from offers_app.models import OfferDetail


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
        ).order_by('-created_at')

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsCustomerUser()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        offer_detail_id = request.data.get('offer_detail_id')
        if not offer_detail_id:
            return Response(
                {'detail': 'offer_detail_id is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            offer_detail = OfferDetail.objects.get(id=offer_detail_id)
        except OfferDetail.DoesNotExist:
            return Response(
                {'detail': 'OfferDetail not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        business_user = offer_detail.offer.user

        if request.user == business_user:
            return Response(
                {'detail': 'Kunde und Anbieter dürfen nicht identisch sein.'},
                status=status.HTTP_403_FORBIDDEN
            )

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


class OrderStatusUpdateView(generics.UpdateAPIView):
    """
    View to update the status of an existing order.
    """
    permission_classes = [IsAuthenticated, IsBusinessUserOfOrder]
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def patch(self, request, *args, **kwargs):
        order = self.get_object()
        status_value = request.data.get('status')
        if status_value not in ['in_progress', 'completed', 'cancelled']:
            return Response(
                {'detail': 'Invalid status.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        order.status = status_value
        order.save()
        serializer = self.get_serializer(order)
        return Response(serializer.data)
