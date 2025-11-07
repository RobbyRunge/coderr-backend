from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase

from offers_app.models import Offer, OfferDetail


class OfferDetailAPITest(APITestCase):
    """
    Test cases for the OfferDetail API endpoint.
    """
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.offer = Offer.objects.create(
            user=self.user,
            title='Grafikdesign-Paket',
            image=None,
            description='Ein umfassendes Grafikdesign-Paket für Unternehmen.'
        )
        OfferDetail.objects.create(
            offer=self.offer,
            title='Basic Design',
            revisions=2,
            delivery_time_in_days=5,
            price=50,
            features=['Logo Design', 'Visitenkarte'],
            offer_type='basic'
        )
        OfferDetail.objects.create(
            offer=self.offer,
            title='Standard Design',
            revisions=5,
            delivery_time_in_days=7,
            price=100,
            features=['Logo Design', 'Visitenkarte', 'Briefpapier'],
            offer_type='standard'
        )
        OfferDetail.objects.create(
            offer=self.offer,
            title='Premium Design',
            revisions=10,
            delivery_time_in_days=10,
            price=200,
            features=['Logo Design', 'Visitenkarte', 'Briefpapier', 'Flyer'],
            offer_type='premium'
        )

    # Test cases for testing successful retrieval of offer details
    def test_get_offer_detail_success(self):
        self.client.force_authenticate(user=self.user)
        url = f'/api/offers/{self.offer.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('id', data)
        self.assertIn('user', data)
        self.assertIn('title', data)
        self.assertIn('details', data)
        self.assertEqual(len(data['details']), 3)

    # Test cases for testing unauthenticated access
    def test_get_offer_detail_unauthenticated(self):
        url = f'/api/offers/{self.offer.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    # Test cases for testing non-existing offer
    def test_get_offer_detail_not_found(self):
        self.client.force_authenticate(user=self.user)
        url = '/api/offers/99999/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
