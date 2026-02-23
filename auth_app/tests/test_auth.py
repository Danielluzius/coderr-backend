from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from profiles_app.models import UserProfile


class RegistrationTests(APITestCase):
    """Tests for POST /api/registration/"""

    def setUp(self):
        self.url = reverse('registration')
        self.valid_data = {
            'username': 'newuser',
            'email': 'new@test.de',
            'password': 'Test1234!',
            'repeated_password': 'Test1234!',
            'type': 'customer',
        }

    def test_registration_success(self):
        response = self.client.post(self.url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        self.assertIn('user_id', response.data)
        self.assertEqual(response.data['username'], 'newuser')
        self.assertEqual(response.data['email'], 'new@test.de')
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertTrue(UserProfile.objects.filter(user__username='newuser', type='customer').exists())

    def test_registration_passwords_do_not_match(self):
        data = {**self.valid_data, 'repeated_password': 'wrongpassword'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_missing_field(self):
        data = {**self.valid_data}
        data.pop('username')
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_duplicate_username(self):
        self.client.post(self.url, self.valid_data, format='json')
        response = self.client.post(self.url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_invalid_type(self):
        data = {**self.valid_data, 'type': 'invalid'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginTests(APITestCase):
    """Tests for POST /api/login/"""

    def setUp(self):
        self.url = reverse('login')
        self.user = User.objects.create_user(
            username='testuser', password='Test1234!', email='test@test.de'
        )
        UserProfile.objects.create(user=self.user, type='customer')

    def test_login_success(self):
        response = self.client.post(self.url, {'username': 'testuser', 'password': 'Test1234!'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('user_id', response.data)
        self.assertEqual(response.data['username'], 'testuser')

    def test_login_wrong_password(self):
        response = self.client.post(self.url, {'username': 'testuser', 'password': 'wrongpass'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_nonexistent_user(self):
        response = self.client.post(self.url, {'username': 'nobody', 'password': 'Test1234!'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_missing_fields(self):
        response = self.client.post(self.url, {'username': 'testuser'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
