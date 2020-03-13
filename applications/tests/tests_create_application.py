from parameterized import parameterized
from rest_framework import status
from rest_framework.reverse import reverse

from applications.enums import (
    ApplicationExportType,
    ApplicationExportLicenceOfficialType,
    GoodsCategory,
)
from applications.models import (
    StandardApplication,
    OpenApplication,
    HmrcQuery,
    BaseApplication,
    ExhibitionClearanceApplication,
    GiftingClearanceApplication,
    F680ClearanceApplication,
)
from cases.enums import CaseTypeEnum, CaseTypeReferenceEnum
from lite_content.lite_api import strings
from test_helpers.clients import DataTestClient


class DraftTests(DataTestClient):
    url = reverse("applications:applications")

    def test_create_draft_standard_individual_export_application_successful(self):
        """
        Ensure we can create a new standard individual export application draft
        """
        data = {
            "name": "Test",
            "application_type": CaseTypeReferenceEnum.SIEL,
            "export_type": ApplicationExportType.TEMPORARY,
            "have_you_been_informed": ApplicationExportLicenceOfficialType.YES,
            "reference_number_on_information_form": "123",
        }

        response = self.client.post(self.url, data, **self.exporter_headers)
        response_data = response.json()
        standard_application = StandardApplication.objects.get()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_data["id"], str(standard_application.id))
        self.assertEqual(StandardApplication.objects.count(), 1)

    def test_create_draft_standard_application_with_goods_categories_successful(self):
        """
        Ensure we can create a new standard application with goods categories draft object
        """
        data = {
            "name": "Test",
            "application_type": CaseTypeReferenceEnum.SIEL,
            "export_type": ApplicationExportType.TEMPORARY,
            "goods_categories": [GoodsCategory.ANTI_PIRACY, GoodsCategory.FIREARMS],
            "have_you_been_informed": ApplicationExportLicenceOfficialType.YES,
            "reference_number_on_information_form": "123",
        }

        response = self.client.post(self.url, data, **self.exporter_headers)
        response_data = response.json()
        standard_application = StandardApplication.objects.get()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_data["id"], str(standard_application.id))
        self.assertCountEqual(standard_application.goods_categories, data["goods_categories"])

    def test_create_draft_standard_application_with_invalid_goods_categories_failure(self):
        """
        Ensure we cannot create a standard application with invalid goods categories
        """
        data = {
            "name": "Test",
            "application_type": CaseTypeReferenceEnum.SIEL,
            "export_type": ApplicationExportType.TEMPORARY,
            "goods_categories": ["Hard to Find"],
            "have_you_been_informed": ApplicationExportLicenceOfficialType.YES,
            "reference_number_on_information_form": "123",
        }

        response = self.client.post(self.url, data, **self.exporter_headers)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(StandardApplication.objects.count(), 0)

    def test_create_draft_exhibition_clearance_application_successful(self):
        """
        Ensure we can create a new Exhibition Clearance draft object
        """
        self.assertEqual(ExhibitionClearanceApplication.objects.count(), 0)

        data = {
            "name": "Test",
            "application_type": CaseTypeReferenceEnum.EXHC,
        }

        response = self.client.post(self.url, data, **self.exporter_headers)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ExhibitionClearanceApplication.objects.count(), 1)

    def test_create_draft_gifting_clearance_application_successful(self):
        """
        Ensure we can create a new Exhibition Clearance draft object
        """
        self.assertEqual(GiftingClearanceApplication.objects.count(), 0)

        data = {
            "name": "Test",
            "application_type": CaseTypeReferenceEnum.GIFT,
        }

        response = self.client.post(self.url, data, **self.exporter_headers)
        application = GiftingClearanceApplication.objects.get()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(GiftingClearanceApplication.objects.count(), 1)
        self.assertEqual(application.name, data["name"])
        self.assertEqual(application.case_type.id, CaseTypeEnum.GIFTING.id)

    def test_create_draft_f680_clearance_application_successful(self):
        """
        Ensure we can create a new Exhibition Clearance draft object
        """
        self.assertEqual(F680ClearanceApplication.objects.count(), 0)

        data = {
            "name": "Test",
            "application_type": CaseTypeReferenceEnum.F680,
        }

        response = self.client.post(self.url, data, **self.exporter_headers)
        application = F680ClearanceApplication.objects.get()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(F680ClearanceApplication.objects.count(), 1)
        self.assertEqual(application.name, data["name"])
        self.assertEqual(application.case_type.id, CaseTypeEnum.F680.id)

    def test_create_draft_open_application_successful(self):
        """
        Ensure we can create a new open application draft object
        """
        data = {
            "name": "Test",
            "application_type": CaseTypeReferenceEnum.OIEL,
            "export_type": ApplicationExportType.TEMPORARY,
        }

        response = self.client.post(self.url, data, **self.exporter_headers)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(OpenApplication.objects.count(), 1)

    def test_create_draft_hmrc_query_successful(self):
        """
        Ensure we can create a new HMRC query draft object
        """
        data = {
            "application_type": CaseTypeReferenceEnum.CRE,
            "organisation": self.organisation.id,
        }

        response = self.client.post(self.url, data, **self.hmrc_exporter_headers)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(HmrcQuery.objects.count(), 1)

    def test_create_draft_hmrc_query_failure(self):
        """
        Ensure that a normal exporter cannot create an HMRC query
        """
        data = {
            "application_type": CaseTypeReferenceEnum.CRE,
            "organisation": self.organisation.id,
        }

        response = self.client.post(self.url, data, **self.exporter_headers)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(HmrcQuery.objects.count(), 0)

    @parameterized.expand(
        [
            [{}],
            [{"application_type": CaseTypeReferenceEnum.SIEL, "export_type": ApplicationExportType.TEMPORARY}],
            [{"name": "Test", "export_type": ApplicationExportType.TEMPORARY}],
            [{"name": "Test", "application_type": CaseTypeReferenceEnum.SIEL}],
            [{"application_type": CaseTypeReferenceEnum.EXHC}],
            [{"name": "Test"}],
        ]
    )
    def test_create_draft_failure(self, data):
        """
        Ensure we cannot create a new draft object with POST data that is missing required properties
        Applications require: application_type, export_type & name
        Exhibition clearances require: application_type & name
        Above is a mixture of invalid combinations for these cases
        """
        response = self.client.post(self.url, data, **self.exporter_headers)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(BaseApplication.objects.count(), 0)

    def test_create_no_application_type_failure(self):
        """
        Ensure that we cannot create a new application without
        providing a application_type.
        """
        data = {}

        response = self.client.post(self.url, data, **self.exporter_headers)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()["errors"]["application_type"][0], strings.Applications.Generic.SELECT_A_LICENCE_TYPE
        )
