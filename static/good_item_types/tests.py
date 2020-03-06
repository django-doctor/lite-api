from rest_framework import status
from rest_framework.reverse import reverse

from goods.enums import ItemType
from test_helpers.clients import DataTestClient


class ItemTypeTests(DataTestClient):

    url = reverse("static:item-types:item_types")

    def test_get_good_item_types(self):
        response = self.client.get(self.url)
        types = response.json()["item_types"]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(types["equipment"], "Equipment")
        self.assertEqual(len(types), len(ItemType.choices))