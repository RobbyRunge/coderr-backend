from django.urls import path

from orders_app.api.views import OrderListCreateView, OrderStatusUpdateView


urlpatterns = [
    path('orders/', OrderListCreateView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', OrderStatusUpdateView.as_view(), name='order-status-update'),
]
