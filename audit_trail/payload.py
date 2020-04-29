from audit_trail.enums import AuditType


def format_payload(audit_type, payload):
    text = audit_type_format[audit_type].format(**payload)
    if text[-1] not in [":", ".", "?"]:
        return f"{text}."

    return text


audit_type_format = {
    AuditType.CREATED: "created",
    AuditType.ADD_FLAGS: "added flags: {added_flags}",
    AuditType.REMOVE_FLAGS: "removed flags: {removed_flags}",
    AuditType.GOOD_REVIEWED: 'good was reviewed: {good_name} control code changed from "{old_control_list_entry}" to "{new_control_list_entry}"',
    AuditType.GOOD_ADD_FLAGS: "added flags: {added_flags} to good: {good_name}",
    AuditType.GOOD_REMOVE_FLAGS: "removed flags: {removed_flags} from good: {good_name}",
    AuditType.GOOD_ADD_REMOVE_FLAGS: "added flags: {added_flags}, and removed: {removed_flags} from good: {good_name}",
    AuditType.DESTINATION_ADD_FLAGS: "added flags: {added_flags} to destination: {destination_name}",
    AuditType.DESTINATION_REMOVE_FLAGS: "removed flags: {removed_flags} from destination: {destination_name}",
    AuditType.ADD_GOOD_TO_APPLICATION: "added good: {good_name}",
    AuditType.REMOVE_GOOD_FROM_APPLICATION: "removed good: {good_name}",
    AuditType.ADD_GOOD_TYPE_TO_APPLICATION: "added good type: {good_type_name}",
    AuditType.REMOVE_GOOD_TYPE_FROM_APPLICATION: "removed good type: {good_type_name}",
    AuditType.UPDATE_APPLICATION_END_USE_DETAIL: 'updated {end_use_detail} from "{old_end_use_detail}" to "{new_end_use_detail}"',
    AuditType.UPDATE_APPLICATION_TEMPORARY_EXPORT: (
        'updated {temp_export_detail} from "{old_temp_export_detail}" to "{new_temp_export_detail}"'
    ),
    AuditType.REMOVED_SITES_FROM_APPLICATION: "removed sites: {sites}",
    AuditType.ADD_SITES_TO_APPLICATION: "added sites: {sites}",
    AuditType.REMOVED_EXTERNAL_LOCATIONS_FROM_APPLICATION: "removed external locations: {locations}",
    AuditType.ADD_EXTERNAL_LOCATIONS_TO_APPLICATION: "added external locations: {locations}",
    AuditType.REMOVED_COUNTRIES_FROM_APPLICATION: "removed countries: {countries}",
    AuditType.ADD_COUNTRIES_TO_APPLICATION: "added countries: {countries}",
    AuditType.ADD_ADDITIONAL_CONTACT_TO_CASE: "added an additional contact: {contact}",
    AuditType.MOVE_CASE: "moved the case to {queues}",
    AuditType.ASSIGN_CASE: "added case to {assignment}",
    AuditType.REMOVE_CASE: "removed case from queues: {queues}",
    AuditType.REMOVE_CASE_FROM_ALL_QUEUES: "removed case from all queues",
    AuditType.REMOVE_CASE_FROM_ALL_USER_ASSIGNMENTS: "removed case from all user assignments",
    AuditType.CLC_RESPONSE: "responded to the case",
    AuditType.PV_GRADING_RESPONSE: "responded to pv grading, grading set as {grading}",
    AuditType.CREATED_CASE_NOTE: "added a case note: {case_note}",
    AuditType.ECJU_QUERY: " added an ECJU Query: {ecju_query}",
    AuditType.UPDATED_STATUS: "updated the status to: {status}",
    AuditType.UPDATED_APPLICATION_NAME: 'updated the application name from "{old_name}" to "{new_name}"',
    AuditType.UPDATE_APPLICATION_LETTER_REFERENCE: 'updated the letter reference from "{old_ref_number}" to "{new_ref_number}"',
    AuditType.UPDATE_APPLICATION_F680_CLEARANCE_TYPES: 'updated the clearance types from "{old_types}" to "{new_types}"',
    AuditType.ADDED_APPLICATION_LETTER_REFERENCE: "added the letter reference: {new_ref_number}",
    AuditType.REMOVED_APPLICATION_LETTER_REFERENCE: "removed the letter reference: {old_ref_number}",
    AuditType.ASSIGNED_COUNTRIES_TO_GOOD: "added the destinations {countries} to '{good_type_name}'",
    AuditType.REMOVED_COUNTRIES_FROM_GOOD: "removed the destinations {countries} from '{good_type_name}'",
    AuditType.CREATED_FINAL_ADVICE: "created final advice",
    AuditType.CLEARED_FINAL_ADVICE: "cleared final advice",
    AuditType.CREATED_TEAM_ADVICE: "created team advice",
    AuditType.CLEARED_TEAM_ADVICE: "cleared team advice",
    AuditType.CREATED_USER_ADVICE: "created user advice",
    AuditType.ADD_PARTY: "added the {party_type} {party_name}",
    AuditType.REMOVE_PARTY: "removed the {party_type} {party_name}",
    AuditType.UPLOAD_PARTY_DOCUMENT: "uploaded the document {file_name} for {party_type} {party_name}",
    AuditType.DELETE_PARTY_DOCUMENT: "deleted the document {file_name} for {party_type} {party_name}",
    AuditType.UPLOAD_APPLICATION_DOCUMENT: "uploaded the application document {file_name}",
    AuditType.DELETE_APPLICATION_DOCUMENT: "deleted the application document {file_name}",
    AuditType.UPLOAD_CASE_DOCUMENT: "uploaded the case document {file_name}",
    AuditType.GENERATE_CASE_DOCUMENT: "generated the case document {file_name} from template {template}",
    AuditType.ADD_CASE_OFFICER_TO_CASE: "set {case_officer} as the Case Officer",
    AuditType.REMOVE_CASE_OFFICER_FROM_CASE: "removed {case_officer} as the Case Officer",
    AuditType.GRANTED_APPLICATION: "granted licence for {licence_duration} months starting from {start_date}",
    AuditType.FINALISED_APPLICATION: "finalised the application",
    AuditType.UNASSIGNED_QUEUES: "marked themselves as done for this case on the following queues: {queues}",
    AuditType.UNASSIGNED: "marked themselves as done for this case",
    AuditType.UPDATED_LETTER_TEMPLATE_NAME: "updated letter template name from {old_name} to {new_name}",
    AuditType.ADDED_LETTER_TEMPLATE_CASE_TYPES: "added letter template types: {new_case_types}",
    AuditType.UPDATED_LETTER_TEMPLATE_CASE_TYPES: "updated letter template types from {old_case_types} to {new_case_types}",
    AuditType.REMOVED_LETTER_TEMPLATE_CASE_TYPES: "removed letter template types: {old_case_types}",
    AuditType.ADDED_LETTER_TEMPLATE_DECISIONS: "added decisions: {new_decisions}",
    AuditType.UPDATED_LETTER_TEMPLATE_DECISIONS: "updated decisions from {old_decisions} to {new_decisions}",
    AuditType.REMOVED_LETTER_TEMPLATE_DECISIONS: "removed decisions: {old_decisions}",
    AuditType.UPDATED_LETTER_TEMPLATE_PARAGRAPHS: "updated letter paragraphs from {old_paragraphs} to {new_paragraphs}",
    AuditType.UPDATED_LETTER_TEMPLATE_LAYOUT: "updated letter layout from {old_layout} to {new_layout}",
    AuditType.UPDATED_LETTER_TEMPLATE_PARAGRAPHS_ORDERING: "updated letter paragraphs ordering",
    AuditType.CREATED_PICKLIST: "created the picklist item",
    AuditType.UPDATED_PICKLIST_TEXT: 'updated picklist text from "{old_text}" to "{new_text}"',
    AuditType.UPDATED_PICKLIST_NAME: 'updated picklist name from "{old_name}" to "{new_name}"',
    AuditType.DEACTIVATE_PICKLIST: "deactivated the picklist item",
    AuditType.REACTIVATE_PICKLIST: "reactivated the picklist item",
    AuditType.UPDATED_EXHIBITION_DETAILS_TITLE: 'updated exhibition title from "{old_title}" to "{new_title}"',
    AuditType.UPDATED_EXHIBITION_DETAILS_START_DATE: 'updated exhibition start date to "{new_first_exhibition_date}"',
    AuditType.UPDATED_EXHIBITION_DETAILS_REQUIRED_BY_DATE: 'updated required by date to "{new_required_by_date}"',
    AuditType.UPDATED_EXHIBITION_DETAILS_REASON_FOR_CLEARANCE: (
        'updated exhibition reason for clearance to "{new_reason_for_clearance}"'
    ),
    AuditType.UPDATED_ROUTE_OF_GOODS: 'updated {route_of_goods_field} from "{previous_value}" to "{new_value}"',
    AuditType.RERUN_ROUTING_RULES: "reran the routing rules",
}
