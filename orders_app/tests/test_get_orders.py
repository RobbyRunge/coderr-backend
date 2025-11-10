from django.contrib.auth import get_user_model
from django.utils import timezone

from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from orders_app.models import Order


class OrderListAPITest(APITestCase):
    """
    Test cases for the Order List API endpoint.
    """
    def setUp(self):
        # Create test users
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass',
        )
        self.user2 = get_user_model().objects.create_user(
            username='anotheruser',
            password='anotherpass',
        )
        Token.objects.create(user=self.user)
        Token.objects.create(user=self.user2)
        # Create test orders
        self.order_a1 = Order.objects.create(
            customer_user=self.user,
            business_user=self.user,
            title="Order A1",
            revisions=1,
            delivery_time_in_days=5,
            price=150,
            features=[],
            offer_type="basic",
            status="in_progress",
            created_at=timezone.now(),
            updated_at=timezone.now()
        )
        self.order_a2 = Order.objects.create(
            customer_user=self.user,
            business_user=self.user2,
            title="Order A2",
            revisions=2,
            delivery_time_in_days=10,
            price=250,
            features=[],
            offer_type="premium",
            status="completed",
            created_at=timezone.now(),
            updated_at=timezone.now()
        )
        self.order_b1 = Order.objects.create(
            customer_user=self.user2,
            business_user=self.user,
            title="Order B1",
            revisions=1,
            delivery_time_in_days=5,
            price=300,
            features=[],
            offer_type="basic",
            status="shipped",
            created_at=timezone.now(),
            updated_at=timezone.now()
        )

    # Test cases for authenticated access
    def test_get_orders(self):
        token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get('/api/orders/')
        self.assertEqual(response.status_code, 200)
        orders = response.json()
        titles = [order['title'] for order in orders]
        self.assertIn("Order A1", titles)
        self.assertIn("Order A2", titles)

    # Test cases for unauthenticated access
    def test_get_orders_unauthenticated(self):
        response = self.client.get('/api/orders/')
        self.assertEqual(response.status_code, 401)

    # Test cases for user with no orders
    def test_get_orders_empty(self):
        user3 = get_user_model().objects.create_user(
            username='nouserorders',
            password='nopass',
        )
        token = Token.objects.create(user=user3)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get('/api/orders/')
        self.assertEqual(response.status_code, 200)
        orders = response.json()
        self.assertEqual(orders, [])
