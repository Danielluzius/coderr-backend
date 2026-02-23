from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from profiles_app.models import UserProfile
from reviews_app.models import Review


def make_user(username, user_type, password='Test1234!'):
    user = User.objects.create_user(username=username, password=password)
    UserProfile.objects.create(user=user, type=user_type)
    token, _ = Token.objects.get_or_create(user=user)
    return user, token.key


def create_review(reviewer, business_user, rating=4, description='Great work!'):
    return Review.objects.create(
        reviewer=reviewer,
        business_user=business_user,
        rating=rating,
        description=description,
    )


class ReviewListTests(APITestCase):
    """Tests for GET /api/reviews/"""

    def setUp(self):
        self.customer, self.customer_token = make_user('cust', 'customer')
        self.business, self.business_token = make_user('biz', 'business')
        create_review(self.customer, self.business)
        self.url = reverse('review-list-create')

    def test_get_reviews_returns_200(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_reviews_without_token_returns_401(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_filter_by_business_user_id_returns_200(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token)
        response = self.client.get(self.url, {'business_user_id': self.business.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for result in response.data:
            self.assertEqual(result['business_user'], self.business.pk)

    def test_filter_by_reviewer_id_returns_200(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token)
        response = self.client.get(self.url, {'reviewer_id': self.customer.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for result in response.data:
            self.assertEqual(result['reviewer'], self.customer.pk)

    def test_ordering_returns_200(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token)
        response = self.client.get(self.url, {'ordering': '-updated_at'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ReviewCreateTests(APITestCase):
    """Tests for POST /api/reviews/"""

    def setUp(self):
        self.customer, self.customer_token = make_user('cust', 'customer')
        self.business, self.business_token = make_user('biz', 'business')
        self.url = reverse('review-list-create')
        self.valid_data = {
            'business_user': self.business.pk,
            'rating': 5,
            'description': 'Excellent!',
        }

    def test_post_review_as_customer_returns_201(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token)
        response = self.client.post(self.url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_review_as_business_returns_403(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token)
        response = self.client.post(self.url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_review_without_token_returns_401(self):
        response = self.client.post(self.url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_duplicate_review_returns_400(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token)
        self.client.post(self.url, self.valid_data, format='json')
        response = self.client.post(self.url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_review_with_invalid_rating_returns_400(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token)
        data = {**self.valid_data, 'rating': 6}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ReviewUpdateTests(APITestCase):
    """Tests for PATCH /api/reviews/<pk>/"""

    def setUp(self):
        self.customer, self.customer_token = make_user('cust', 'customer')
        self.other_customer, self.other_token = make_user('cust2', 'customer')
        self.business, _ = make_user('biz', 'business')
        self.review = create_review(self.customer, self.business)
        self.url = reverse('review-detail', kwargs={'pk': self.review.pk})

    def test_patch_own_review_returns_200(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token)
        response = self.client.patch(self.url, {'rating': 3}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_other_review_returns_403(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.other_token)
        response = self.client.patch(self.url, {'rating': 1}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_review_without_token_returns_401(self):
        response = self.client.patch(self.url, {'rating': 3}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ReviewDeleteTests(APITestCase):
    """Tests for DELETE /api/reviews/<pk>/"""

    def setUp(self):
        self.customer, self.customer_token = make_user('cust', 'customer')
        self.other_customer, self.other_token = make_user('cust2', 'customer')
        self.business, _ = make_user('biz', 'business')
        self.review = create_review(self.customer, self.business)
        self.url = reverse('review-detail', kwargs={'pk': self.review.pk})

    def test_delete_own_review_returns_204(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_other_review_returns_403(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.other_token)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_review_without_token_returns_401(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
