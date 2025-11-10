from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient


class OfferCreateTests(TestCase):
    """
    Test cases for creating offers via the API.
    """
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass',
            user_type='business'
        )

    # Test cases creating an offer with valid details
    def test_create_offer_with_details(self):
        self.client.force_authenticate(user=self.user)
        offer_data = {
            "title": "Grafikdesign-Paket",
            "image": None,
            "description":
                "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
            "details": [
                {
                    "title": "Basic Design",
                    "revisions": 2,
                    "delivery_time_in_days": 5,
                    "price": 100,
                    "features": [
                        "Logo Design",
                        "Visitenkarte"
                    ],
                    "offer_type": "basic"
                },
                {
                    "title": "Standard Design",
                    "revisions": 5,
                    "delivery_time_in_days": 7,
                    "price": 200,
                    "features": [
                        "Logo Design",
                        "Visitenkarte",
                        "Briefpapier"
                    ],
                    "offer_type": "standard"
                },
                {
                    "title": "Premium Design",
                    "revisions": 10,
                    "delivery_time_in_days": 10,
                    "price": 500,
                    "features": [
                        "Logo Design",
                        "Visitenkarte",
                        "Briefpapier",
                        "Flyer"
                    ],
                    "offer_type": "premium"
                }
            ]
        }
        response = self.client.post('/api/offers/', offer_data, format='json')
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertIn('id', data)
        self.assertEqual(data['title'], offer_data['title'])
        self.assertEqual(len(data['details']), 3)
        for detail in data['details']:
            self.assertIn('id', detail)
            self.assertIn('title', detail)
            self.assertIn('revisions', detail)
            self.assertIn('delivery_time_in_days', detail)
            self.assertIn('price', detail)
            self.assertIn('features', detail)
            self.assertIn('offer_type', detail)

    # Test cases creating an offer with fewer than three details
    def test_create_offer_with_too_few_details(self):
        self.client.force_authenticate(user=self.user)
        offer_data = {
            "title": "Testangebot",
            "image": None,
            "description": "Zu wenige Details",
            "details": [
                {
                    "title": "Nur eins",
                    "revisions": 1,
                    "delivery_time_in_days": 1,
                    "price": 10,
                    "features": ["Feature"],
                    "offer_type": "basic"
                }
            ]
        }
        response = self.client.post('/api/offers/', offer_data, format='json')
        self.assertEqual(response.status_code, 400)

    # Test cases creating an offer as a non-business user
    def test_create_offer_as_non_business_user(self):
        customer = get_user_model().objects.create_user(
            username='customer',
            password='testpass',
            user_type='customer'
        )
        self.client.force_authenticate(user=customer)
        offer_data = {
            "title": "Testangebot",
            "image": None,
            "description": "Nur für Business",
            "details": [
                {
                    "title": "Basic",
                    "revisions": 1,
                    "delivery_time_in_days": 1,
                    "price": 10,
                    "features": ["Feature"],
                    "offer_type": "basic"
                },
                {
                    "title": "Standard",
                    "revisions": 2,
                    "delivery_time_in_days": 2,
                    "price": 20,
                    "features": ["Feature"],
                    "offer_type": "standard"
                },
                {
                    "title": "Premium",
                    "revisions": 3,
                    "delivery_time_in_days": 3,
                    "price": 30,
                    "features": ["Feature"],
                    "offer_type": "premium"
                }
            ]
        }
        response = self.client.post('/api/offers/', offer_data, format='json')
        self.assertEqual(response.status_code, 403)

    # Test cases creating an offer without authentication
    def test_create_offer_unauthenticated(self):
        offer_data = {
            "title": "Testangebot",
            "image": None,
            "description": "Nicht eingeloggt",
            "details": [
                {
                    "title": "Basic",
                    "revisions": 1,
                    "delivery_time_in_days": 1,
                    "price": 10,
                    "features": ["Feature"],
                    "offer_type": "basic"
                },
                {
                    "title": "Standard",
                    "revisions": 2,
                    "delivery_time_in_days": 2,
                    "price": 20,
                    "features": ["Feature"],
                    "offer_type": "standard"
                },
                {
                    "title": "Premium",
                    "revisions": 3,
                    "delivery_time_in_days": 3,
                    "price": 30,
                    "features": ["Feature"],
                    "offer_type": "premium"
                }
            ]
        }
        response = self.client.post('/api/offers/', offer_data, format='json')
        self.assertEqual(response.status_code, 401)

    # Test cases creating an offer with missing title
    def test_create_offer_missing_title(self):
        self.client.force_authenticate(user=self.user)
        offer_data = {
            "image": None,
            "description": "Kein Titel",
            "details": [
                {
                    "title": "Basic",
                    "revisions": 1,
                    "delivery_time_in_days": 1,
                    "price": 10,
                    "features": ["Feature"],
                    "offer_type": "basic"
                },
                {
                    "title": "Standard",
                    "revisions": 2,
                    "delivery_time_in_days": 2,
                    "price": 20,
                    "features": ["Feature"],
                    "offer_type": "standard"
                },
                {
                    "title": "Premium",
                    "revisions": 3,
                    "delivery_time_in_days": 3,
                    "price": 30,
                    "features": ["Feature"],
                    "offer_type": "premium"
                }
            ]
        }
        response = self.client.post('/api/offers/', offer_data, format='json')
        self.assertEqual(response.status_code, 400)
