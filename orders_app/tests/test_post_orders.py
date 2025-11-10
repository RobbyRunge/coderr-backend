from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status

from offers_app.models import Offer, OfferDetail
from profiles_app.models import Profile


class OrderCreateAPITest(APITestCase):
    def setUp(self):
        # Create users and their profiles
        User = get_user_model()
        self.customer = User.objects.create_user(
            username='customer_user',
            password='customerpass'
        )
        self.business = User.objects.create_user(
            username='business_user',
            password='businesspass'
        )
        Profile.objects.create(
            user=self.customer,
            username='customer',
            type='customer',
            email='customer@example.com'
        )
        Profile.objects.create(
            user=self.business,
            username='business',
            type='business',
            email='business@example.com'
        )
        Token.objects.create(user=self.customer)
        Token.objects.create(user=self.business)

        self.offer = Offer.objects.create(
            user=self.business,
            title="Logo Design",
            description="Design eines Logos"
        )
        self.offer_detail = OfferDetail.objects.create(
            offer=self.offer,
            title="Logo Design",
            revisions=3,
            delivery_time_in_days=5,
            price=150,
            features=["Logo Design", "Visitenkarten"],
            offer_type="basic"
        )

    # Test cases for creating an order
    def test_create_order_success(self):
        token = Token.objects.get(user=self.customer)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post('/api/orders/', {
            "offer_detail_id": self.offer_detail.id
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], "Logo Design")

    # Test cases for missing data
    def test_create_order_missing_offer_detail_id(self):
        token = Token.objects.get(user=self.customer)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post('/api/orders/', {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Test cases for invalid order creation
    def test_create_order_invalid_offer_detail_id(self):
        token = Token.objects.get(user=self.customer)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post('/api/orders/', {
            "offer_detail_id": 9999
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Test cases for unauthorized access
    def test_create_order_unauthenticated(self):
        response = self.client.post('/api/orders/', {
            "offer_detail_id": self.offer_detail.id
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Test cases for unauthorized user type
    def test_create_order_not_customer(self):
        token = Token.objects.get(user=self.business)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post('/api/orders/', {
            "offer_detail_id": self.offer_detail.id
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)