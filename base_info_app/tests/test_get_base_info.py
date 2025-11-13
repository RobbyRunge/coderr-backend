from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from profiles_app.models import Profile
from offers_app.models import Offer, OfferDetail
from reviews_app.models import Review


class BaseInfoAPITest(APITestCase):
    """
    Test cases for the Base Info API endpoint.
    """

    def setUp(self):
        self.base_info_url = '/api/base-info/'
        User = get_user_model()
        self.business_user = User.objects.create_user(
            username='businessuser',
            email='business@example.com',
            password='testpass123'
        )
        self.customer_user = User.objects.create_user(
            username='customeruser',
            email='customer@example.com',
            password='testpass123'
        )

    # Test cases base info with empty database.
    def test_base_info_empty_database(self):
        response = self.client.get(self.base_info_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['review_count'], 0)
        self.assertEqual(response.data['average_rating'], 0)
        self.assertEqual(response.data['business_profile_count'], 0)
        self.assertEqual(response.data['offer_count'], 0)

    # Test cases base info with all data types present.
    def test_base_info_complete_data(self):
        # Create business profile (customer should not be counted)
        Profile.objects.create(
            user=self.business_user,
            username='businessuser',
            email='business@example.com',
            type='business'
        )
        Profile.objects.create(
            user=self.customer_user,
            username='customeruser',
            email='customer@example.com',
            type='customer'
        )
        # Create offers
        offer = Offer.objects.create(
            user=self.business_user,
            title='Web Development',
            description='Professional services'
        )
        OfferDetail.objects.create(
            offer=offer,
            title='Basic',
            revisions=2,
            delivery_time_in_days=5,
            price=500,
            features=[],
            offer_type='basic'
        )
        # Create reviews
        Review.objects.create(
            business_user=self.business_user,
            reviewer=self.customer_user,
            rating=5,
            description='Excellent!'
        )
        Review.objects.create(
            business_user=self.business_user,
            reviewer=self.customer_user,
            rating=4,
            description='Very good'
        )
        response = self.client.get(self.base_info_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['review_count'], 2)
        self.assertEqual(response.data['average_rating'], 4.5)
        self.assertEqual(response.data['business_profile_count'], 1)
        self.assertEqual(response.data['offer_count'], 1)

    # Test cases that average rating is rounded to one decimal place.
    def test_base_info_average_rating_rounding(self):
        Review.objects.create(
            business_user=self.business_user,
            reviewer=self.customer_user,
            rating=5,
            description='Perfect!'
        )
        Review.objects.create(
            business_user=self.business_user,
            reviewer=self.customer_user,
            rating=4,
            description='Good'
        )
        Review.objects.create(
            business_user=self.business_user,
            reviewer=self.customer_user,
            rating=5,
            description='Excellent'
        )
        response = self.client.get(self.base_info_url)
        self.assertEqual(response.status_code, 200)
        # Average: (5 + 4 + 5) / 3 = 4.666... -> rounded to 4.7
        self.assertEqual(response.data['average_rating'], 4.7)

    # Test cases for no authentication required
    def test_base_info_no_authentication_required(self):
        self.client.logout()
        response = self.client.get(self.base_info_url)
        self.assertEqual(response.status_code, 200)
