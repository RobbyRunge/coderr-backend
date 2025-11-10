from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from orders_app.models import Order
from orders_app.api.serializers import OrderSerializer


class OrderListView(APIView):
    """
    View to list all orders for a user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(
            Q(customer_user=request.user) | Q(business_user=request.user)
        )
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
