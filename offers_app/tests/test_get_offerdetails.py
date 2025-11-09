from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from offers_app.models import Offer, OfferDetail


class OfferDetailGetTest(APITestCase):
    """
    Test suite for retrieving offer details via the API.
    """
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass',
        )
        self.token = Token.objects.create(user=self.user)
        self.offer = Offer.objects.create(
            user=self.user,
            title='Test Offer',
            description='This is a test offer.'
        )
        self.detail = OfferDetail.objects.create(
            offer=self.offer,
            title='Basic Design',
            revisions=2,
            delivery_time_in_days=5,
            price=100,
            features=['Logo Design', 'Visitenkarte'],
            offer_type='basic'
        )

    # Test cases for retrieving an offer detail
    def test_get_offerdetail_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(f'/api/offerdetails/{self.detail.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], self.detail.id)
        self.assertEqual(response.data['title'], 'Basic Design')

    # Test cases for unauthenticated access
    def test_get_offerdetail_unauthenticated(self):
        response = self.client.get(f'/api/offerdetails/{self.detail.id}/')
        self.assertEqual(response.status_code, 401)

    # Test cases for non-existent offer detail
    def test_get_offerdetail_not_found(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get('/api/offerdetails/999999/')
        self.assertEqual(response.status_code, 404)