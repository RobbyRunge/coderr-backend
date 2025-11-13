from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from auth_app.models import CustomUser


class ReviewCreateTests(APITestCase):
    """
    Test suite for the Review Create API endpoint.
    """
    def setUp(self):
        # Create users and tokens
        self.customer_user = CustomUser.objects.create_user(
            username="kunde",
            password="pass",
            user_type="customer"
        )
        self.business_user = CustomUser.objects.create_user(
            username="business",
            password="pass",
            user_type="business"
        )
        self.token = Token.objects.create(user=self.customer_user)

    # Test cases for creating reviews
    def test_customer_can_create_review(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = reverse("reviews-list")
        data = {
            "business_user": self.business_user.id,
            "rating": 4,
            "description": "Alles war toll!"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["business_user"], self.business_user.id)
        self.assertEqual(response.data["reviewer"], self.customer_user.id)
        self.assertEqual(response.data["rating"], 4)
        self.assertEqual(response.data["description"], "Alles war toll!")

    # Test cases for duplicate reviews
    def test_customer_cannot_create_duplicate_review(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = reverse("reviews-list")
        data = {
            "business_user": self.business_user.id,
            "rating": 4,
            "description": "Alles war toll!"
        }
        # Erste Bewertung (soll funktionieren)
        response1 = self.client.post(url, data)
        self.assertEqual(response1.status_code, 201)
        # Zweite Bewertung (soll fehlschlagen)
        response2 = self.client.post(url, data)
        self.assertEqual(response2.status_code, 400)
        self.assertIn("already", str(response2.data).lower())

    # Test cases for unauthenticated access
    def test_unauthenticated_user_cannot_create_review(self):
        url = reverse("reviews-list")
        data = {
            "business_user": self.business_user.id,
            "rating": 4,
            "description": "Alles war toll!"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 401)

    # Test cases for business user trying to create a review
    def test_business_user_cannot_create_review(self):
        business_token = Token.objects.create(user=self.business_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + business_token.key)
        url = reverse("reviews-list")
        data = {
            "business_user": self.business_user.id,
            "rating": 4,
            "description": "Alles war toll!"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 403)

    # Test cases for invalid data
    def test_create_review_with_invalid_data(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = reverse("reviews-list")
        # Fehlendes Feld 'rating'
        data = {
            "business_user": self.business_user.id,
            "description": "Alles war toll!"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("rating", response.data)
