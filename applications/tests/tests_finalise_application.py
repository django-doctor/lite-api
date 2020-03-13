from django.urls import reverse
from rest_framework import status

from applications.enums import LicenceDuration
from applications.libraries.licence import get_default_duration
from audit_trail.models import Audit
from audit_trail.payload import AuditType
from cases.enums import AdviceType, CaseTypeSubTypeEnum, CaseTypeEnum
from cases.models import CaseAssignment
from conf.constants import GovPermissions
from static.statuses.enums import CaseStatusEnum
from static.statuses.libraries.get_case_status import get_case_status_by_status
from static.statuses.models import CaseStatus
from test_helpers.clients import DataTestClient
from test_helpers.helpers import generate_key_value_pair
from users.models import Role
from lite_content.lite_api import strings


class FinaliseApplicationTests(DataTestClient):
    def setUp(self):
        super().setUp()
        self.standard_application = self.create_draft_standard_application(self.organisation)
        self.submit_application(self.standard_application)
        self.url = reverse("applications:finalise", kwargs={"pk": self.standard_application.id})
        self.role = Role.objects.create(name="test")
        self.finalised_status = CaseStatus.objects.get(status="finalised")

    def test_gov_user_finalise_permission_error(self):
        self.gov_user.role = self.role
        self.gov_user.role.permissions.set([])
        self.gov_user.save()

        data = {"licence_duration": 13}
        response = self.client.put(self.url, data=data, **self.gov_headers)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_gov_user_finalise_clearance_application_success(self):
        clearance_application = self.create_mod_clearance_application(
            self.organisation, case_type=CaseTypeEnum.EXHIBITION
        )

        self.gov_user.role = self.role
        self.gov_user.role.permissions.set(
            [GovPermissions.MANAGE_CLEARANCE_FINAL_ADVICE.name, GovPermissions.MANAGE_LICENCE_DURATION.name]
        )
        self.gov_user.save()

        licence_duration = 13
        data = {"licence_duration": licence_duration}
        url = reverse("applications:finalise", kwargs={"pk": clearance_application.pk})
        response = self.client.put(url, data=data, **self.gov_headers)

        clearance_application.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(clearance_application.status, get_case_status_by_status(CaseStatusEnum.FINALISED))
        self.assertEqual(clearance_application.licence_duration, data["licence_duration"])
        self.assertEqual(licence_duration, response.json()["licence_duration"])

    def test_gov_user_finalise_clearance_application_failure(self):
        """ Test failure in finalising a clearance application as the gov user does not have the
         permission.
        """
        clearance_application = self.create_mod_clearance_application(
            self.organisation, case_type=CaseTypeEnum.EXHIBITION
        )

        self.gov_user.role = self.role
        self.gov_user.role.permissions.set(
            [GovPermissions.MANAGE_LICENCE_FINAL_ADVICE.name, GovPermissions.MANAGE_LICENCE_DURATION.name]
        )
        self.gov_user.save()

        data = {"licence_duration": 13}
        url = reverse("applications:finalise", kwargs={"pk": clearance_application.pk})
        response = self.client.put(url, data=data, **self.gov_headers)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_gov_user_finalise_application_success(self):
        self.assertEqual(self.standard_application.licence_duration, None)

        self.gov_user.role = self.role
        self.gov_user.role.permissions.set(
            [GovPermissions.MANAGE_LICENCE_FINAL_ADVICE.name, GovPermissions.MANAGE_LICENCE_DURATION.name]
        )
        self.gov_user.save()

        data = {"licence_duration": 13}
        response = self.client.put(self.url, data=data, **self.gov_headers)

        self.standard_application.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.standard_application.status, get_case_status_by_status(CaseStatusEnum.FINALISED))
        self.assertEqual(self.standard_application.licence_duration, data["licence_duration"])

    def test_gov_user_finalise_application_removes_case_from_queues_and_users_from_case_success(self):
        """
        When a case is set to the finalised status, its assigned users, case officer and queues should be removed
        """
        self.standard_application.case_officer = self.gov_user
        self.standard_application.save()
        self.standard_application.queues.set([self.queue])
        case_assignment = CaseAssignment.objects.create(case=self.standard_application, queue=self.queue)
        case_assignment.users.set([self.gov_user])

        self.gov_user.role = self.role
        self.gov_user.role.permissions.set(
            [GovPermissions.MANAGE_LICENCE_FINAL_ADVICE.name, GovPermissions.MANAGE_LICENCE_DURATION.name]
        )
        self.gov_user.save()

        data = {"licence_duration": 13}
        response = self.client.put(self.url, data, **self.gov_headers)

        self.standard_application.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.standard_application.status, get_case_status_by_status(CaseStatusEnum.FINALISED))
        self.assertEqual(self.standard_application.licence_duration, data["licence_duration"])
        self.assertEqual(self.standard_application.queues.count(), 0)
        self.assertEqual(self.standard_application.case_officer, None)
        self.assertEqual(CaseAssignment.objects.filter(case=self.standard_application).count(), 0)

    def test_gov_use_set_duration_permission_denied(self):
        self.gov_user.role = self.role
        self.gov_user.role.permissions.set([GovPermissions.MANAGE_LICENCE_FINAL_ADVICE.name])
        self.gov_user.save()

        data = {"licence_duration": 13}
        response = self.client.put(self.url, data=data, **self.gov_headers)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.json(), {"errors": [strings.Applications.Generic.Finalise.Error.SET_DURATION_PERMISSION]}
        )

    def test_invalid_duration_data(self):
        self.gov_user.role = self.role
        self.gov_user.role.permissions.set(
            [GovPermissions.MANAGE_LICENCE_FINAL_ADVICE.name, GovPermissions.MANAGE_LICENCE_DURATION.name]
        )
        self.gov_user.save()

        data = {"licence_duration": LicenceDuration.MAX.value + 1}
        response = self.client.put(self.url, data=data, **self.gov_headers)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {"errors": {"non_field_errors": [strings.Applications.Generic.Finalise.Error.DURATION_RANGE]}},
        )

    def test_default_duration_no_permission_application_finalised_success(self):
        self.gov_user.role = self.role
        self.gov_user.role.permissions.set([GovPermissions.MANAGE_LICENCE_FINAL_ADVICE.name])
        self.gov_user.save()

        data = {"licence_duration": get_default_duration(self.standard_application)}
        response = self.client.put(self.url, data=data, **self.gov_headers)
        self.standard_application.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.standard_application.licence_duration, data["licence_duration"])

    def test_refuse_application_success(self):
        self.gov_user.role = self.role
        self.gov_user.role.permissions.set([GovPermissions.MANAGE_LICENCE_FINAL_ADVICE.name])
        self.gov_user.save()

        data = {"action": AdviceType.REFUSE}
        response = self.client.put(self.url, data=data, **self.gov_headers)
        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data["name"], self.standard_application.name)
        self.assertIsNone(response_data["licence_duration"])
        self.assertEqual(
            response_data["status"], generate_key_value_pair(self.finalised_status.status, CaseStatusEnum.choices)
        )
        self.assertEqual(
            Audit.objects.get(target_object_id=self.standard_application.id).verb, AuditType.FINALISED_APPLICATION.value
        )

    def test_grant_application_success(self):
        self.gov_user.role = self.role
        self.gov_user.role.permissions.set([GovPermissions.MANAGE_LICENCE_FINAL_ADVICE.name])
        self.gov_user.save()

        data = {"action": AdviceType.APPROVE}
        response = self.client.put(self.url, data=data, **self.gov_headers)
        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data["name"], self.standard_application.name)
        self.assertEqual(response_data["licence_duration"], get_default_duration(self.standard_application))
        self.assertEqual(
            response_data["status"], generate_key_value_pair(self.finalised_status.status, CaseStatusEnum.choices)
        )
        self.assertEqual(
            Audit.objects.get(target_object_id=self.standard_application.id).verb, AuditType.GRANTED_APPLICATION.value
        )
