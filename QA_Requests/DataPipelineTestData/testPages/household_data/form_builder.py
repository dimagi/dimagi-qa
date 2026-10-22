"""Renders planned form events as XForm submissions for the HQ receiver.

The XML mirrors what CommCare produces for the "Household Registration" app:
question answers, a case transaction block and the form meta block.
"""
from xml.sax.saxutils import escape, quoteattr

from QA_Requests.DataPipelineTestData.userInputs.test_data import TestData

CASE_NS = "http://commcarehq.org/case/transaction/v2"
META_NS = "http://openrosa.org/jr/xforms"

# question id -> case property, per form (matches the app's case mappings)
REGISTER_PROPERTIES = ["hh_head_gender", "village", "district", "household_size", "children_under_5",
                       "water_source", "has_electricity", "livelihoods", "registration_date", "gps_location"]
FOLLOWUP_PROPERTIES = {"visit_date": "last_visit_date", "current_household_size": "household_size",
                       "members_present": "last_members_present", "attended_training": "attended_training",
                       "training_topic": "training_topic", "visit_notes": "last_visit_notes"}
CLOSE_PROPERTIES = {"close_date": "close_date", "close_reason": "close_reason",
                    "close_reason_other": "close_reason_other"}

# every question in form order; non-relevant ones are submitted empty, as CommCare does
QUESTIONS = {
    "register": ["hh_head_name"] + REGISTER_PROPERTIES,
    "followup": list(FOLLOWUP_PROPERTIES),
    "close": list(CLOSE_PROPERTIES),
}

FORMS = {
    "register": (TestData.register_xmlns, TestData.register_form_name),
    "followup": (TestData.followup_xmlns, TestData.followup_form_name),
    "close": (TestData.close_xmlns, TestData.close_form_name),
}


def _iso(dt):
    return dt.isoformat(timespec="milliseconds").replace("+00:00", "Z")


def _elements(values, prefix=""):
    return "".join(f"<{prefix}{k}>{escape(str(v))}</{prefix}{k}>" for k, v in values.items())


def _case_block(event, user_id):
    if event.kind == "register":
        updates = {p: event.answers[p] for p in REGISTER_PROPERTIES}
        create = (f"<n0:create><n0:case_name>{escape(event.case_name)}</n0:case_name>"
                  f"<n0:owner_id>{user_id}</n0:owner_id>"
                  f"<n0:case_type>{TestData.case_type}</n0:case_type></n0:create>")
        close = ""
    else:
        mapping = FOLLOWUP_PROPERTIES if event.kind == "followup" else CLOSE_PROPERTIES
        # non-relevant questions (training topic, "other" reason) don't update the case
        updates = {prop: event.answers[q] for q, prop in mapping.items() if q in event.answers}
        create = ""
        close = "<n0:close/>" if event.kind == "close" else ""
    return (f"<n0:case xmlns:n0=\"{CASE_NS}\" case_id=\"{event.case_id}\" "
            f"date_modified=\"{_iso(event.time_end)}\" user_id=\"{user_id}\">"
            f"{create}<n0:update>{_elements(updates, 'n0:')}</n0:update>{close}</n0:case>")


def _meta(event, username, user_id):
    return (f"<n1:meta xmlns:n1=\"{META_NS}\">"
            f"<n1:deviceID>{TestData.device_id}</n1:deviceID>"
            f"<n1:timeStart>{_iso(event.time_start)}</n1:timeStart>"
            f"<n1:timeEnd>{_iso(event.time_end)}</n1:timeEnd>"
            f"<n1:username>{escape(username)}</n1:username>"
            f"<n1:userID>{user_id}</n1:userID>"
            f"<n1:instanceID>uuid:{event.instance_id}</n1:instanceID>"
            f"<n1:appVersion>{escape(TestData.app_version_label)}</n1:appVersion>"
            f"</n1:meta>")


def build_form_xml(event, username, user_id, app_version):
    xmlns, name = FORMS[event.kind]
    return (f"<?xml version='1.0' ?>"
            f"<data xmlns:jrm=\"http://dev.commcarehq.org/jr/xforms\" xmlns=\"{xmlns}\" uiVersion=\"1\" "
            f"version=\"{app_version}\" name={quoteattr(name)}>"
            f"{_elements({q: event.answers.get(q, '') for q in QUESTIONS[event.kind]})}"
            f"{_case_block(event, user_id)}"
            f"{_meta(event, username, user_id)}"
            f"</data>")
