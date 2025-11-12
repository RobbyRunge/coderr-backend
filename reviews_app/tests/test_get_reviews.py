from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from reviews_app.models import Review


class ReviewListViewTests(APITestCase):
    """
    Test suite for the Review List API endpoint.
    """
    def setUp(self):
        # Create users and tokens
        User = get_user_model()
        self.user = User.objects.create_user(username="user", password="pass")
        self.user_token = Token.objects.create(user=self.user)

        self.business_user = User.objects.create_user(username="business", password="pass")
        self.business_user_token = Token.objects.create(user=self.business_user)

        self.other_user = User.objects.create_user(username="other", password="pass")
        self.other_user_token = Token.objects.create(user=self.other_user)

        self.other_business_user = User.objects.create_user(username="other_business", password="pass")
        self.other_business_user_token = Token.objects.create(user=self.other_business_user)

        # Create some reviews
        Review.objects.create(
            business_user=self.business_user,
            reviewer=self.user,
            rating=4,
            description="Sehr professioneller Service.",
        )
        Review.objects.create(
            business_user=self.business_user,
            reviewer=self.other_user,
            rating=2,
            description="Nicht so gut.",
        )
        Review.objects.create(
            business_user=self.other_business_user,
            reviewer=self.user,
            rating=5,
            description="Top Qualität!",
        )

    # Test cases for successful retrieval of reviews
    def test_authenticated_user_can_list_reviews(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + Token.objects.get(user=self.business_user).key
        )
        url = reverse("reviews-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data["results"], list)

    # Test cases for unauthentication
    def test_unauthenticated_user(self):
        url = reverse("reviews-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    # Test cases for filtering by business user
    def test_filter_by_business_user_id(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.user_token.key
        )
        url = reverse("reviews-list")
        response = self.client.get(url, {"business_user": self.business_user.id})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(all(r["business_user"] == self.business_user.id for r in response.data["results"]))

    # Test cases for filtering by reviewer user
    def test_filter_by_reviewer_id(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.user_token.key
        )
        url = reverse("reviews-list")
        response = self.client.get(url, {"reviewer": self.user.id})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(all(r["reviewer"] == self.user.id for r in response.data["results"]))

    # Test cases for ordering by updated_at
    def test_ordering_by_updated_at(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.user_token.key
        )
        url = reverse("reviews-list")
        response = self.client.get(url, {"ordering": "updated_at"})
        self.assertEqual(response.status_code, 200)
        updated_ats = [r["updated_at"] for r in response.data["results"]]
        self.assertEqual(updated_ats, sorted(updated_ats))

    # Test cases for ordering by rating
    def test_ordering_by_rating(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.user_token.key
        )
        url = reverse("reviews-list")
        response = self.client.get(url, {"ordering": "rating"})
        self.assertEqual(response.status_code, 200)
        ratings = [r["rating"] for r in response.data["results"]]
        self.assertEqual(ratings, sorted(ratings))
