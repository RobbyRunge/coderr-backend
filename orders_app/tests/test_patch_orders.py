from django.utils import timezone

from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from auth_app.models import CustomUser
from offers_app.models import OfferDetail, Offer
from orders_app.models import Order


class OrderPatchAPITest(APITestCase):
    """
    Test case for updating the status of an existing order.
    """
    def setUp(self):
        # Create test users
        self.customer_user = CustomUser.objects.create_user(
            username='customeruser',
            password='customerpass',
        )
        self.business_user = CustomUser.objects.create_user(
            username='businessuser',
            password='businesspass',
        )
        Token.objects.create(user=self.customer_user)
        Token.objects.create(user=self.business_user)

        # Create test offer and offer detail
        self.offer = Offer.objects.create(
            user=self.business_user,
            title="Test Offer",
            description="Test Description",
        )
        self.offer_detail = OfferDetail.objects.create(
            offer=self.offer,
            title="Test Offer Detail",
            revisions=2,
            delivery_time_in_days=7,
            price=300,
            features=[],
            offer_type="standard",
        )

        # Create test order
        self.order = Order.objects.create(
            customer_user=self.customer_user,
            business_user=self.business_user,
            title="Test Order",
            revisions=2,
            delivery_time_in_days=7,
            price=300,
            features=[],
            offer_type="standard",
            status="in_progress",
            created_at=timezone.now(),
            updated_at=timezone.now()
        )

    # Test cases for patching order status
    def test_patch_order_status(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user=self.business_user).key)
        url = f'/api/orders/{self.order.id}/'
        data = {
            'status': 'completed'
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'completed')
