from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from offers_app.models import Offer, OfferDetail
from orders_app.models import Order
from profiles_app.models import UserProfile


def make_user(username, user_type, password='Test1234!', is_staff=False):
    user = User.objects.create_user(username=username, password=password, is_staff=is_staff)
    UserProfile.objects.create(user=user, type=user_type)
    token, _ = Token.objects.get_or_create(user=user)
    return user, token.key


def create_offer_with_details(business_user):
    offer = Offer.objects.create(user=business_user, title='Test Offer', description='desc')
    detail = OfferDetail.objects.create(
        offer=offer, title='Basic', revisions=1,
        delivery_time_in_days=3, price='49.99',
        features=[], offer_type='basic',
    )
    return offer, detail


def create_order(customer_user, business_user):
    return Order.objects.create(
        customer_user=customer_user,
        business_user=business_user,
        title='Test Order',
        revisions=1,
        delivery_time_in_days=3,
        price='49.99',
        features=[],
        offer_type='basic',
        status=Order.IN_PROGRESS,
    )


class OrderListTests(APITestCase):
    """Tests for GET /api/orders/"""

    def setUp(self):
        self.customer, self.customer_token = make_user('cust', 'customer')
        self.business, self.business_token = make_user('biz', 'business')
        create_order(self.customer, self.business)
        self.url = reverse('order-list-create')

    def test_get_orders_as_customer_returns_200(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_orders_without_token_returns_401(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class OrderCreateTests(APITestCase):
    """Tests for POST /api/orders/"""

    def setUp(self):
        self.customer, self.customer_token = make_user('cust', 'customer')
        self.business, self.business_token = make_user('biz', 'business')
        _, self.offer_detail = create_offer_with_details(self.business)
        self.url = reverse('order-list-create')

    def test_post_order_as_customer_returns_201(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token)
        response = self.client.post(self.url, {'offer_detail_id': self.offer_detail.pk}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_order_as_business_returns_403(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token)
        response = self.client.post(self.url, {'offer_detail_id': self.offer_detail.pk}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_order_without_token_returns_401(self):
        response = self.client.post(self.url, {'offer_detail_id': self.offer_detail.pk}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_order_with_nonexistent_offer_detail_returns_400(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token)
        response = self.client.post(self.url, {'offer_detail_id': 9999}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class OrderUpdateTests(APITestCase):
    """Tests for PATCH /api/orders/<pk>/"""

    def setUp(self):
        self.customer, self.customer_token = make_user('cust', 'customer')
        self.business, self.business_token = make_user('biz', 'business')
        self.other_business, self.other_token = make_user('biz2', 'business')
        self.order = create_order(self.customer, self.business)
        self.url = reverse('order-detail', kwargs={'pk': self.order.pk})

    def test_patch_order_as_assigned_business_returns_200(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token)
        response = self.client.patch(self.url, {'status': Order.COMPLETED}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_order_as_other_business_returns_403(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.other_token)
        response = self.client.patch(self.url, {'status': Order.COMPLETED}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_order_without_token_returns_401(self):
        response = self.client.patch(self.url, {'status': Order.COMPLETED}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class OrderDeleteTests(APITestCase):
    """Tests for DELETE /api/orders/<pk>/"""

    def setUp(self):
        self.customer, self.customer_token = make_user('cust', 'customer')
        self.business, self.business_token = make_user('biz', 'business')
        self.admin, self.admin_token = make_user('admin', 'customer', is_staff=True)
        self.order = create_order(self.customer, self.business)
        self.url = reverse('order-detail', kwargs={'pk': self.order.pk})

    def test_delete_order_as_admin_returns_204(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_order_as_normal_user_returns_403(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class OrderCountTests(APITestCase):
    """Tests for GET /api/order-count/<business_user_id>/ and /api/completed-order-count/<business_user_id>/"""

    def setUp(self):
        self.customer, self.customer_token = make_user('cust', 'customer')
        self.business, self.business_token = make_user('biz', 'business')
        create_order(self.customer, self.business)

    def test_get_order_count_returns_200(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token)
        url = reverse('order-count', kwargs={'business_user_id': self.business.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('order_count', response.data)

    def test_get_completed_order_count_returns_200(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token)
        url = reverse('completed-order-count', kwargs={'business_user_id': self.business.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('completed_order_count', response.data)

    def test_get_order_count_nonexistent_business_returns_404(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token)
        url = reverse('order-count', kwargs={'business_user_id': 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
