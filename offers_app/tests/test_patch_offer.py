from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token

from offers_app.models import Offer, OfferDetail


class OfferPatchAPITest(APITestCase):
    """
    Tests for PATCH /api/offers/<int:pk>/ endpoint.
    """
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='patchuser',
            password='patchpass'
        )
        self.other_user = get_user_model().objects.create_user(
            username='otheruser',
            password='otherpass'
        )
        self.token = Token.objects.create(user=self.user)
        self.other_token = Token.objects.create(user=self.other_user)
        self.offer = Offer.objects.create(
            user=self.user,
            title="Grafikdesign-Paket",
            description="Ein umfassendes Grafikdesign-Paket für Unternehmen."
        )
        self.detail_basic = OfferDetail.objects.create(
            offer=self.offer,
            title="Basic Design",
            revisions=2,
            delivery_time_in_days=7,
            price=100,
            features=["Logo Design"],
            offer_type="basic"
        )
        self.detail_standard = OfferDetail.objects.create(
            offer=self.offer,
            title="Standard Design",
            revisions=5,
            delivery_time_in_days=10,
            price=120,
            features=["Logo Design", "Visitenkarte", "Briefpapier"],
            offer_type="standard"
        )
        self.detail_premium = OfferDetail.objects.create(
            offer=self.offer,
            title="Premium Design",
            revisions=10,
            delivery_time_in_days=10,
            price=150,
            features=["Logo Design", "Visitenkarte", "Briefpapier", "Flyer"],
            offer_type="premium"
        )
        self.url = reverse('offer-detail', args=[self.offer.id])

    # Test cases for patch title and basic detail
    def test_patch_offer_title_and_basic_detail(self):
        self.client.login(username='patchuser', password='patchpass')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        patch_data = {
            "title": "Updated Grafikdesign-Paket",
            "details": [
                {
                    "id": self.detail_basic.id,
                    "title": "Basic Design Updated",
                    "revisions": 3,
                    "delivery_time_in_days": 6,
                    "price": 120,
                    "features": ["Logo Design", "Flyer"],
                    "offer_type": "basic"
                }
            ]
        }
        response = self.client.patch(self.url, patch_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Updated Grafikdesign-Paket")
        basic_detail = next(
            d for d in response.data['details'] if d['offer_type'] == 'basic'
        )
        self.assertEqual(basic_detail['title'], "Basic Design Updated")
        self.assertEqual(basic_detail['revisions'], 3)
        self.assertEqual(basic_detail['delivery_time_in_days'], 6)
        self.assertEqual(basic_detail['price'], 120)
        self.assertEqual(basic_detail['features'], ["Logo Design", "Flyer"])
        standard_detail = next(
            d for d in response.data['details'] if d['offer_type'] == 'standard'
        )
        self.assertEqual(standard_detail['title'], "Standard Design")
        premium_detail = next(
            d for d in response.data['details'] if d['offer_type'] == 'premium'
        )
        self.assertEqual(premium_detail['title'], "Premium Design")

    # Test cases for authentication
    def test_patch_offer_unauthenticated(self):
        patch_data = {"title": "Unauthenticated Update"}
        response = self.client.patch(self.url, patch_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Test cases for ownership
    def test_patch_offer_not_owner(self):
        self.client.login(username='otheruser', password='otherpass')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.other_token.key)
        patch_data = {"title": "Not Owner Update"}
        response = self.client.patch(self.url, patch_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Test cases for non-existent offer
    def test_patch_offer_not_found(self):
        self.client.login(username='patchuser', password='patchpass')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = reverse('offer-detail', args=[99999])
        patch_data = {"title": "Not Found"}
        response = self.client.patch(url, patch_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Test cases for invalid detail data
    def test_patch_offer_invalid_details(self):
        self.client.login(username='patchuser', password='patchpass')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        patch_data = {
            "details": [
                {
                    "id": self.detail_basic.id,
                    "title": "Invalid Detail"
                    # offer_type fehlt!
                }
            ]
        }
        response = self.client.patch(self.url, patch_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Test cases for partial update
    def test_patch_offer_partial_update(self):
        self.client.login(username='patchuser', password='patchpass')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        patch_data = {"description": "Nur die Beschreibung wurde geändert."}
        response = self.client.patch(self.url, patch_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], "Nur die Beschreibung wurde geändert.")
        self.assertEqual(response.data['title'], "Grafikdesign-Paket")
