from django.contrib.contenttypes.models import ContentType
from django.urls import reverse_lazy
from parameterized import parameterized
from rest_framework import status

from cases.generated_documents.models import GeneratedCaseDocument
from cases.models import CaseNote, EcjuQuery
from test_helpers.clients import DataTestClient
from users.libraries.user_to_token import user_to_token
from users.models import ExporterNotification


class ExporterUserNotificationTests(DataTestClient):
    def setUp(self):
        super().setUp()
        self.case_note_content_type = ContentType.objects.get_for_model(CaseNote)
        self.ecju_query_content_type = ContentType.objects.get_for_model(EcjuQuery)
        self.generated_case_doc_content_type = ContentType.objects.get_for_model(GeneratedCaseDocument)

    def _create_all_case_types_with_notifications(self):
        self._create_end_user_advisory_query_with_notifications()
        self._create_application_with_notifications()
        self._create_clc_query_with_notifications()

    def _create_clc_query_with_notifications(self):
        clc_query = self.create_clc_query(description="this is a clc query", organisation=self.organisation)
        self.create_case_note(clc_query, "This is a test note 1", self.gov_user, True)
        self.create_case_note(clc_query, "This is a test note 2", self.gov_user, False)
        self.create_ecju_query(clc_query, "This is an ecju query")
        self.create_generated_case_document(clc_query, template=self.create_letter_template())
        return clc_query

    def _create_application_with_notifications(self):
        application = self.create_standard_application_case(self.organisation)
        self.create_case_note(application, "This is a test note 1", self.gov_user, True)
        self.create_case_note(application, "This is a test note 2", self.gov_user, False)
        self.create_ecju_query(application, "This is an ecju query")
        self.create_generated_case_document(application, template=self.create_letter_template())
        return application

    def _create_end_user_advisory_query_with_notifications(self):
        eua_query = self.create_end_user_advisory_case("note", "reasoning", self.organisation)
        self.create_case_note(eua_query, "This is a test note 1", self.gov_user, True)
        self.create_case_note(eua_query, "This is a test note 2", self.gov_user, False)
        self.create_ecju_query(eua_query, "This is an ecju query")
        self.create_generated_case_document(eua_query, template=self.create_letter_template())
        return eua_query

    @parameterized.expand(
        [
            [_create_application_with_notifications],
            [_create_clc_query_with_notifications],
            [_create_end_user_advisory_query_with_notifications],
        ]
    )
    def test_create_case_notifications_success(self, create_case_func):
        case = create_case_func(self)

        case_notification_count = ExporterNotification.objects.filter(
            user=self.exporter_user, organisation=self.exporter_user.organisation, case=case,
        ).count()
        case_case_note_notification_count = ExporterNotification.objects.filter(
            user=self.exporter_user,
            organisation=self.exporter_user.organisation,
            content_type=self.case_note_content_type,
            case=case,
        ).count()
        case_ecju_query_notification_count = ExporterNotification.objects.filter(
            user=self.exporter_user,
            organisation=self.exporter_user.organisation,
            content_type=self.ecju_query_content_type,
            case=case,
        ).count()
        case_generated_case_document_notification_count = ExporterNotification.objects.filter(
            user=self.exporter_user,
            organisation=self.exporter_user.organisation,
            content_type=self.generated_case_doc_content_type,
            case=case,
        ).count()

        self.assertEqual(case_notification_count, 3)
        self.assertEqual(case_case_note_notification_count, 1)
        self.assertEqual(case_ecju_query_notification_count, 1)
        self.assertEqual(case_generated_case_document_notification_count, 1)

    @parameterized.expand([[False], [True]])
    def test_get_notifications_for_user_with_and_without_count_only_param_success(self, count_only):
        self._create_all_case_types_with_notifications()

        response = self.client.get(
            reverse_lazy("users:notifications") + f"?count_only={count_only}", **self.exporter_headers
        )
        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual("notifications" in response_data and len(response_data["notifications"]) == 9, not count_only)
        self.assertEqual(response_data["notification_count"]["application"], 3)
        self.assertEqual(response_data["notification_count"]["end_user_advisory_query"], 3)
        self.assertEqual(response_data["notification_count"]["clc_query"], 3)

    @parameterized.expand([["application"], ["end_user_advisory_query"], ["clc_query"]])
    def test_get_notifications_for_user_individual_case_type_without_count_only_param_success(self, case_type):
        self._create_all_case_types_with_notifications()

        response = self.client.get(
            reverse_lazy("users:notifications") + f"?case_type={case_type}", **self.exporter_headers
        )
        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_data["notifications"]), 3)
        self.assertEqual(response_data["notification_count"][case_type], 3)

    @parameterized.expand([["application"], ["end_user_advisory_query"], ["clc_query"]])
    def test_get_notifications_for_user_individual_case_type_with_count_only_param_success(self, case_type):
        self._create_all_case_types_with_notifications()

        response = self.client.get(
            reverse_lazy("users:notifications") + f"?count_only=True&case_type={case_type}", **self.exporter_headers
        )
        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn("notifications", response_data)
        self.assertEqual(response_data["notification_count"][case_type], 3)

    def test_get_notifications_for_user_in_multiple_orgs_success(self):
        """
        Given an exporter user in multiple orgs
        When an API user gets notifications for the exporter user and one of their orgs
        Then only the notifications specific to that user and org combination are returned
        """
        self._create_application_with_notifications()

        org_2, _ = self.create_organisation_with_exporter_user("Org 2")
        self.add_exporter_user_to_org(org_2, self.exporter_user)
        self.exporter_headers = {
            "HTTP_EXPORTER_USER_TOKEN": user_to_token(self.exporter_user),
            "HTTP_ORGANISATION_ID": org_2.id,
        }
        application = self.create_standard_application_case(org_2)
        case_note = self.create_case_note(application, "This is a test note 3", self.gov_user, True)
        ecju_query = self.create_ecju_query(application, "This is an ecju query")
        notification_object_ids = [str(case_note.id), str(ecju_query.id)]

        response = self.client.get(reverse_lazy("users:notifications"), **self.exporter_headers)
        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data["notification_count"]["application"], 2)
        self.assertEqual(len(response_data["notifications"]), 2)
        # Check that the 2 notifications we got are the ones arising from notes on application 2, i.e. the application
        # created while org_2 is the currently selected org
        for data in response_data["notifications"]:
            self.assertTrue(data["object_id"] in notification_object_ids)

    def test_get_applications_with_notifications_success(self):
        self.exporter_user.set_role(self.organisation, self.exporter_super_user_role)
        self._create_application_with_notifications()

        response = self.client.get(reverse_lazy("applications:applications"), **self.exporter_headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        application_response_data = response.json()["results"][0]
        self.assertIn("exporter_user_notification_count", application_response_data)
        self.assertEqual(application_response_data["exporter_user_notification_count"]["total"], 3)

    def test_get_application_with_notifications_success(self):
        case = self._create_application_with_notifications()

        response = self.client.get(
            reverse_lazy("applications:application", kwargs={"pk": str(case.id)}), **self.exporter_headers
        )
        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("exporter_user_notification_count", response_data)
        self.assertEqual(len(response_data["exporter_user_notification_count"]), 3)

    def test_get_goods_with_notifications_success(self):
        self._create_clc_query_with_notifications()

        response = self.client.get(reverse_lazy("goods:goods"), **self.exporter_headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        good_response_data = response.json()["results"][0]["query"]
        self.assertIn("exporter_user_notification_count", good_response_data)
        self.assertEqual(good_response_data["exporter_user_notification_count"]["total"], 3)

    def test_get_good_with_notifications_success(self):
        case = self._create_clc_query_with_notifications()

        response = self.client.get(
            reverse_lazy("goods:good", kwargs={"pk": str(case.good_id)}), **self.exporter_headers
        )
        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("exporter_user_notification_count", response_data["good"]["query"])
        self.assertEqual(len(response_data["good"]["query"]["exporter_user_notification_count"]), 3)

    def test_get_end_user_advisory_queries_with_notifications_success(self):
        self._create_end_user_advisory_query_with_notifications()

        response = self.client.get(
            reverse_lazy("queries:end_user_advisories:end_user_advisories"), **self.exporter_headers,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        eua_query_response_data = response.json()["end_user_advisories"][0]
        self.assertIn("exporter_user_notification_count", eua_query_response_data)
        self.assertEqual(eua_query_response_data["exporter_user_notification_count"]["total"], 3)

    def test_get_end_user_advisory_query_with_notifications_success(self):
        case = self._create_end_user_advisory_query_with_notifications()

        response = self.client.get(
            reverse_lazy("queries:end_user_advisories:end_user_advisory", kwargs={"pk": str(case.id)}),
            **self.exporter_headers,
        )
        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("exporter_user_notification_count", response_data["end_user_advisory"])
        self.assertEqual(len(response_data["end_user_advisory"]["exporter_user_notification_count"]), 3)
