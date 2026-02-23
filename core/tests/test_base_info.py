from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from offers_app.models import Offer, OfferDetail
from profiles_app.models import UserProfile
from reviews_app.models import Review


class BaseInfoTests(APITestCase):
    """Tests for GET /api/base-info/"""

    def setUp(self):
        self.url = reverse('base-info')

        business_user = User.objects.create_user(username='biz', password='Test1234!')
        UserProfile.objects.create(user=business_user, type='business')

        customer_user = User.objects.create_user(username='cust', password='Test1234!')
        UserProfile.objects.create(user=customer_user, type='customer')

        offer = Offer.objects.create(user=business_user, title='Test Offer', description='desc')
        OfferDetail.objects.create(
            offer=offer, title='Basic', revisions=1,
            delivery_time_in_days=3, price='49.99',
            features=[], offer_type='basic',
        )

        Review.objects.create(
            reviewer=customer_user,
            business_user=business_user,
            rating=4,
            description='Great!',
        )

    def test_get_base_info_returns_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_base_info_returns_correct_fields(self):
        response = self.client.get(self.url)
        self.assertIn('review_count', response.data)
        self.assertIn('average_rating', response.data)
        self.assertIn('business_profile_count', response.data)
        self.assertIn('offer_count', response.data)

    def test_get_base_info_returns_correct_values(self):
        response = self.client.get(self.url)
        self.assertEqual(response.data['review_count'], 1)
        self.assertEqual(response.data['average_rating'], 4.0)
        self.assertEqual(response.data['business_profile_count'], 1)
        self.assertEqual(response.data['offer_count'], 1)

    def test_get_base_info_accessible_without_token(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
