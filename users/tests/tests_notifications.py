from test_helpers.clients import DataTestClient
from cases.models import Notification


class NotificationTests(DataTestClient):

    def tests_create_new_clc_query_notification(self):

        clc_case = self.create_clc_query_case('Case Ref')

        self.create_case_note(clc_case, 'This is a test note 1', self.gov_user, True)
        self.create_case_note(clc_case, 'This is a test note 2', self.gov_user, True)
        self.create_case_note(clc_case, 'This is a test note 3', self.gov_user, True)
        self.create_case_note(clc_case, 'This is a test note 4', self.gov_user, False)

        self.assertEqual(Notification.objects.all().count(), 3)

    def tests_create_new_application_notification(self):
        app_case = self.create_application_case('Case Ref')
        self.create_case_note(app_case, 'This is a test note 1', self.gov_user, True)
        self.create_case_note(app_case, 'This is a test note 2', self.gov_user, False)

        self.assertEqual(Notification.objects.all().count(), 1)

    def tests_create_both_clc_and_application_notifications(self):

        app_case = self.create_application_case('Case Ref')
        clc_case = self.create_clc_query_case('Case Ref')

        self.create_case_note(app_case, 'This is a test note 1', self.gov_user, True)
        self.create_case_note(app_case, 'This is a test note 2', self.gov_user, True)
        self.create_case_note(app_case, 'This is a test note 3', self.gov_user, True)
        self.create_case_note(app_case, 'This is a test note 4', self.gov_user, True)

        self.create_case_note(clc_case, 'This is a test note 1', self.gov_user, True)
        self.create_case_note(clc_case, 'This is a test note 2', self.gov_user, True)
        self.create_case_note(clc_case, 'This is a test note 3', self.gov_user, True)

        self.assertEqual(Notification.objects.all().count(), 7)
        self.assertEqual(Notification.objects.filter(note__case__clc_query_id__isnull=True).count(), 4)
        self.assertEqual(Notification.objects.filter(note__case__application_id__isnull=True).count(), 3)