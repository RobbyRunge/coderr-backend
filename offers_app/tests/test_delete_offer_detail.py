from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from offers_app.models import Offer


class OfferDeleteTest(APITestCase):
    """
    Test suite for deleting an offer via the API.
    """
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username='businessuser',
            password='businesspass',
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='otherpass',
        )
        self.token = Token.objects.create(user=self.user)
        self.other_token = Token.objects.create(user=self.other_user)

        # Create an offer to be deleted
        self.offer = Offer.objects.create(
            user=self.user,
            title='Test Offer',
            description='This is a test offer.'
        )

    # Test cases for deleting an offer
    def test_delete_offer(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.delete(f'/api/offers/{self.offer.id}/')
        self.assertEqual(response.status_code, 204)
        # Check that the offer has been deleted
        with self.assertRaises(Offer.DoesNotExist):
            Offer.objects.get(id=self.offer.id)

    # Test cases for unauthenticated delete attempt
    def test_delete_offer_unauthenticated(self):
        response = self.client.delete(f'/api/offers/{self.offer.id}/')
        self.assertEqual(response.status_code, 401)
        self.assertTrue(Offer.objects.filter(id=self.offer.id).exists())

    # Test cases for not owner trying to delete
    def test_delete_offer_not_owner(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.other_token.key)
        response = self.client.delete(f'/api/offers/{self.offer.id}/')
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Offer.objects.filter(id=self.offer.id).exists())

    # Test cases for deleting a non-existent offer
    def test_delete_offer_not_found(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.delete('/api/offers/999999/')
        self.assertEqual(response.status_code, 404)
