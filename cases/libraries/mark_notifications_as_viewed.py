from django.utils import timezone

from cases.models import CaseNote, Notification, EcjuQuery
from queries.control_list_classifications.models import ControlListClassificationQuery


def mark_notifications_as_viewed(user, objects):
    for obj in objects:
        if isinstance(obj, CaseNote):
            Notification.objects.filter(user=user, case_note=obj).update(
                viewed_at=timezone.now())
        elif isinstance(obj, EcjuQuery):
            Notification.objects.filter(user=user, ecju_query=obj).update(
                viewed_at=timezone.now())
        elif isinstance(obj, ControlListClassificationQuery):
            Notification.objects.filter(user=user, query=obj).update(
                viewed_at=timezone.now())
        else:
            raise Exception('mark_notifications_as_viewed: object type not expected')