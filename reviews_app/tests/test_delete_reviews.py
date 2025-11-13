from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from auth_app.models import CustomUser
from reviews_app.models import Review


class DeleteReviewTests(APITestCase):
    """
    Test suite for deleting reviews.
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

    # Test cases for successful delete requests
    def test_customer_can_delete_own_review(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token.key
        )
        url = reverse("reviews-detail", args=[self.review.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Review.objects.filter(id=self.review.id).exists())

    # Test cases for unauthorized delete requests
    def test_delete_review_unauthenticated(self):
        url = reverse("reviews-detail", args=[self.review.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 401)

    # Test cases for forbidden delete requests
    def test_delete_review_forbidden_for_other_user(self):
        other_user = CustomUser.objects.create_user(
            username="other",
            password="pass",
            user_type="customer"
        )
        other_token = Token.objects.create(user=other_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + other_token.key)
        url = reverse("reviews-detail", args=[self.review.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)

    # Test cases for not found delete requests
    def test_delete_review_not_found(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = reverse("reviews-detail", args=[99999])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)
