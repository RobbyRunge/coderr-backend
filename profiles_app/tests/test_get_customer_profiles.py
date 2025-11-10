from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token


class CustomerProfileListViewTests(APITestCase):
    """
    Test suite for retrieving customer profiles via the API.
    """
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass',
        )
        self.client = APIClient()
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    # Test retrieving customer profiles
    def test_get_customer_profiles(self):
        response = self.client.get('/api/profiles/customer/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('results', response.data)
        self.assertIsInstance(response.data['results'], list)
        for profile in response.data['results']:
            self.assertEqual(profile['type'], 'customer')

    # Test that certain fields are never null in the response
    def test_fields_never_null(self):
        response = self.client.get('/api/profiles/customer/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('results', response.data)
        for profile in response.data['results']:
            for field in [
                'first_name', 'last_name', 'location',
                'tel', 'description', 'working_hours'
            ]:
                self.assertIn(field, profile)
                self.assertIsNotNone(profile[field])
                self.assertIsInstance(profile[field], str)
