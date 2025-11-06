from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase

from offers_app.models import Offer


class OfferListAPITest(APITestCase):
    """
    Tests for the Offer List API endpoint with filtering,
    ordering, searching, and pagination.
    """
    def setUp(self):
        # Create test users
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.user2 = get_user_model().objects.create_user(
            username='anotheruser',
            password='anotherpass'
        )
        # Create test offers
        self.offer_a1 = Offer.objects.create(
            user=self.user,
            title="Offer A1",
            description="Description for Offer A1",
            price=100,
            delivery_time=5,
            updated_at='2024-01-01T10:00:00Z'
        )
        self.offer_a2 = Offer.objects.create(
            user=self.user,
            title="Offer A2",
            description="Description for Offer A2",
            price=200,
            delivery_time=10,
            updated_at='2024-01-02T10:00:00Z'
        )
        self.offer_b1 = Offer.objects.create(
            user=self.user2,
            title="Offer B1",
            description="Description for Offer B1",
            price=150,
            delivery_time=7,
            updated_at='2024-01-03T10:00:00Z'
        )

    # Test cases for retrieving all offers
    def test_offers_list_returns_all_offers(self):
        url = '/api/offers/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        # Check that all three offers are returned (consider pagination!)
        self.assertEqual(data['count'], 3)
        titles = [offer['title'] for offer in data['results']]
        self.assertIn(self.offer_a1.title, titles)
        self.assertIn(self.offer_a2.title, titles)
        self.assertIn(self.offer_b1.title, titles)

    # Test cases for filtering by creator_id
    def test_filter_by_creator_id(self):
        url = '/api/offers/?creator_id={}'.format(self.user.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        # Check that only the offers created by the user are returned
        self.assertEqual(data['count'], 2)
        titles = [offer['title'] for offer in data['results']]
        self.assertIn(self.offer_a1.title, titles)
        self.assertIn(self.offer_a2.title, titles)
        self.assertNotIn(self.offer_b1.title, titles)

    # Test cases for filtering by min_price
    def test_filter_by_min_price(self):
        url = '/api/offers/?min_price=150'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        # Check that only the offers with a price >= 150 are returned
        self.assertEqual(data['count'], 2)
        titles = [offer['title'] for offer in data['results']]
        self.assertNotIn(self.offer_a1.title, titles)
        self.assertIn(self.offer_a2.title, titles)
        self.assertIn(self.offer_b1.title, titles)

    # Test cases for filtering by max_delivery_time
    def test_filter_by_max_delivery_time(self):
        url = '/api/offers/?max_delivery_time=7'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        # Check that only the offers with a delivery_time <= 7 are returned
        self.assertEqual(data['count'], 2)
        titles = [offer['title'] for offer in data['results']]
        self.assertIn(self.offer_a1.title, titles)
        self.assertIn(self.offer_b1.title, titles)
        self.assertNotIn(self.offer_a2.title, titles)

    # Test cases for ordering by updated_at or min_price
    def test_ordering(self):
        url = '/api/offers/?ordering=updated_at'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        # Check that the offers are ordered by updated_at
        self.assertEqual(data['count'], 3)
        self.assertEqual(data['results'][0]['title'], self.offer_a2.title)
        self.assertEqual(data['results'][1]['title'], self.offer_a1.title)
        self.assertEqual(data['results'][2]['title'], self.offer_b1.title)

    # Test cases for searching by title or description
    def test_search(self):
        url = '/api/offers/?search=Offer A1'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        # Check that only the offers matching the search term are returned
        self.assertEqual(data['count'], 1)
        self.assertEqual(data['results'][0]['title'], self.offer_a1.title)

    # Test cases for pagination
    def test_pagination(self):
        url = '/api/offers/?page=1&page_size=2'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        # Check that only 2 offers are returned
        self.assertEqual(data['count'], 3)
        self.assertEqual(len(data['results']), 2)

    # Test cases for response structure
    def test_response_structure(self):
        url = '/api/offers/?page=1&page_size=2'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        # Check the structure of the response
        self.assertIn('count', data)
        self.assertIn('results', data)
        self.assertIsInstance(data['results'], list)
