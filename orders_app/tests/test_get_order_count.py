from django.utils import timezone

from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from auth_app.models import CustomUser
from profiles_app.models import Profile
from orders_app.models import Order


class OrderCountAPITest(APITestCase):
    def setUp(self):
        Profile.objects.all().delete()
        CustomUser.objects.all().delete()
        # Business user
        self.business_user = CustomUser.objects.create_user(
            username='businessuserordercount',
            password='businesspassordercount'
        )
        Profile.objects.create(
            user=self.business_user,
            username='businessuserordercount',
            email='business@test.com',
            type='business'
        )
        # Customer user
        self.customer_user = CustomUser.objects.create_user(
            username='customeruserordercount',
            password='customerpassordercount'
        )
        Profile.objects.create(
            user=self.customer_user,
            username='customeruserordercount',
            email='customer@test.com',
            type='customer'
        )
        Token.objects.create(user=self.business_user)
        Token.objects.create(user=self.customer_user)

        # In-progress orders for business user
        for _ in range(3):
            Order.objects.create(
                customer_user=self.customer_user,
                business_user=self.business_user,
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

    # Test cases for getting order count
    def test_get_order_count_success(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + Token.objects.get(user=self.business_user).key
        )
        url = f'/api/order-count/{self.business_user.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['order_count'], 3)

    # Test cases for unauthenticated access
    def test_get_order_count_unauthenticated(self):
        url = f'/api/order-count/{self.business_user.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    # Test cases for non-business user access
    def test_get_order_count_not_business_user(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + Token.objects.get(user=self.customer_user).key
        )
        url = f'/api/order-count/{self.customer_user.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    # Test cases for business user not found
    def test_get_order_count_not_found(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + Token.objects.get(user=self.business_user).key
        )
        url = '/api/order-count/99999/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)