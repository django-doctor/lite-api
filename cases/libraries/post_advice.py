from django.http import JsonResponse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail

from applications.serializers.advice import CaseAdviceSerializer
from audit_trail import service as audit_trail_service
from audit_trail.enums import AuditType
from cases.libraries.get_case import get_case
from cases.models import Advice
from conf import constants
from conf.permissions import assert_user_has_permission
from flags.enums import SystemFlags
from flags.models import Flag
from lite_content.lite_api import strings
from static.statuses.enums import CaseStatusEnum


def check_if_user_cannot_manage_team_advice(case, user):
    if constants.GovPermissions.MANAGE_TEAM_CONFIRM_OWN_ADVICE.name not in user.role.permissions.values_list(
        "id", flat=True
    ):
        assert_user_has_permission(user, constants.GovPermissions.MANAGE_TEAM_ADVICE)

        if Advice.objects.filter(case=case, user=user).exists():
            return JsonResponse(
                {"errors": strings.Cases.ADVICE_POST_TEAM_ADVICE_WHEN_USER_ADVICE_EXISTS_ERROR},
                status=status.HTTP_403_FORBIDDEN,
            )


def check_if_final_advice_exists(case):
    if Advice.objects.get_final_advice(case=case):
        return JsonResponse({"errors": "Final advice already exists for this case"}, status=status.HTTP_400_BAD_REQUEST)


def check_if_team_advice_exists(case, user):
    if Advice.objects.get_team_advice(case=case, team=user.team):
        return JsonResponse(
            {"errors": "Team advice from your team already exists for this case"}, status=status.HTTP_400_BAD_REQUEST
        )


def check_refusal_errors(advice):
    if advice["type"].lower() == "refuse" and not advice["text"]:
        return {"text": [ErrorDetail(string=strings.Cases.ADVICE_REFUSAL_ERROR, code="blank")]}
    return None


def post_advice(request, case, level, team=False):
    if CaseStatusEnum.is_terminal(case.status.status):
        return JsonResponse(
            data={"errors": [strings.Applications.Generic.TERMINAL_CASE_CANNOT_PERFORM_OPERATION_ERROR]},
            status=status.HTTP_400_BAD_REQUEST,
        )

    data = request.data

    # Update the case and user in each piece of advice
    refusal_error = False
    for advice in data:
        advice["level"] = level
        advice["case"] = str(case.id)
        advice["user"] = str(request.user.id)
        if team:
            advice["team"] = str(request.user.team.id)
        if not refusal_error:
            refusal_error = check_refusal_errors(advice)

    serializer = CaseAdviceSerializer(data=data, many=True)

    if serializer.is_valid() and not refusal_error:
        serializer.save()
        if not team:
            # Only applies at user level advice
            audit_trail_service.create(
                actor=request.user, verb=AuditType.CREATED_USER_ADVICE, target=case,
            )
        return JsonResponse({"advice": serializer.data}, status=status.HTTP_201_CREATED)

    errors = {}
    if serializer.errors:
        errors.update(serializer.errors[0])

    if refusal_error:
        errors.update(refusal_error)
    return JsonResponse({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)


def case_advice_contains_refusal(case_id):
    case = get_case(case_id)
    team_advice = Advice.objects.filter(case=case)
    flag = Flag.objects.get(id=SystemFlags.REFUSAL_FLAG_ID)

    refuse_advice_found = False

    for advice in team_advice:
        if advice.type.lower() == "refuse":
            refuse_advice_found = True
            if flag not in case.flags.all():
                case.flags.add(flag)
                break

    if not refuse_advice_found:
        if flag in case.flags.all():
            case.flags.remove(flag)
