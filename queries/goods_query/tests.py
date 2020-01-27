from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from rest_framework import status

from audit_trail.models import Audit
from audit_trail.payload import AuditType
from cases.enums import CaseTypeEnum
from conf import constants
from flags.enums import SystemFlags
from flags.models import Flag
from goods.enums import GoodControlled, GoodStatus, GoodPvGraded
from goods.models import Good
from lite_content.lite_api import strings
from picklists.enums import PicklistType, PickListStatus
from queries.goods_query.models import GoodsQuery
from static.statuses.enums import CaseStatusEnum
from static.statuses.libraries.get_case_status import get_case_status_by_status
from static.statuses.models import CaseStatus
from test_helpers.clients import DataTestClient
from users.models import Role, GovUser


class ControlListClassificationsQueryCreateTests(DataTestClient):
    def setUp(self):
        super().setUp()

        self.good = Good(
            description="Good description",
            is_good_controlled=GoodControlled.UNSURE,
            is_pv_graded=GoodPvGraded.NO,
            pv_grading_details=None,
            control_code="ML1",
            part_number="123456",
            organisation=self.organisation,
        )
        self.good.save()

        self.data = {
            "good_id": self.good.id,
            "not_sure_details_control_code": "ML1a",
            "not_sure_details_details": "I " "don't know",
        }

        self.url = reverse("queries:goods_queries:goods_queries")

    def test_create_control_list_classification_query(self):
        """
        Ensure that an exporter can raise a control list
        classification query and that a case has been created
        """
        response = self.client.post(self.url, self.data, **self.exporter_headers)
        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_data["id"], str(GoodsQuery.objects.get().id))
        self.assertEqual(GoodsQuery.objects.count(), 1)
        self.assertEqual(
            [str(id) for id in GoodsQuery.objects.get().flags.values_list("id", flat=True)],
            [SystemFlags.GOOD_CLC_QUERY_ID],
        )

    def test_cannot_create_control_list_classification_query_on_good_when_good_already_exists(self):
        self.client.post(self.url, self.data, **self.exporter_headers)
        response = self.client.post(self.url, self.data, **self.exporter_headers)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(strings.GoodsQuery.A_QUERY_ALREADY_EXISTS_FOR_THIS_GOOD_ERROR in response.json()["errors"],)
        self.assertEqual(GoodsQuery.objects.count(), 1)


class ControlListClassificationsQueryRespondTests(DataTestClient):
    def setUp(self):
        super().setUp()
        self.report_summary = self.create_picklist_item(
            "Report Summary", self.team, PicklistType.REPORT_SUMMARY, PickListStatus.ACTIVE
        )

        self.query = self.create_clc_query("This is a widget", self.organisation)

        role = Role(name="review_goods")
        role.permissions.set([constants.GovPermissions.REVIEW_GOODS.name])
        role.save()
        self.gov_user.role = role
        self.gov_user.save()

        self.url = reverse("queries:goods_queries:clc_query_response", kwargs={"pk": self.query.pk})

        self.data = {
            "comment": "I Am Easy to Find",
            "report_summary": self.report_summary.pk,
            "control_code": "ML1a",
            "is_good_controlled": "yes",
        }

    def test_respond_to_control_list_classification_query_without_updating_control_code_success(self):
        self.query.good.control_code = "ML1a"
        self.query.good.save()
        previous_query_control_code = self.query.good.control_code

        response = self.client.put(self.url, self.data, **self.gov_headers)
        self.query.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.query.good.control_code, self.data["control_code"])
        self.assertEqual(self.query.good.control_code, previous_query_control_code)
        self.assertEqual(self.query.good.is_good_controlled, str(self.data["is_good_controlled"]))
        self.assertEqual(self.query.good.status, GoodStatus.VERIFIED)

        case = self.query.get_case()
        # Check that an audit item has been added
        audit_qs = Audit.objects.filter(
            target_object_id=case.id, target_content_type=ContentType.objects.get_for_model(case)
        )
        self.assertEqual(audit_qs.count(), 1)

    def test_respond_to_control_list_classification_query_update_control_code_success(self):
        previous_query_control_code = self.query.good.control_code
        response = self.client.put(self.url, self.data, **self.gov_headers)
        self.query.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.query.good.control_code, self.data["control_code"])
        self.assertNotEqual(self.query.good.control_code, previous_query_control_code)
        self.assertEqual(self.query.good.is_good_controlled, str(self.data["is_good_controlled"]))
        self.assertEqual(self.query.good.status, GoodStatus.VERIFIED)

        audit_qs = Audit.objects.all()
        self.assertEqual(audit_qs.count(), 2)
        for audit in audit_qs:
            verb = AuditType.GOOD_REVIEWED if audit.payload else AuditType.CLC_RESPONSE
            self.assertEqual(AuditType(audit.verb), verb)
            if verb == AuditType.GOOD_REVIEWED:
                payload = {
                    "good_name": self.query.good.description,
                    "old_control_code": previous_query_control_code,
                    "new_control_code": self.data["control_code"],
                }
                self.assertEqual(audit.payload, payload)

    def test_respond_to_control_list_classification_query_nlr(self):
        """
        Ensure that a gov user can respond to a control list classification query with no licence required.
        """
        previous_query_control_code = self.query.good.control_code
        data = {"comment": "I Am Easy to Find", "report_summary": self.report_summary.pk, "is_good_controlled": "no"}

        response = self.client.put(self.url, data, **self.gov_headers)
        self.query.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.query.good.control_code, "")
        self.assertNotEqual(self.query.good.control_code, previous_query_control_code)
        self.assertEqual(self.query.good.is_good_controlled, str(data["is_good_controlled"]))
        self.assertEqual(self.query.good.status, GoodStatus.VERIFIED)

        # Check that an activity item has been added
        qs = Audit.objects.filter(
            target_object_id=self.query.id, target_content_type=ContentType.objects.get_for_model(self.query)
        )
        for audit in qs:
            verb = AuditType.GOOD_REVIEWED if audit.payload else AuditType.CLC_RESPONSE
            self.assertEqual(AuditType(audit.verb), verb)

    def test_respond_to_control_list_classification_query_failure(self):
        """
        Ensure that a gov user cannot respond to a control list classification query without providing data.
        """
        data = {}

        response = self.client.put(self.url, data, **self.gov_headers)
        self.query.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.query.good.status, GoodStatus.DRAFT)

    def test_user_cannot_respond_to_clc_without_permissions(self):
        """
        Tests that the right level of permissions are required. A user must have permission to create
        team advice.
        """
        # Make sure at least one user maintains the super user role
        valid_user = GovUser(
            email="test2@mail.com", first_name="John", last_name="Smith", team=self.team, role=self.super_user_role
        )
        valid_user.save()

        self.gov_user.role = self.default_role
        self.gov_user.save()

        response = self.client.put(self.url, **self.gov_headers)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_cannot_respond_to_clc_with_case_in_terminal_state(self):
        self.query.status = CaseStatus.objects.get(status="finalised")
        self.query.save()

        response = self.client.put(self.url, self.data, **self.gov_headers)

        self.assertEqual(Audit.objects.all().count(), 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ControlListClassificationsQueryManageStatusTests(DataTestClient):
    def test_user_set_clc_status_success(self):
        query = self.create_clc_query("This is a widget", self.organisation)
        url = reverse("queries:goods_queries:manage_status", kwargs={"pk": query.pk})
        data = {"status": "withdrawn"}

        response = self.client.put(url, data, **self.gov_headers)
        query.refresh_from_db()

        self.assertEqual(query.status.status, CaseStatusEnum.WITHDRAWN)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ControlListClassificationsGeneratedDocumentsTests(DataTestClient):
    def setUp(self):
        super().setUp()
        self.query = self.create_clc_query("This is a widget", self.organisation)
        self.url = reverse("queries:goods_queries:generated_documents", kwargs={"pk": self.query.pk})

    def test_get_generated_documents_none_success(self):
        response = self.client.get(self.url, **self.exporter_headers)
        results = response.json()["generated_documents"]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(results), 0)

    def test_get_generated_documents_success(self):
        document_name = "Abc"
        template = self.create_letter_template("Template", case_type=CaseTypeEnum.GOODS_QUERY)
        self.create_generated_case_document(self.query, template, document_name=document_name)

        response = self.client.get(self.url, **self.exporter_headers)
        results = response.json()["generated_documents"]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["name"], document_name)


class PvGradingQueryCreateTests(DataTestClient):
    def test_given_an_unsure_pv_graded_good_exists_when_creating_pv_grading_query_then_201_created_is_returned(self):
        pv_graded_good = self.create_good(
            description="This is a good",
            org=self.organisation,
            is_good_controlled=GoodControlled.NO,
            control_code="",
            is_pv_graded=GoodPvGraded.GRADING_REQUIRED,
        )
        pv_grading_raised_reasons = "This is the reason why I'm unsure..."
        data = {
            "good_id": pv_graded_good.id,
            "pv_grading_raised_reasons": pv_grading_raised_reasons,
        }
        url = reverse("queries:goods_queries:goods_queries")

        response = self.client.post(url, data, **self.exporter_headers)
        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_data["id"], str(GoodsQuery.objects.get().id))
        self.assertEqual(GoodsQuery.objects.count(), 1)
        self.assertEqual(GoodsQuery.objects.get().pv_grading_raised_reasons, pv_grading_raised_reasons)
        self.assertEqual(
            [str(id) for id in GoodsQuery.objects.get().flags.values_list("id", flat=True)],
            [SystemFlags.GOOD_PV_GRADING_QUERY_ID],
        )

    def test_given_a_pv_graded_good_exists_when_creating_pv_grading_query_then_400_bad_request_is_returned(self):
        pv_graded_good = self.create_good(
            description="This is a good",
            org=self.organisation,
            is_good_controlled=GoodControlled.NO,
            control_code="",
            is_pv_graded=GoodPvGraded.YES,
        )
        pv_grading_raised_reasons = "This is the reason why I'm unsure..."
        data = {
            "good_id": pv_graded_good.id,
            "pv_grading_raised_reasons": pv_grading_raised_reasons,
        }
        url = reverse("queries:goods_queries:goods_queries")

        response = self.client.post(url, data, **self.exporter_headers)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()["errors"], [strings.GoodsQuery.GOOD_CLC_UNSURE_OR_PV_REQUIRED_ERROR],
        )
        self.assertEqual(GoodsQuery.objects.count(), 0)

    def test_given_good_doesnt_require_pv_grading_when_creating_pv_grading_query_then_400_bad_request_is_returned(self):
        pv_graded_good = self.create_good(
            description="This is a good",
            org=self.organisation,
            is_good_controlled=GoodControlled.NO,
            control_code="",
            is_pv_graded=GoodPvGraded.NO,
        )
        pv_grading_raised_reasons = "This is the reason why I'm unsure..."
        data = {
            "good_id": pv_graded_good.id,
            "pv_grading_raised_reasons": pv_grading_raised_reasons,
        }
        url = reverse("queries:goods_queries:goods_queries")

        response = self.client.post(url, data, **self.exporter_headers)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()["errors"], [strings.GoodsQuery.GOOD_CLC_UNSURE_OR_PV_REQUIRED_ERROR],
        )
        self.assertEqual(GoodsQuery.objects.count(), 0)


class PvGradingQueryManageStatusTests(DataTestClient):
    def test_when_setting_pv_graded_good_query_to_withdrawn_then_the_status_is_updated_and_a_200_ok_is_returned(self):
        query = self.create_pv_grading_query("This is a widget", self.organisation)
        url = reverse("queries:goods_queries:manage_status", kwargs={"pk": query.pk})
        data = {"status": "withdrawn"}

        response = self.client.put(url, data, **self.gov_headers)
        query.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(query.status.status, CaseStatusEnum.WITHDRAWN)


class CombinedPvGradingAndClcQuery(DataTestClient):
    def setUp(self):
        super().setUp()

        role = Role(name="review_goods")
        role.permissions.set([constants.GovPermissions.REVIEW_GOODS.name])
        role.save()
        self.gov_user.role = role
        self.gov_user.save()

        self.report_summary = self.create_picklist_item(
            "Report Summary", self.team, PicklistType.REPORT_SUMMARY, PickListStatus.ACTIVE
        )

        self.pv_graded_and_controlled_good = self.create_good(
            description="This is a good",
            org=self.organisation,
            is_good_controlled=GoodControlled.UNSURE,
            control_code="ML1a",
            is_pv_graded=GoodPvGraded.GRADING_REQUIRED,
        )

        self.clc_and_pv_query = GoodsQuery.objects.create(
            clc_raised_reasons="some clc reasons",
            pv_grading_raised_reasons="some pv reasons",
            good=self.pv_graded_and_controlled_good,
            organisation=self.organisation,
            type=CaseTypeEnum.GOODS_QUERY,
            status=get_case_status_by_status(CaseStatusEnum.SUBMITTED),
        )
        self.clc_and_pv_query.flags.set(
            [
                Flag.objects.get(id=SystemFlags.GOOD_CLC_QUERY_ID),
                Flag.objects.get(id=SystemFlags.GOOD_PV_GRADING_QUERY_ID),
            ]
        )
        self.clc_and_pv_query.save()

        self.clc_response_url = reverse(
            "queries:goods_queries:clc_query_response", kwargs={"pk": self.clc_and_pv_query.pk}
        )

        # The control_code and is_good_controlled must be equal to what they are currently on the good
        # otherwise two audits will be created;
        # One for the response to the query and another for updating the good
        self.data = {
            "comment": "I Am Easy to Find",
            "report_summary": self.report_summary.pk,
            "control_code": "ML1a",
            "is_good_controlled": "yes",
        }

    def test_when_responding_to_only_clc_then_only_the_clc_system_flag_is_removed_from_case(self):
        response = self.client.put(self.clc_response_url, self.data, **self.gov_headers)
        self.clc_and_pv_query.refresh_from_db()
        case = self.clc_and_pv_query.get_case()
        remaining_flags = [str(id) for id in case.flags.values_list("id", flat=True)]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(SystemFlags.GOOD_CLC_QUERY_ID not in remaining_flags)
        self.assertTrue(SystemFlags.GOOD_PV_GRADING_QUERY_ID in remaining_flags)
        self.assertEqual(self.clc_and_pv_query.good.status, GoodStatus.VERIFIED)

        # Check that an audit item has been added
        audit_qs = Audit.objects.filter(
            target_object_id=case.id, target_content_type=ContentType.objects.get_for_model(case)
        )
        self.assertEqual(audit_qs.count(), 1)
