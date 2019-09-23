import json

import reversion
from django.http import JsonResponse, Http404
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from cases.libraries.activity_types import CaseActivityType
from cases.models import CaseActivity
from conf.authentication import ExporterAuthentication, SharedAuthentication
from goods.enums import GoodStatus
from goods.libraries.get_good import get_good
from queries.control_list_classifications.models import ControlListClassificationQuery
from queries.control_list_classifications.serializers import ClcQueryResponseSerializer
from queries.helpers import get_exporter_query
from users.models import UserOrganisationRelationship


class ControlListClassificationsList(APIView):
    authentication_classes = (ExporterAuthentication,)

    def post(self, request):
        """
        Create a new CLC query case instance
        """
        data = JSONParser().parse(request)
        good = get_good(data['good_id'])
        data['organisation'] = request.user.organisation

        # A CLC Query can only be created if the good is in draft status
        if good.status != GoodStatus.DRAFT:
            raise Http404

        if data['not_sure_details_control_code'] == '':
            return JsonResponse(data={
                'errors': {
                    'not_sure_details_control_code': ['This field may not be blank.']
                }
            }, status=status.HTTP_400_BAD_REQUEST)

        good.status = GoodStatus.CLC_QUERY
        good.control_code = data['not_sure_details_control_code']
        good.save()

        clc_query = ControlListClassificationQuery.objects.create(details=data['not_sure_details_details'],
                                                                  good=good,
                                                                  organisation=data['organisation'])
        clc_query.save()

        return JsonResponse(data={'id': clc_query.id, 'case_id': clc_query.case.get().id},
                            status=status.HTTP_201_CREATED)


class ControlListClassificationDetail(APIView):
    authentication_classes = (SharedAuthentication,)

    def put(self, request, pk):
        """
        Respond to a control list classification.
        """
        query = get_exporter_query(pk)
        data = json.loads(request.body)

        with reversion.create_revision():
            serializer = ClcQueryResponseSerializer(query, data=data)
            if serializer.is_valid():
                if 'validate_only' not in data or data['validate_only'] == 'False':
                    serializer.save()

                    # Add an activity item for the query's case
                    CaseActivity.create(activity_type=CaseActivityType.CLC_RESPONSE,
                                        case=query.case.get(),
                                        user=request.user)

                    # Send a notification to the user
                    for user_relationship in UserOrganisationRelationship.objects.filter(organisation=query.organisation):
                        user_relationship.user.send_notification(query=query)

                    return JsonResponse(data={'control_list_classification_query': serializer.data})
                else:
                    return JsonResponse(data={}, status=status.HTTP_200_OK)

            return JsonResponse(data={'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)