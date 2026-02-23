from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from profiles_app.models import UserProfile


class ProfileDetailTests(APITestCase):
    """Tests for GET/PATCH /api/profile/<pk>/"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='owner', password='Test1234!', email='owner@test.de'
        )
        self.profile = UserProfile.objects.create(user=self.user, type='customer')

        self.other_user = User.objects.create_user(
            username='other', password='Test1234!', email='other@test.de'
        )
        self.other_profile = UserProfile.objects.create(user=self.other_user, type='business')

        token, _ = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_get_own_profile_returns_200(self):
        url = reverse('profile-detail', kwargs={'pk': self.user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_other_profile_returns_200(self):
        url = reverse('profile-detail', kwargs={'pk': self.other_user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_nonexistent_profile_returns_404(self):
        url = reverse('profile-detail', kwargs={'pk': 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_profile_without_token_returns_401(self):
        self.client.credentials()
        url = reverse('profile-detail', kwargs={'pk': self.user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_own_profile_returns_200(self):
        url = reverse('profile-detail', kwargs={'pk': self.user.pk})
        response = self.client.patch(url, {'location': 'Berlin'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_other_profile_returns_403(self):
        url = reverse('profile-detail', kwargs={'pk': self.other_user.pk})
        response = self.client.patch(url, {'location': 'Hamburg'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_profile_without_token_returns_401(self):
        self.client.credentials()
        url = reverse('profile-detail', kwargs={'pk': self.user.pk})
        response = self.client.patch(url, {'location': 'Berlin'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class BusinessProfileListTests(APITestCase):
    """Tests for GET /api/profiles/business/"""

    def setUp(self):
        self.user = User.objects.create_user(username='biz', password='Test1234!')
        UserProfile.objects.create(user=self.user, type='business')
        token, _ = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_get_business_profiles_returns_200(self):
        url = reverse('business-profiles')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    def test_get_business_profiles_without_token_returns_401(self):
        self.client.credentials()
        url = reverse('business-profiles')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CustomerProfileListTests(APITestCase):
    """Tests for GET /api/profiles/customer/"""

    def setUp(self):
        self.user = User.objects.create_user(username='cust', password='Test1234!')
        UserProfile.objects.create(user=self.user, type='customer')
        token, _ = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_get_customer_profiles_returns_200(self):
        url = reverse('customer-profiles')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    def test_get_customer_profiles_without_token_returns_401(self):
        self.client.credentials()
        url = reverse('customer-profiles')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
