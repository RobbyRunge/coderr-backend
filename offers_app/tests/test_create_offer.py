from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient


class OfferCreateTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass',
            user_type='business'
        )

    def test_create_offer_with_details(self):
        self.client.force_authenticate(user=self.user)
        offer_data = {
            "title": "Grafikdesign-Paket",
            "image": None,
            "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
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
