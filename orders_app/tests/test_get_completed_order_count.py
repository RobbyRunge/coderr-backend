from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token

from auth_app.models import CustomUser
from orders_app.models import Order
from profiles_app.models import Profile


class CompletedOrderCountTests(APITestCase):
    """
    Test suite for getting the count of completed orders for a business user.
    """
    def setUp(self):
        # Create users and profiles
        self.customer_user = CustomUser.objects.create_user(
            username='cust',
            password='pass'
        )
        Profile.objects.create(
            user=self.customer_user,
            username='customer',
            type='customer'
        )
        self.business_user = CustomUser.objects.create_user(
            username='biz',
            password='pass',
        )
        self.business_profile = Profile.objects.create(
            user=self.business_user,
            username='business',
            type='business'
        )
        Token.objects.create(user=self.business_user)
        Token.objects.create(user=self.customer_user)
        # Create completed orders
        Order.objects.create(
            customer_user=self.customer_user,
            business_user=self.business_user,
            title='A',
            revisions=1,
            delivery_time_in_days=1,
            price=10,
            features=[],
            offer_type='t',
            status='completed'
        )
        Order.objects.create(
            customer_user=self.customer_user,
            business_user=self.business_user,
            title='B',
            revisions=1,
            delivery_time_in_days=1,
            price=20,
            features=[],
            offer_type='t',
            status='completed'
        )

    # Test cases for getting completed order count
    def test_get_completed_order_count_success(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + Token.objects.get(user=self.business_user).key
        )
        url = f'/api/completed-order-count/{self.business_user.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['completed_order_count'], 2)

    # Test cases for unauthorized access
    def test_get_completed_order_count_unauthorized(self):
        url = f'/api/completed-order-count/{self.business_user.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Test cases for not found business user
    def test_get_completed_order_count_business_user_not_found(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + Token.objects.get(user=self.business_user).key
        )
        url = '/api/completed-order-count/9999/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
