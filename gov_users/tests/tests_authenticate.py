from django.urls import reverse
from parameterized import parameterized
from rest_framework import status
from rest_framework.utils import json

from gov_users.enums import GovUserStatuses
from test_helpers.clients import DataTestClient


class GovUserAuthenticateTests(DataTestClient):

    url = reverse('gov_users:authenticate')

    def test_authentication_success(self):
        """
        Authorises user then checks the token which is sent is valid upon another request
        """
        data = {
            'email': self.gov_user.email,
            'first_name': self.gov_user.first_name,
            'last_name': self.gov_user.last_name
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content)
        headers = {'HTTP_GOV_USER_TOKEN': response_data['token']}
        url = reverse('gov_users:gov_users')
        response = self.client.get(url, **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_empty(self):
        data = {
            'email': None,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_login_incorrect_details(self):
        data = {
            'email': 'something@random.com',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_a_deactivated_user_cannot_log_in(self):
        self.gov_user.status = GovUserStatuses.DEACTIVATED
        self.gov_user.save()
        data = {
            'email': self.gov_user.email,
            'first_name': self.gov_user.first_name,
            'last_name': self.gov_user.last_name
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @parameterized.expand([
        [{'headers': {'HTTP_GOV_USER_EMAIL': str('test@mail.com')}, 'response': status.HTTP_200_OK}],
        [{'headers': {}, 'response': status.HTTP_403_FORBIDDEN}],
        [{'headers': {'HTTP_GOV_USER_EMAIL': str('sadkjaf@asdasdf.casdas')}, 'response': status.HTTP_403_FORBIDDEN}],
    ])
    def test_authorised_valid_email_in_header(self, data):
        url = reverse('gov_users:gov_users')
        headers = data['headers']
        response = self.client.get(url, **headers)
        self.assertEqual(response.status_code, data['response'])