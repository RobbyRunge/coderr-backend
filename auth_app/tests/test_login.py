from rest_framework.test import APITestCase


class TestLoginAPI(APITestCase):
    """
    Test cases for the Login API endpoint.
    Tests:
        - Successful login
        - Invalid login (wrong password)
        - Missing fields (username or password)
        - Empty username field
    """

    def setUp(self):
        self.register_url = '/api/registration/'
        self.login_url = '/api/login/'

        # Register a test user
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword',
            'repeated_password': 'testpassword',
            'type': 'customer'
        }

        self.client.post(self.register_url, self.user_data, format='json')

    # Test cases for login
    def test_login_success(self):
        """
        Test successful login with valid credentials.
        """
        login_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['username'], 'testuser')
        self.assertEqual(response.data['email'], 'testuser@example.com')

    # test cases for invalid login (wrong password)
    def test_login_invalid_credentials(self):
        """
        Test login failure with invalid credentials.
        """
        login_data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.data)
        self.assertIn('Invalid credentials!', str(response.data['error']))

    # test cases for missing fields (username or password)
    def test_login_missing_fields(self):
        """
        Test login failure with missing fields.
        """
        login_data = {
            'username': 'testuser'
            # Missing password
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('password', response.data)

    # test cases for empty username field
    def test_login_empty_username(self):
        """
        Test login failure with empty username.
        """
        login_data = {
            'username': '',
            'password': 'testpassword'
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('username', response.data)
