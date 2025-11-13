from django.urls import reverse

from rest_framework.test import APITestCase

from base_info_app.models import Review, BusinessProfile, Offer


class BaseInfoAPITest(APITestCase):
    """
    Tests for the BaseInfo API endpoint.
    """
    def setUp(self):
        # 10 Reviews with various ratings
        ratings = [4.5, 5.0, 4.0, 4.7, 4.6, 4.8, 4.9, 4.3, 4.4, 4.6]
        for r in ratings:
            Review.objects.create(rating=r)
        # 45 BusinessProfiles
        for _ in range(45):
            BusinessProfile.objects.create()
        # 150 Offers
        for _ in range(150):
            Offer.objects.create()

    def test_base_info_status_200(self):
        url = reverse('base-info')
        response = self.client.get(url)
        assert response.status_code == 200

    def test_base_info_fields(self):
        url = reverse('base-info')
        response = self.client.get(url)
        data = response.json()
        assert 'review_count' in data
        assert 'average_rating' in data
        assert 'business_profile_count' in data
        assert 'offer_count' in data

    def test_base_info_values(self):
        url = reverse('base-info')
        response = self.client.get(url)
        data = response.json()
        assert data['review_count'] == 10
        # Calculate expected average rating
        ratings = [4.5, 5.0, 4.0, 4.7, 4.6, 4.8, 4.9, 4.3, 4.4, 4.6]
        avg = round(sum(ratings) / len(ratings), 1)
        assert data['average_rating'] == avg
        assert data['business_profile_count'] == 45
        assert data['offer_count'] == 150
