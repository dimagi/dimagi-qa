import os
import time
import pytest

from AppSprintPerformanceTests.CICT.WorkflowActions.workflows.excel_actions import write_to_excel
from AppSprintPerformanceTests.CICT.WorkflowActions.workflows.hq_actions import HomePage
from common_utilities.decorators import first_dump_filename

from AppSprintPerformanceTests.CICT.UserInputs.ny_cict_user_inputs import NYUserData

"""Runs all workflows and captures the readings for the app versions before and after releases for two preconfigured users"""


@pytest.mark.parametrize("user", [NYUserData.ci_ct_user1, NYUserData.ci_ct_user2])
@pytest.mark.parametrize("application", [NYUserData.application_before_release, NYUserData.application_after_release])
@pytest.mark.repeat(NYUserData.repeat_count)
def test_app_workflows(driver, user, application, settings, appsite):
    """Repeat Count"""

    test_app_workflows.counter += 1

    """General workflows"""

    visible = HomePage(driver)
    visible.login_as_ci_ct_user(user, settings["url"])
    time.sleep(2)
    visible.break_locks_and_clear_user_data(project_space=NYUserData.project_space)
    time.sleep(2)
    visible.sync_application(username=user, application_name=application)
    time.sleep(2)
    visible.open_application(username=user, application_name=application)

    """CI workflows"""

    visible.all_cases_menu_load(username=user, application_name=application)
    visible.search_case_in_test(username=user, application_name=application, pre_configured_case=NYUserData.pre_configured_case)
    visible.open_case_detail(username=user, application_name=application, pre_configured_case=NYUserData.pre_configured_case)
    visible.case_menu_display(username=user, application_name=application)
    visible.open_case_investigation_form(username=user, application_name=application)
    visible.ci_form_answer_question(username=user, application_name=application, site=appsite)
    visible.ci_form_submission(username=user, application_name=application)

    """CM workflows"""

    visible.app_home_screen(application)
    visible.all_contacts_menu_load(username=user, application_name=application)
    visible.search_contact_in_test(username=user, application_name=application, pre_configured_contact=NYUserData.pre_configured_contact)
    visible.open_contact_detail(username=user, application_name=application)
    visible.contact_menu_display(username=user, application_name=application)
    visible.open_contact_monitoring_form(username=user, application_name=application)
    visible.cm_form_answer_question(username=user, application_name=application)
    visible.cm_form_submission(username=user, application_name=application)

    """Back to webapps workflows"""

    visible.back_to_webapps_home()

    """Write to excel"""

    workflows = ["sync_application",
                 "open_application",
                 "all_cases_menu_load",
                 "open_case_detail",
                 "case_menu_display",
                 "open_case_investigation_form",
                 "ci_form_answer_question",
                 "ci_form_submission",
                 "all_contacts_menu_load",
                 "open_contact_detail",
                 "contact_menu_display",
                 "open_contact_monitoring_form",
                 "cm_form_answer_question",
                 "cm_form_submission"]

    write_to_excel(username=user, application_name=application, site=appsite, workflows=workflows)
    if os.path.isfile(first_dump_filename) and test_app_workflows.counter == NYUserData.repeat_count:
        os.remove(first_dump_filename)
        test_app_workflows.counter = 0


test_app_workflows.counter = 0
