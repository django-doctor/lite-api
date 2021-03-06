from django.urls import reverse
from rest_framework import status

from api.core import constants
from api.users.tests.factories import GovUserFactory
from test_helpers.clients import DataTestClient
from api.users.models import GovUser, Permission


class SuperUserTests(DataTestClient):
    """
    Other related tests in:
        'gov_users/tests/tests_deactivate'
            for cannot deactive a super user
        'gov_users/tests/tests_roles_and_permissions'
            for actions requiring the role administrator permission
    """

    def test_super_user_role_cannot_be_edited(self):
        role_id = "00000000-0000-0000-0000-000000000002"
        url = reverse("gov_users:role", kwargs={"pk": role_id})

        data = {"permissions": [constants.GovPermissions.MANAGE_LICENCE_FINAL_ADVICE.name]}

        response = self.client.put(url, data, **self.gov_headers)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_super_user_roles_have_all_permissions(self):
        self.assertEqual(self.super_user_role.permissions.count(), Permission.internal.all().count())
        self.assertEqual(self.exporter_super_user_role.permissions.count(), Permission.exporter.all().count())

    def test_cannot_remove_super_user_role_from_yourself(self):
        self.gov_user.role = self.super_user_role
        self.gov_user.save()
        data = {"role": self.default_role.id}
        url = reverse("gov_users:gov_user", kwargs={"pk": self.gov_user.pk})

        response = self.client.put(url, data, **self.gov_headers)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_super_user_role_can_be_removed_by_a_super_user(self):
        valid_user = GovUserFactory(
            baseuser_ptr__email="test2@mail.com",
            baseuser_ptr__first_name="John",
            baseuser_ptr__last_name="Smith",
            team=self.team,
            role=self.super_user_role,
        )
        self.gov_user.role = self.super_user_role
        self.gov_user.save()
        data = {"role": self.default_role.id}
        url = reverse("gov_users:gov_user", kwargs={"pk": valid_user.pk})

        response = self.client.put(url, data, **self.gov_headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_super_user_role_cannot_be_removed_by_someone_without_super_user_role(self):
        valid_user = GovUserFactory(
            baseuser_ptr__email="test2@mail.com",
            baseuser_ptr__first_name="John",
            baseuser_ptr__last_name="Smith",
            team=self.team,
            role=self.super_user_role,
        )
        data = {"role": self.default_role.id}
        url = reverse("gov_users:gov_user", kwargs={"pk": valid_user.pk})

        response = self.client.put(url, data, **self.gov_headers)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_super_user_can_assign_super_user_role(self):
        valid_user = GovUserFactory(
            baseuser_ptr__email="test2@mail.com",
            baseuser_ptr__first_name="John",
            baseuser_ptr__last_name="Smith",
            team=self.team,
            role=self.super_user_role,
        )
        self.gov_user.role = self.super_user_role
        self.gov_user.save()
        data = {"role": self.super_user_role.id}
        url = reverse("gov_users:gov_user", kwargs={"pk": valid_user.pk})

        response = self.client.put(url, data, **self.gov_headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cannot_assign_super_user_without_super_user_role(self):
        valid_user = GovUserFactory(
            baseuser_ptr__email="test2@mail.com",
            baseuser_ptr__first_name="John",
            baseuser_ptr__last_name="Smith",
            team=self.team,
            role=self.super_user_role,
        )
        data = {"role": self.super_user_role.id}
        url = reverse("gov_users:gov_user", kwargs={"pk": valid_user.pk})

        response = self.client.put(url, data, **self.gov_headers)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
