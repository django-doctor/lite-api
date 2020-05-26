from django.urls import reverse
from parameterized import parameterized_class
from rest_framework import status

from applications.models import (
    SiteOnApplication,
    GoodOnApplication,
    ExhibitionClearanceApplication,
    F680ClearanceApplication,
    GiftingClearanceApplication,
)
from cases.enums import CaseTypeEnum
from lite_content.lite_api import strings
from parties.enums import PartyType
from parties.models import PartyDocument
from static.statuses.enums import CaseStatusEnum
from test_helpers.clients import DataTestClient


@parameterized_class(
    "case_type", [(CaseTypeEnum.EXHIBITION,), (CaseTypeEnum.GIFTING,), (CaseTypeEnum.F680,),],
)
class MODClearanceTests(DataTestClient):
    """
    Shared MOD clearance tests.
    Covers elements MOD clearances have in common like the requirement
    for goods & locations.
    """

    def setUp(self):
        super().setUp()
        self.draft = self.create_mod_clearance_application(self.organisation, case_type=self.case_type)
        self.url = reverse("applications:application_submit", kwargs={"pk": self.draft.id})
        self.exporter_user.set_role(self.organisation, self.exporter_super_user_role)

    def test_submit_MOD_clearance_success(self):
        response = self.client.put(self.url, **self.exporter_headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["application"]["name"], self.draft.name)

    def test_submit_MOD_clearance_without_goods_failure(self):
        GoodOnApplication.objects.get(application=self.draft).delete()

        response = self.client.put(self.url, **self.exporter_headers)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["errors"]["goods"], [strings.Applications.Standard.NO_GOODS_SET])


class ExhibitionClearanceTests(DataTestClient):
    def setUp(self):
        super().setUp()
        self.draft = self.create_mod_clearance_application(self.organisation, case_type=CaseTypeEnum.EXHIBITION)
        self.url = reverse("applications:application_submit", kwargs={"pk": self.draft.id})
        self.exporter_user.set_role(self.organisation, self.exporter_super_user_role)

    def test_submit_exhibition_clearance_success(self):
        response = self.client.put(self.url, **self.exporter_headers)
        application = ExhibitionClearanceApplication.objects.get()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["application"]["name"], self.draft.name)
        self.assertEqual(ExhibitionClearanceApplication.objects.count(), 1)
        self.assertEqual(list(application.third_parties.all()), [])
        self.assertIsNone(application.end_user)
        self.assertIsNone(application.consignee)
        self.assertIsNone(application.submitted_at)
        self.assertEqual(application.status.status, CaseStatusEnum.DRAFT)
        self.assertIsNotNone(application.goods.get())

    def test_submit_exhibition_clearance_without_location_failure(self):
        SiteOnApplication.objects.get(application=self.draft).delete()

        response = self.client.put(self.url, **self.exporter_headers)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["errors"]["location"], [strings.Applications.Generic.NO_LOCATION_SET])

    def test_submit_exhibition_clearance_without_details_failure(self):
        self.draft.title, self.draft.first_exhibition_date, self.draft.required_by_date = None, None, None
        self.draft.save()

        response = self.client.put(self.url, **self.exporter_headers)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["errors"]["details"], [strings.Applications.Exhibition.Error.NO_DETAILS])

    def test_submit_exhibition_clearance_without_goods_failure(self):
        GoodOnApplication.objects.get(application=self.draft).delete()

        response = self.client.put(self.url, **self.exporter_headers)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["errors"]["goods"], [strings.Applications.Standard.NO_GOODS_SET])

    def test_exhibition_clearance_declaration_submit_success(self):
        data = {
            "submit_declaration": True,
            "agreed_to_declaration": True,
            "agreed_to_foi": True,
        }
        application = ExhibitionClearanceApplication.objects.get()
        self.assertEqual(application.status.status, CaseStatusEnum.DRAFT)

        url = reverse("applications:application_submit", kwargs={"pk": self.draft.id})
        response = self.client.put(url, data, **self.exporter_headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        application.refresh_from_db()
        self.assertIsNotNone(application.submitted_at)
        self.assertNotEqual(application.status.status, CaseStatusEnum.DRAFT)
        self.assertEqual(application.agreed_to_foi, True)
        self.assertEqual(application.submitted_by, self.exporter_user)

    def test_exhibition_clearance_declaration_submit_tcs_false_failure(self):
        data = {
            "submit_declaration": True,
            "agreed_to_declaration": False,
            "agreed_to_foi": True,
        }

        url = reverse("applications:application_submit", kwargs={"pk": self.draft.id})
        response = self.client.put(url, data, **self.exporter_headers)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = response.json()["errors"]
        self.assertEqual(errors["agreed_to_declaration"], [strings.Applications.Generic.AGREEMENT_TO_TCS_REQUIRED])


class GiftingClearanceTests(DataTestClient):
    def setUp(self):
        super().setUp()
        self.draft = self.create_mod_clearance_application(self.organisation, case_type=CaseTypeEnum.GIFTING)
        self.url = reverse("applications:application_submit", kwargs={"pk": self.draft.id})
        self.exporter_user.set_role(self.organisation, self.exporter_super_user_role)

    def test_submit_gifting_clearance_success(self):
        response = self.client.put(self.url, **self.exporter_headers)
        application = GiftingClearanceApplication.objects.get()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["application"]["name"], self.draft.name)
        self.assertEqual(GiftingClearanceApplication.objects.count(), 1)
        self.assertIsNotNone(application.third_parties.get())
        self.assertIsNotNone(application.end_user)
        self.assertIsNone(application.submitted_at)
        self.assertEqual(application.status.status, CaseStatusEnum.DRAFT)
        self.assertIsNotNone(application.goods.get())

    def test_submit_gifting_clearance_without_end_user_failure(self):
        self.draft.delete_party(self.draft.end_user)

        response = self.client.put(self.url, **self.exporter_headers)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["errors"]["end_user"], [strings.Applications.Standard.NO_END_USER_SET])

    def test_submit_gifting_clearance_without_end_user_document_success(self):
        PartyDocument.objects.filter(party=self.draft.end_user.party).delete()

        response = self.client.put(self.url, **self.exporter_headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["application"]["name"], self.draft.name)

    def test_submit_gifting_with_consignee_failure(self):
        self.create_party("Consignee", self.organisation, PartyType.CONSIGNEE, self.draft)

        response = self.client.put(self.url, **self.exporter_headers)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["errors"]["consignee"], [strings.Applications.Gifting.CONSIGNEE])

    def test_submit_gifting_with_ultimate_end_user_failure(self):
        self.create_party("Ultimate End User", self.organisation, PartyType.ULTIMATE_END_USER, self.draft)

        response = self.client.put(self.url, **self.exporter_headers)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()["errors"]["ultimate_end_users"], [strings.Applications.Gifting.ULTIMATE_END_USERS]
        )

    def test_submit_gifting_clearance_with_location_failure(self):
        SiteOnApplication(site=self.organisation.primary_site, application=self.draft).save()

        response = self.client.put(self.url, **self.exporter_headers)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["errors"]["location"], [strings.Applications.Gifting.LOCATIONS])

    def test_gifting_clearance_declaration_submit_success(self):
        data = {
            "submit_declaration": True,
            "agreed_to_declaration": True,
            "agreed_to_foi": True,
        }
        application = GiftingClearanceApplication.objects.get()
        self.assertEqual(application.status.status, CaseStatusEnum.DRAFT)

        url = reverse("applications:application_submit", kwargs={"pk": self.draft.id})
        response = self.client.put(url, data, **self.exporter_headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        application.refresh_from_db()
        self.assertIsNotNone(application.submitted_at)
        self.assertNotEqual(application.status.status, CaseStatusEnum.DRAFT)
        self.assertEqual(application.agreed_to_foi, True)
        self.assertEqual(application.submitted_by, self.exporter_user)

    def test_gifting_clearance_declaration_submit_tcs_false_failure(self):
        data = {
            "submit_declaration": True,
            "agreed_to_declaration": False,
            "agreed_to_foi": True,
        }

        url = reverse("applications:application_submit", kwargs={"pk": self.draft.id})
        response = self.client.put(url, data, **self.exporter_headers)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = response.json()["errors"]
        self.assertEqual(errors["agreed_to_declaration"], [strings.Applications.Generic.AGREEMENT_TO_TCS_REQUIRED])


class F680ClearanceTests(DataTestClient):
    def setUp(self):
        super().setUp()
        self.draft = self.create_mod_clearance_application(self.organisation, case_type=CaseTypeEnum.F680)
        self.url = reverse("applications:application_submit", kwargs={"pk": self.draft.id})
        self.exporter_user.set_role(self.organisation, self.exporter_super_user_role)

    def test_submit_F680_clearance_success(self):
        response = self.client.put(self.url, **self.exporter_headers)
        application = F680ClearanceApplication.objects.get()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["application"]["name"], self.draft.name)
        self.assertEqual(F680ClearanceApplication.objects.count(), 1)
        self.assertIsNotNone(application.third_parties.get())
        self.assertIsNotNone(application.end_user)
        self.assertIsNone(application.submitted_at)
        self.assertEqual(application.status.status, CaseStatusEnum.DRAFT)
        self.assertIsNotNone(application.goods.get())
        self.assertIsNotNone(application.intended_end_use)

    def test_submit_F680_with_end_user_and_without_third_party_success(self):
        self.draft.third_parties.all().delete()

        response = self.client.put(self.url, **self.exporter_headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["application"]["name"], self.draft.name)

    def test_submit_F680_without_end_user_and_with_third_party_success(self):
        self.draft.delete_party(self.draft.end_user)

        response = self.client.put(self.url, **self.exporter_headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["application"]["name"], self.draft.name)

    def test_submit_F680_without_end_user_or_third_party_failure(self):
        self.draft.delete_party(self.draft.end_user)
        self.draft.third_parties.all().delete()
        self.draft.save()

        response = self.client.put(self.url, **self.exporter_headers)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["errors"]["party"], [strings.Applications.F680.NO_END_USER_OR_THIRD_PARTY])

    def test_submit_F680_without_end_user_document_success(self):
        PartyDocument.objects.filter(party=self.draft.end_user.party).delete()

        response = self.client.put(self.url, **self.exporter_headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["application"]["name"], self.draft.name)

    def test_submit_F680_with_consignee_failure(self):
        self.create_party("Consignee", self.organisation, PartyType.CONSIGNEE, self.draft)

        response = self.client.put(self.url, **self.exporter_headers)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["errors"]["consignee"], [strings.Applications.F680.CONSIGNEE])

    def test_submit_F680_with_ultimate_end_user_failure(self):
        self.create_party("Ultimate End User", self.organisation, PartyType.ULTIMATE_END_USER, self.draft)

        response = self.client.put(self.url, **self.exporter_headers)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()["errors"]["ultimate_end_users"], [strings.Applications.F680.ULTIMATE_END_USERS]
        )

    def test_submit_F680_clearance_with_location_failure(self):
        SiteOnApplication(site=self.organisation.primary_site, application=self.draft).save()

        response = self.client.put(self.url, **self.exporter_headers)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["errors"]["location"], [strings.Applications.F680.LOCATIONS])

    def test_submit_F680_clearance_without_details_failure(self):
        self.draft.types.clear()

        response = self.client.put(self.url, **self.exporter_headers)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["errors"]["types"], [strings.Applications.F680.NO_CLEARANCE_TYPE])

    def test_submit_F680_clearance_without_end_use_details_failure(self):
        self.draft.intended_end_use = ""
        self.draft.save()

        response = self.client.put(self.url, **self.exporter_headers)

        self.draft.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.json()["errors"]), 1)
        self.assertEqual(
            response.json()["errors"]["end_use_details"], [strings.Applications.Generic.NO_END_USE_DETAILS]
        )

    def test_f680_clearance_declaration_submit_success(self):
        data = {
            "submit_declaration": True,
            "agreed_to_declaration": True,
            "agreed_to_foi": True,
        }
        application = F680ClearanceApplication.objects.get()
        self.assertEqual(application.status.status, CaseStatusEnum.DRAFT)

        url = reverse("applications:application_submit", kwargs={"pk": self.draft.id})
        response = self.client.put(url, data, **self.exporter_headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        application.refresh_from_db()
        self.assertIsNotNone(application.submitted_at)
        self.assertNotEqual(application.status.status, CaseStatusEnum.DRAFT)
        self.assertEqual(application.agreed_to_foi, True)
        self.assertEqual(application.submitted_by, self.exporter_user)

    def test_f680_clearance_declaration_submit_tcs_false_failure(self):
        data = {
            "submit_declaration": True,
            "agreed_to_declaration": False,
            "agreed_to_foi": True,
        }

        url = reverse("applications:application_submit", kwargs={"pk": self.draft.id})
        response = self.client.put(url, data, **self.exporter_headers)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = response.json()["errors"]
        self.assertEqual(errors["agreed_to_declaration"], [strings.Applications.Generic.AGREEMENT_TO_TCS_REQUIRED])
