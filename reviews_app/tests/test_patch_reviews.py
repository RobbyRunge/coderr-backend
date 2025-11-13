from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from auth_app.models import CustomUser
from reviews_app.models import Review


class ReviewPatchTests(APITestCase):
    """
    Test cases for PATCH requests on reviews
    """
    def setUp(self):
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
        self.review = Review.objects.create(
            business_user=self.business_user,
            reviewer=self.customer_user,
            rating=4,
            description="Alles war toll!"
        )

    # Test cases for success requests
    def test_customer_can_patch_own_review(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = reverse("reviews-detail", args=[self.review.id])
        data = {
            "rating": 5,
            "description": "Noch besser als erwartet!"
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["rating"], 5)
        self.assertEqual(response.data["description"], "Noch besser als erwartet!")

    # Test cases for invalid requests
    def test_patch_review_with_invalid_rating(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = reverse("reviews-detail", args=[self.review.id])
        data = {
            "rating": 10,  # Invalid rating (should be between 1 and 5)
            "description": "Ungültiges Rating!"
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("rating", response.data)

    # Test cases for unauthorized requests
    def test_patch_review_unauthenticated(self):
        url = reverse("reviews-detail", args=[self.review.id])
        data = {
            "rating": 5,
            "description": "Versuch ohne Authentifizierung"
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 401)

    # Test cases for forbidden requests
    def test_patch_review_forbidden_for_other_user(self):
        other_user = CustomUser.objects.create_user(
            username="anderer_kunde",
            password="pass",
            user_type="customer"
        )
        other_token = Token.objects.create(user=other_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + other_token.key)
        url = reverse("reviews-detail", args=[self.review.id])
        data = {
            "rating": 3,
            "description": "Ich bin nicht der Ersteller!"
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 403)

    # Test cases for not found requests
    def test_patch_review_not_found(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = reverse("reviews-detail", args=[9999])
        data = {
            "rating": 5,
            "description": "Nicht vorhanden"
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 404)
