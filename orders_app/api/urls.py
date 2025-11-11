from django.urls import path

from orders_app.api.views import (
    OrderListCreateView,
    OrderDetailView,
    OrderCountView
)


urlpatterns = [
    path('orders/', OrderListCreateView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('order-count/<int:pk>/', OrderCountView.as_view(), name='order-count'),
    path('completed-order-count/<int:pk>/', OrderDetailView.as_view(), name='completed-order-count'),
]
