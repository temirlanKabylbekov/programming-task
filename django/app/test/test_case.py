from django.test import TestCase
from rest_framework.test import APIClient

from app.test import Factory


class ApiUserTestCase(TestCase):
    c = APIClient()

    @classmethod
    def setUpClass(cls):
        cls.user = Factory.user()
        cls.c.force_authenticate(user=cls.user)
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.c.logout()
        super().tearDownClass()
