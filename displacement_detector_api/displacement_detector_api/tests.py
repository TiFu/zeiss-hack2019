from django.test import TestCase


class UsersTestcase(TestCase):
    def test_endpoint_returns_200(self):
        response = self.client.get('/users/')
        assert response.status_code == 200

class AdminTestcase(TestCase):
    def test_endpoint_returns_200(self):
        response = self.client.get('/admin/')
        assert response.status_code == 302
