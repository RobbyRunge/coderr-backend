from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token

from profiles_app.models import Profile


class ProfileDetailAPITest(APITestCase):
    """
    Test suite for retrieving and updating user profiles via the API.
    """
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass',
            email='test@mail.com'
        )
        self.token = Token.objects.create(user=self.user)
        self.profile = Profile.objects.create(
            user=self.user,
            username='testuser',
            first_name='Test',
            last_name='User',
            location='Test City',
            tel='123456789',
            description='Test description',
            working_hours='9-17',
            type='business',
            email='test@mail.com'
        )
        self.url = reverse('profile-detail', kwargs={'pk': self.profile.pk})

    # Test that authentication is required to access the profile detail view
    def test_profile_detail_requires_authentication(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Test that the profile detail view is accessible to authenticated users
    def test_profile_detail_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')
        self.assertEqual(response.data['first_name'], 'Test')
        self.assertEqual(response.data['last_name'], 'User')
        self.assertEqual(response.data['location'], 'Test City')
        self.assertEqual(response.data['tel'], '123456789')
        self.assertEqual(response.data['description'], 'Test description')
        self.assertEqual(response.data['working_hours'], '9-17')
        self.assertEqual(response.data['type'], 'business')
        self.assertEqual(response.data['email'], 'test@mail.com')

    # Test that certain fields are never null in the response
    def test_profile_detail_fields_never_null(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.profile.first_name = None
        self.profile.last_name = None
        self.profile.location = None
        self.profile.tel = None
        self.profile.description = None
        self.profile.working_hours = None
        self.profile.save()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for field in [
            'first_name', 'last_name',
            'location', 'tel',
            'description', 'working_hours'
        ]:
            self.assertEqual(response.data[field], '')

    # Test that only the owner can update their profile
    def test_profile_patch_only_owner(self):
        User = get_user_model()
        other_user = User.objects.create_user(
            username='otheruser',
            password='otherpass',
            email='other@mail.com'
        )
        other_token = Token.objects.create(user=other_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + other_token.key)
        response = self.client.patch(self.url, {'first_name': 'Hacker'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Test that the owner can update their profile
    def test_profile_patch_owner(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.patch(self.url, {'first_name': 'Updated'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.first_name, 'Updated')

    # Test that GET on non-existent profile returns 404
    def test_profile_detail_not_found(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        non_existent_url = reverse('profile-detail', kwargs={'pk': 9999})
        response = self.client.get(non_existent_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Test that authenticated user can view other users' profiles
    def test_profile_detail_accessible_by_other_user(self):
        User = get_user_model()
        other_user = User.objects.create_user(
            username='otheruser',
            password='otherpass',
            email='other@mail.com'
        )
        other_token = Token.objects.create(user=other_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + other_token.key)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')

    # Test that PATCH with invalid data returns 400
    def test_profile_patch_invalid_data(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.patch(
            self.url,
            {'email': 'not-a-valid-email'}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
