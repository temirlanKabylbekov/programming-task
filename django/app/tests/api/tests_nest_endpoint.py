from unittest.mock import patch

from app.nest import JsonArrayValidationError
from app.test import APIClient, ApiUserTestCase, status


def test_nest_endpoint_requires_authentication():
    c = APIClient()
    got = c.post('/api/v1/nest/', {'json_array': [{'key1': 'value1', 'key2': 'value2'}], 'keys_path': ['key1']}, format='json')
    assert got.status_code == status.HTTP_401_UNAUTHORIZED


class TestNestEndpoint(ApiUserTestCase):
    def test_get_method_is_not_allowed(self):
        got = self.c.get('/api/v1/nest/')
        assert got.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_posting_invalid_json_array_param(self):
        got = self.c.post('/api/v1/nest/', {'json_array': 123, 'keys_path': ['key']}, format='json')
        assert got.status_code == status.HTTP_400_BAD_REQUEST

    def test_posting_invalid_keys_path_param(self):
        got = self.c.post('/api/v1/nest/', {'json_array': [{'key': 'value'}], 'keys_path': 'key'}, format='json')
        assert got.status_code == status.HTTP_400_BAD_REQUEST

    @patch('app.views.nester')
    def test_raising_nest_validation_error(self, nester_mock):
        nester_mock.side_effect = JsonArrayValidationError('some error msg')
        got = self.c.post('/api/v1/nest/', {'json_array': [{'key1': 'value1', 'key2': 'value2'}], 'keys_path': ['key1']}, format='json')
        assert got.json() == {'error': 'some error msg'}

    @patch('app.views.nester')
    def test_returning_success_json(self, nester_mock):
        nester_mock.return_value = {'value': [{'key2': 'value2'}]}
        got = self.c.post('/api/v1/nest/', {'json_array': [{'key1': 'value1', 'key2': 'value2'}], 'keys_path': ['key1']}, format='json')
        assert got.json() == {'value': [{'key2': 'value2'}]}
