from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from auth_app.models import CustomUser
from orders_app.models import Order


class OrderDeleteAPITest(APITestCase):
    def setUp(self):
        # Admin user (is_staff)
        self.admin_user = CustomUser.objects.create_user(
            username='adminuser',
            password='adminpass',
            is_staff=True
        )
        # Normal user
        self.normal_user = CustomUser.objects.create_user(
            username='normaluser',
            password='normalpass'
        )
        Token.objects.create(user=self.admin_user)
        Token.objects.create(user=self.normal_user)

        # Test order
        self.order = Order.objects.create(
            customer_user=self.normal_user,
            business_user=self.admin_user,
            title="Test Order",
            revisions=1,
            delivery_time_in_days=2,
            price=100,
            features=[],
            offer_type="basic",
            status="in_progress",
            created_at=timezone.now(),
            updated_at=timezone.now()
        )

    # Test cases for success delete
    def test_delete_order_success(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + Token.objects.get(user=self.admin_user).key
        )
        url = f'/api/orders/{self.order.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Order.objects.filter(id=self.order.id).exists())

    # Test cases for unauthenticated delete
    def test_delete_order_unauthenticated(self):
        url = f'/api/orders/{self.order.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 401)

    # Test cases for forbidden delete
    def test_delete_order_forbidden(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + Token.objects.get(user=self.normal_user).key
        )
        url = f'/api/orders/{self.order.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)

    # Test cases for order not found
    def test_delete_order_not_found(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + Token.objects.get(user=self.admin_user).key
        )
        url = '/api/orders/99999/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)