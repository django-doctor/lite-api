from django.http import Http404

from conf.exceptions import NotFoundError
from end_user.models import EndUser


def get_end_user_with_organisation(pk, organisation):
    try:
        end_user = EndUser.objects.get(pk=pk)

        if end_user.organisation.pk != organisation.pk:
            raise Http404

        return end_user
    except EndUser.DoesNotExist:
        raise NotFoundError({'end_user': 'End User not found - ' + str(pk)})