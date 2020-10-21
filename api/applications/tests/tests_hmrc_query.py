from unittest import mock

from django.urls import reverse
from rest_framework import status
from uuid import UUID

from api.applications.models import SiteOnApplication, ExternalLocationOnApplication
from api.cases.enums import CaseTypeSubTypeEnum, CaseDocumentState
from api.cases.models import Case, CaseDocument
from api.core.constants import AutoGeneratedDocuments
from api.flags.enums import SystemFlags
from api.goodstype.models import GoodsType
from lite_content.lite_api import strings
from api.parties.models import PartyDocument
from api.staticdata.statuses.enums import CaseStatusEnum
from test_helpers.clients import DataTestClient


class HmrcQueryTests(DataTestClient):
    def setUp(self):
        super().setUp()
        self.hmrc_query = self.create_hmrc_query(self.organisation)
        self.url = reverse("applications:application_submit", kwargs={"pk": self.hmrc_query.id})

    @mock.patch("api.documents.libraries.s3_operations.upload_bytes_file")
    @mock.patch("api.cases.generated_documents.helpers.html_to_pdf")
    def test_submit_hmrc_query_success(self, upload_bytes_file_func, html_to_pdf_func):
        upload_bytes_file_func.return_value = None
        html_to_pdf_func.return_value = None

        data = {"submit_hmrc": True}
        response = self.client.put(self.url, data=data, **self.hmrc_exporter_headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        case = Case.objects.get()
        self.assertEqual(case.id, self.hmrc_query.id)
        self.assertIsNotNone(case.submitted_at)
        self.assertEqual(case.status.status, CaseStatusEnum.SUBMITTED)
        self.assertEqual(case.case_type.sub_type, CaseTypeSubTypeEnum.HMRC)
        self.assertTrue(UUID(SystemFlags.ENFORCEMENT_CHECK_REQUIRED) in case.flags.values_list("id", flat=True))
        self.assertEqual(case.submitted_by, self.hmrc_exporter_user)
        # Asserting that the 'Application Form' has been autogenerated on submission of the application
        html_to_pdf_func.assert_called_once()
        upload_bytes_file_func.assert_called_once()
        self.assertEqual(
            CaseDocument.objects.filter(
                name__contains=AutoGeneratedDocuments.APPLICATION_FORM,
                type=CaseDocumentState.AUTO_GENERATED,
                safe=True,
                case=case,
                visible_to_exporter=False,
            ).count(),
            1,
        )

    def test_submit_hmrc_query_with_goods_departed_success(self):
        SiteOnApplication.objects.get(application=self.hmrc_query).delete()
        self.hmrc_query.have_goods_departed = True
        self.hmrc_query.save()

        response = self.client.put(self.url, **self.hmrc_exporter_headers)
        response_data = response.json()["application"]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data["have_goods_departed"], True)

    def test_submit_hmrc_query_with_invalid_id_failure(self):
        draft_id = "90D6C724-0339-425A-99D2-9D2B8E864EC7"
        url = "applications/" + draft_id + "/submit/"

        response = self.client.put(url, **self.hmrc_exporter_headers)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_submit_hmrc_query_without_end_user_failure(self):
        self.hmrc_query.end_user.delete()

        url = reverse("applications:application_submit", kwargs={"pk": self.hmrc_query.id})

        response = self.client.put(url, **self.hmrc_exporter_headers)

        self.assertContains(
            response, text=strings.Applications.Standard.NO_END_USER_SET, status_code=status.HTTP_400_BAD_REQUEST,
        )

    def test_submit_hmrc_query_without_end_user_document_failure(self):
        PartyDocument.objects.filter(party=self.hmrc_query.end_user.party).delete()
        url = reverse("applications:application_submit", kwargs={"pk": self.hmrc_query.id})

        response = self.client.put(url, **self.hmrc_exporter_headers)

        self.assertContains(
            response,
            text=strings.Applications.Standard.NO_END_USER_DOCUMENT_SET,
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    def test_submit_hmrc_query_without_goods_type_failure(self):
        GoodsType.objects.filter(application=self.hmrc_query).delete()

        response = self.client.put(self.url, **self.hmrc_exporter_headers)

        self.assertContains(
            response, text=strings.Applications.Open.NO_GOODS_SET, status_code=status.HTTP_400_BAD_REQUEST,
        )

    def test_status_code_post_with_untested_document_failure(self):
        draft = self.create_hmrc_query(self.organisation, safe_document=None)
        url = reverse("applications:application_submit", kwargs={"pk": draft.id})

        response = self.client.put(url, **self.hmrc_exporter_headers)

        self.assertContains(
            response,
            text=strings.Applications.Standard.END_USER_DOCUMENT_PROCESSING,
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    def test_status_code_post_with_infected_document_failure(self):
        draft = self.create_hmrc_query(self.organisation, safe_document=False)
        url = reverse("applications:application_submit", kwargs={"pk": draft.id})

        response = self.client.put(url, **self.hmrc_exporter_headers)

        self.assertContains(
            response,
            text=strings.Applications.Standard.END_USER_DOCUMENT_INFECTED,
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    def test_setting_have_goods_departed_success(self):
        """
        Ensure that when setting have_goods_departed to True
        that it deletes all existing sites and locations on that application
        """
        data = {"have_goods_departed": True}

        response = self.client.put(
            reverse("applications:application", kwargs={"pk": self.hmrc_query.id}), data, **self.hmrc_exporter_headers
        )
        self.hmrc_query.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.hmrc_query.have_goods_departed)
        self.assertEqual(SiteOnApplication.objects.filter(application=self.hmrc_query).count(), 0)
        self.assertEqual(ExternalLocationOnApplication.objects.filter(application=self.hmrc_query).count(), 0)

    def test_setting_have_goods_departed_to_false_success(self):
        """
        Ensure that when setting have_goods_departed to False that it doesn't
        delete all existing sites and locations on that application
        """
        data = {"have_goods_departed": False}

        response = self.client.put(
            reverse("applications:application", kwargs={"pk": self.hmrc_query.id}), data, **self.hmrc_exporter_headers
        )
        self.hmrc_query.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(self.hmrc_query.have_goods_departed)
        self.assertEqual(SiteOnApplication.objects.filter(application=self.hmrc_query).count(), 1)

    def test_setting_sites_when_goods_departed_is_set_to_true_failure(self):
        """
        Ensure that it is not possible to add sites to the application
        when have_goods_departed is set to True
        """
        SiteOnApplication.objects.get(application=self.hmrc_query).delete()
        self.hmrc_query.have_goods_departed = True
        self.hmrc_query.save()

        data = {"sites": [self.hmrc_organisation.primary_site.id]}

        response = self.client.post(
            reverse("applications:application_sites", kwargs={"pk": self.hmrc_query.id}),
            data,
            **self.hmrc_exporter_headers,
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_setting_locations_when_goods_departed_is_set_to_true_failure(self):
        """
        Ensure that it is not possible to add external locations
        to the application when have_goods_departed is set to True
        """
        SiteOnApplication.objects.get(application=self.hmrc_query).delete()
        self.hmrc_query.have_goods_departed = True
        self.hmrc_query.save()
        external_location = self.create_external_location("storage facility", self.hmrc_organisation)

        data = {"external_locations": [external_location.id]}

        response = self.client.post(
            reverse("applications:application_external_locations", kwargs={"pk": self.hmrc_query.id}),
            data,
            **self.hmrc_exporter_headers,
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)