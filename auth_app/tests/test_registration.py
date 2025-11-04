from rest_framework.test import APITestCase


class TestRegistrationAPI(APITestCase):
    """
    Test cases for the Registration API endpoint.
    Tests:
        - Successful registration
        - Missing fields (username, email, password, repeated_password, type)
        - Password mismatch
        - Duplicate username
    """

    def setUp(self):
        self.register_url = '/api/registration/'

    # Test cases for registration
    def test_registration_success(self):
        """
        Test successful registration with valid data.
        """
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword',
            'repeated_password': 'testpassword',
            'type': 'customer'
        }
        response = self.client.post(
            self.register_url, self.user_data, format='json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['username'], 'testuser')
        self.assertEqual(response.data['email'], 'testuser@example.com')

    # Test cases for missing fields
    def test_registration_missing_fields(self):
        """
        Test registration failure with missing fields.
        """
        incomplete_data = {
            # Missing username
            'email': 'testuser@example.com',
            'password': 'testpassword',
            'repeated_password': 'testpassword',
            'type': 'customer'
        }
        response = self.client.post(
            self.register_url, incomplete_data, format='json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('username', response.data)
        self.assertIn(
            'This field is required.',
            str(response.data['username'])
        )

    # Test cases for password mismatch
    def test_registration_password_mismatch(self):
        """
        Test registration failure when passwords do not match.
        """
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword',
            'repeated_password': 'differentpassword',
            'type': 'customer'
        }
        response = self.client.post(
            self.register_url, self.user_data, format='json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('non_field_errors', response.data)
        self.assertIn(
            'Passwords do not match.',
            str(response.data['non_field_errors'])
        )

    # Test cases for duplicate username
    def test_registration_duplicate_username(self):
        """
        Test registration failure with duplicate username.
        """
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword',
            'repeated_password': 'testpassword',
            'type': 'customer'
        }
        self.client.post(self.register_url, self.user_data, format='json')
        response = self.client.post(
            self.register_url, self.user_data, format='json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('non_field_errors', response.data)
        self.assertIn(
            'Username already taken.',
            str(response.data['non_field_errors'])
        )
