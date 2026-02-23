from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from offers_app.models import Offer, OfferDetail
from profiles_app.models import UserProfile


VALID_DETAILS = [
    {'title': 'Basic', 'revisions': 1, 'delivery_time_in_days': 3, 'price': '49.99', 'features': [], 'offer_type': 'basic'},
    {'title': 'Standard', 'revisions': 3, 'delivery_time_in_days': 5, 'price': '99.99', 'features': [], 'offer_type': 'standard'},
    {'title': 'Premium', 'revisions': 5, 'delivery_time_in_days': 7, 'price': '149.99', 'features': [], 'offer_type': 'premium'},
]


def make_business_user(username, password='Test1234!'):
    user = User.objects.create_user(username=username, password=password)
    UserProfile.objects.create(user=user, type='business')
    token, _ = Token.objects.get_or_create(user=user)
    return user, token.key


def make_customer_user(username, password='Test1234!'):
    user = User.objects.create_user(username=username, password=password)
    UserProfile.objects.create(user=user, type='customer')
    token, _ = Token.objects.get_or_create(user=user)
    return user, token.key


def create_offer(user):
    offer = Offer.objects.create(user=user, title='Test Offer', description='A test offer')
    OfferDetail.objects.create(offer=offer, title='Basic', revisions=1, delivery_time_in_days=3, price='49.99', features=[], offer_type='basic')
    OfferDetail.objects.create(offer=offer, title='Standard', revisions=3, delivery_time_in_days=5, price='99.99', features=[], offer_type='standard')
    OfferDetail.objects.create(offer=offer, title='Premium', revisions=5, delivery_time_in_days=7, price='149.99', features=[], offer_type='premium')
    return offer


class OfferListTests(APITestCase):
    """Tests for GET /api/offers/"""

    def setUp(self):
        self.business_user, self.token = make_business_user('biz')
        self.offer = create_offer(self.business_user)
        self.url = reverse('offer-list-create')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_get_all_offers_returns_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_by_creator_id_returns_200(self):
        response = self.client.get(self.url, {'creator_id': self.business_user.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for result in response.data:
            self.assertEqual(result['user'], self.business_user.pk)

    def test_filter_by_min_price_returns_200(self):
        response = self.client.get(self.url, {'min_price': 50})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_by_max_delivery_time_returns_200(self):
        response = self.client.get(self.url, {'max_delivery_time': 5})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_returns_200(self):
        response = self.client.get(self.url, {'search': 'Test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_ordering_returns_200(self):
        response = self.client.get(self.url, {'ordering': '-updated_at'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class OfferRetrieveTests(APITestCase):
    """Tests for GET /api/offers/<pk>/"""

    def setUp(self):
        self.business_user, self.token = make_business_user('biz')
        self.offer = create_offer(self.business_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_get_single_offer_returns_200(self):
        url = reverse('offer-detail', kwargs={'pk': self.offer.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_nonexistent_offer_returns_404(self):
        url = reverse('offer-detail', kwargs={'pk': 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class OfferCreateTests(APITestCase):
    """Tests for POST /api/offers/"""

    def setUp(self):
        self.business_user, self.business_token = make_business_user('biz')
        self.customer_user, self.customer_token = make_customer_user('cust')
        self.url = reverse('offer-list-create')
        self.valid_data = {'title': 'New Offer', 'description': 'Great offer', 'details': VALID_DETAILS}

    def test_post_offer_as_business_returns_201(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token)
        response = self.client.post(self.url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_offer_as_customer_returns_403(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token)
        response = self.client.post(self.url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_offer_without_token_returns_401(self):
        response = self.client.post(self.url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_offer_with_less_than_3_details_returns_400(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token)
        data = {**self.valid_data, 'details': VALID_DETAILS[:2]}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_offer_with_wrong_offer_type_returns_400(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token)
        bad_details = [
            {**VALID_DETAILS[0], 'offer_type': 'basic'},
            {**VALID_DETAILS[1], 'offer_type': 'basic'},
            {**VALID_DETAILS[2], 'offer_type': 'basic'},
        ]
        data = {**self.valid_data, 'details': bad_details}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class OfferUpdateDeleteTests(APITestCase):
    """Tests for PATCH/DELETE /api/offers/<pk>/"""

    def setUp(self):
        self.business_user, self.business_token = make_business_user('biz')
        self.other_business_user, self.other_token = make_business_user('biz2')
        self.offer = create_offer(self.business_user)
        self.url = reverse('offer-detail', kwargs={'pk': self.offer.pk})

    def test_patch_own_offer_returns_200(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token)
        response = self.client.patch(self.url, {'title': 'Updated Title'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_other_offer_returns_403(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.other_token)
        response = self.client.patch(self.url, {'title': 'Hacked'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_offer_without_token_returns_401(self):
        response = self.client.patch(self.url, {'title': 'No Auth'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_own_offer_returns_204(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_other_offer_returns_403(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.other_token)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class OfferDetailRetrieveTests(APITestCase):
    """Tests for GET /api/offerdetails/<pk>/"""

    def setUp(self):
        self.business_user, self.token = make_business_user('biz')
        self.offer = create_offer(self.business_user)
        self.offer_detail = self.offer.details.filter(offer_type='basic').first()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_get_offer_detail_returns_200(self):
        url = reverse('offerdetail-detail', kwargs={'pk': self.offer_detail.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_nonexistent_offer_detail_returns_404(self):
        url = reverse('offerdetail-detail', kwargs={'pk': 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
