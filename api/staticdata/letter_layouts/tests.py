from rest_framework import status
from rest_framework.reverse import reverse

from api.staticdata.letter_layouts.models import LetterLayout
from test_helpers.clients import DataTestClient
from test_helpers.test_endpoints.test_endpoint_response_time import EndPointTests


class LetterLayoutsTests(DataTestClient):
    def setUp(self):
        super().setUp()
        self.letter_layout = LetterLayout.objects.first()

    def test_get_letter_layouts_success(self):
        url = reverse("staticdata:letter_layouts:letter_layouts")
        response = self.client.get(url, **self.exporter_headers)
        response_data = response.json()["results"][0]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data["id"], str(self.letter_layout.id))
        self.assertEqual(response_data["filename"], self.letter_layout.filename)
        self.assertEqual(response_data["name"], self.letter_layout.name)

    def test_get_letter_layout_success(self):
        url = reverse("staticdata:letter_layouts:letter_layout", kwargs={"pk": self.letter_layout.id})
        response = self.client.get(url, **self.exporter_headers)
        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data["id"], str(self.letter_layout.id))
        self.assertEqual(response_data["filename"], self.letter_layout.filename)
        self.assertEqual(response_data["name"], self.letter_layout.name)


class LetterLayoutsResponseTests(EndPointTests):
    url = "/static/letter-layouts/"

    def test_letter_layouts(self):
        self.call_endpoint(self.get_exporter_headers(), self.url)
