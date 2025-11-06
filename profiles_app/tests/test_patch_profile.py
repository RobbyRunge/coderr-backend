from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token

from profiles_app.models import Profile


class PatchProfileAPITest(APITestCase):
    """
    Test suite for patching user profiles via the API.
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

    # Test that patching the profile works correctly
    def test_patch_profile_success(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        data = {
            "first_name": "Max",
            "last_name": "Mustermann",
            "location": "Berlin",
            "tel": "987654321",
            "description": "Updated business description",
            "working_hours": "10-18",
            "email": "new_email@business.de"
        }
        response = self.client.patch(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "Max")
        self.assertEqual(response.data["last_name"], "Mustermann")
        self.assertEqual(response.data["location"], "Berlin")
        self.assertEqual(response.data["tel"], "987654321")
        self.assertEqual(response.data["description"], "Updated business description")
        self.assertEqual(response.data["working_hours"], "10-18")
        self.assertEqual(response.data["email"], "new_email@business.de")
        for field in [
            "first_name", "last_name",
            "location", "tel",
            "description", "working_hours"
        ]:
            self.assertIsNotNone(response.data[field])

    # Test that fields set to null are returned as empty strings
    def test_patch_profile_field_set_to_null(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        data = {
            "first_name": None,
            "last_name": "Mustermann"
        }
        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "")
        self.assertEqual(response.data["last_name"], "Mustermann")

    # Test that omitted fields are returned as non-null
    def test_patch_profile_field_omitted(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        data = {
            # "first_name" is omitted
            "last_name": "Mustermann"
        }
        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data["first_name"])
        self.assertEqual(response.data["first_name"], "Test")
        self.assertEqual(response.data["last_name"], "Mustermann")

    # Test that a user cannot patch another user's profile
    def test_patch_profile_other_user_forbidden(self):
        """
        Tests that a user cannot patch another user's profile
        (should return 403).
        """
        # Create a second user and profile
        User = get_user_model()
        other_user = User.objects.create_user(
            username='otheruser',
            password='otherpass',
            email='other@mail.com'
        )
        other_profile = Profile.objects.create(
            user=other_user,
            username='otheruser',
            first_name='Other',
            last_name='User',
            location='Other City',
            tel='000000000',
            description='Other description',
            working_hours='8-16',
            type='business',
            email='other@mail.com'
        )
        url = reverse('profile-detail', kwargs={'pk': other_profile.pk})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        data = {"first_name": "Hacker"}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Test that an unauthenticated user cannot patch any profile
    def test_patch_profile_unauthenticated(self):
        """
        Tests that an unauthenticated user cannot patch any profile
        (should return 401).
        """
        data = {"first_name": "Anonymous"}
        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)