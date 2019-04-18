from unittest.mock import patch

from app.nest import JsonArrayValidationError
from app.test import APIClient, ApiUserTestCase, mixer, status
from deposits.models import Deposit


def test_endpoint_requires_authorization():
    c = APIClient()
    got = c.post('/api/v1/deposit/', {'country': 'UK', 'city': 'London', 'currency': 'GBP', 'amount': 12.2}, format='json')
    assert got.status_code == status.HTTP_401_UNAUTHORIZED


def test_nesting_endpoint_requires_authorization():
    c = APIClient()
    got = c.post('/api/v1/deposit/nest/', {'keys_path': ['city']}, format='json')
    assert got.status_code == status.HTTP_401_UNAUTHORIZED


class TestDepositEndpoint(ApiUserTestCase):
    def test_creating_new_deposit(self):
        got = self.c.post('/api/v1/deposit/', {'country': 'UK', 'city': 'London', 'currency': 'GBP', 'amount': 12.2}, format='json')
        assert got.status_code == status.HTTP_201_CREATED
        assert Deposit.objects.filter(country='UK', city='London', currency='GBP', amount=12.2).exists() is True

    def test_updating_existing_deposit(self):
        deposit = mixer.blend('deposits.Deposit', amount=100)
        got = self.c.put(f'/api/v1/deposit/{deposit.id}/', {'amount': 100500}, format='json')
        assert got.status_code == status.HTTP_200_OK
        deposit.refresh_from_db()
        assert deposit.amount == 100500

    def test_deleting_deposit(self):
        deposit = mixer.blend('deposits.Deposit')
        self.c.delete(f'/api/v1/deposit/{deposit.id}/', format='json')
        assert Deposit.objects.filter(id=deposit.id).exists() is False

    def test_retrieving_deposit(self):
        deposit = mixer.blend('deposits.Deposit')
        got = self.c.get(f'/api/v1/deposit/{deposit.id}/', format='json')
        assert got.status_code == status.HTTP_200_OK
        assert got.json()['id'] == deposit.id

    def test_listing_deposits(self):
        deposit = mixer.blend('deposits.Deposit')
        got = self.c.get('/api/v1/deposit/', format='json')
        assert deposit.id in [item['id'] for item in got.json()['results']]

    @patch('deposits.views.nester')
    def test_nesting_deposit_successfully(self, nester_mock):
        nester_mock.return_value = {'London': [{'country': 'UK', 'amount': 10, 'currency': 'GBP'}]}
        got = self.c.post('/api/v1/deposit/nest/', {'keys_path': ['city']}, format='json')
        assert got.json() == {'London': [{'country': 'UK', 'amount': 10, 'currency': 'GBP'}]}

    @patch('deposits.views.nester')
    def test_nesting_deposit_with_validation_error(self, nester_mock):
        nester_mock.side_effect = JsonArrayValidationError('some validation error')
        got = self.c.post('/api/v1/deposit/nest/', {'keys_path': ['city']}, format='json')
        assert got.json() == {'error': 'some validation error'}
