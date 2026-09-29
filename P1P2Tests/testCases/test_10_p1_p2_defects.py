import pytest

from HQSmokeTests.testPages.android.android_screen import AndroidScreen
from HQSmokeTests.testPages.applications.app_preview import AppPreviewPage
from HQSmokeTests.testPages.applications.application_page import ApplicationPage
from HQSmokeTests.testPages.data.export_data_page import ExportDataPage
from HQSmokeTests.testPages.data.import_cases_page import ImportCasesPage
from HQSmokeTests.testPages.email.email_verification import EmailVerification
from HQSmokeTests.testPages.home.home_page import HomePage
from HQSmokeTests.testPages.messaging.messaging_page import MessagingPage
from HQSmokeTests.testPages.project_settings.repeaters_page import RepeatersPage
from HQSmokeTests.testPages.reports.report_page import ReportPage
from HQSmokeTests.testPages.webapps.web_apps_page import WebAppsPage

from HQSmokeTests.userInputs.user_inputs import UserData
from common_utilities.generate_random_string import fetch_random_string

values = dict()
values['flag'] = False
@pytest.mark.report
@pytest.mark.reportCaseList
@pytest.mark.p1p2EscapeDefect
def test_case_70_case_owner_list(driver, settings):
    report = HomePage(driver, settings)
    report.reports_menu()
    load = ReportPage(driver)
    load.check_for_case_list_owner(settings['url'])


@pytest.mark.report
@pytest.mark.reportCaseList
@pytest.mark.p1p2EscapeDefect
def test_case_71_case_owner_list_explorer(driver, settings):
    report = HomePage(driver, settings)
    report.reports_menu()
    load = ReportPage(driver)
    load.check_for_case_list_explorer_owner(settings['url'])


@pytest.mark.report
@pytest.mark.p1p2EscapeDefect
@pytest.mark.xfail
def test_case_75_daily_form_activity(driver, settings):
    home = HomePage(driver, settings)
    home.reports_menu()
    report = ReportPage(driver)
    report.daily_form_activity_report()
    web_data = report.export_daily_form_activity_to_excel()
    email = EmailVerification(settings)
    link = email.get_hyperlink_from_latest_email(UserData.daily_form_activity, settings['url'])
    report.compare_web_with_email(link, web_data)

@pytest.mark.report
@pytest.mark.p1p2EscapeDefect
@pytest.mark.skip
def test_case_76_application_status(driver, settings):
    home = HomePage(driver, settings)
    home.reports_menu()
    report = ReportPage(driver)
    web_data = report.export_app_status_to_excel()
    email = EmailVerification(settings)
    link = email.get_hyperlink_from_latest_email(UserData.app_status, settings['url'])
    report.compare_app_status_web_with_email(link, web_data)


@pytest.mark.application
@pytest.mark.appBuilder
@pytest.mark.p1p2EscapeDefect
def test_case_77_create_new_app(driver, settings, rerun_count):
    if "india" in settings['url']:
        pytest.skip("Skipping for this month as limit exhausted")
    app_p1p2_name = f"App P1P2 {rerun_count}{fetch_random_string()}"
    load = ApplicationPage(driver)
    app_name = load.create_application_with_verifications(app_p1p2_name)
    app = AppPreviewPage(driver)
    lat, lon = app.submit_form_with_loc()
    home = HomePage(driver, settings)
    home.reports_menu()
    report = ReportPage(driver)
    report.verify_form_in_submit_history(app_name, lat, lon)
    load.delete_p1p2_application(app_name)
    values['flag'] = True
    # return values


@pytest.mark.projectSettings
@pytest.mark.createRepeater
@pytest.mark.editRepeater
@pytest.mark.p1p2EscapeDefect
def test_case_78_create_and_edit_repeaters(driver, settings):
    if not values['flag'] is True:
        pytest.skip("Skipping as the previous test failed")
    home = HomePage(driver, settings)
    home.project_settings_page(values['flag'])
    repeater = RepeatersPage(driver)
    repeater.add_repeater()
    repeater.edit_repeater()
    repeater.delete_repeater()


@pytest.mark.data
@pytest.mark.exportsFormData
@pytest.mark.p1p2EscapeDefect
def test_case_79_form_exports(driver, settings):
    if "india" in settings['url']:
        pytest.skip("Not much data present")
    home = HomePage(driver, settings)
    home.data_menu()
    export = ExportDataPage(driver)
    name = export.add_form_exports_reassign()
    export.verify_export_count(name)


@pytest.mark.data
@pytest.mark.exportsCaseData
@pytest.mark.p1p2EscapeDefect
def test_case_80_case_exports(driver, settings):
    home = HomePage(driver, settings)
    home.data_menu()
    export = ExportDataPage(driver)
    name = export.add_case_exports_reassign()
    export.verify_export_count(name)

@pytest.mark.data
@pytest.mark.importFromExcel
@pytest.mark.p1p2EscapeDefect
def test_case_81_parent_child_case_imports(driver, settings):
    if 'www' in settings['url'] or 'india' in settings['url']:
        pytest.skip("Setup not done in Prod yet")
    home = HomePage(driver, settings)
    home.data_menu()
    export = ExportDataPage(driver)
    assignment = export.check_for_related_cases(UserData.parent_1_id)
    filename = export.prepare_parent_child_import_excel(assignment)
    imp = ImportCasesPage(driver)
    home.data_menu()
    imp.import_parent_child_excel(filename)
    home.data_menu()
    export.verify_case_import(assignment)

@pytest.mark.projectSettings
@pytest.mark.createRepeater
@pytest.mark.editRepeater
@pytest.mark.p1p2EscapeDefect
def test_case_83_data_forwarding_add_edit(driver, settings):
    home = HomePage(driver, settings)
    home.project_settings_page()
    repeater = RepeatersPage(driver)
    repeater.delete_all_repeaters()
    repeater.add_repeater()
    repeater.edit_repeater()
    repeater.delete_repeater()

@pytest.mark.data
@pytest.mark.p1p2EscapeDefect
@pytest.mark.skip(reason=(
    "QA-8653: this Conditional Alert's case-type filter matched every "
    "existing case of the shared `reassign` case type on save (6,684+ in "
    "qa-automation-prod), sending one 'Owner' email per matching case and "
    "bouncing heavily at AWS SES. Reworked below to use a dedicated "
    "DoNotDelete app / case_dnd case type AND an added caseid-equals filter "
    "scoping the rule to the exact case this test submits, instead of "
    "matching every case_dnd case missing the target property (which would "
    "still reproduce the same bounce pattern more slowly, one more matching "
    "case per run). Neither the case_dnd switch nor the caseid-scoping has "
    "been run/verified live yet - do not remove this skip until it has "
    "been, or the mass-bounce risk could come right back."
))
def test_case_93_cond_alert_on_form_submit(driver, settings, rerun_count):
    menu = HomePage(driver, settings)
    msg = MessagingPage(driver)
    menu.messaging_menu()
    msg.remove_all_cond_alert()

    # Submit the case and look up its case_id BEFORE creating the rule (this
    # part reordered from the original rule-then-case flow) so the rule below
    # can be scoped to this exact case_id instead of matching every case_dnd
    # case that's ever missing the target property. CommCareHQ evaluates a
    # rule against currently-matching cases as soon as it's saved, so a rule
    # filtered on this case's own id still fires for it despite the case
    # already existing by then - it just does so via the save-time evaluation
    # path instead of the "new case matches an existing rule" path.
    menu.web_apps_menu()
    webapps = WebAppsPage(driver)
    webapps.verify_apps_presence()
    case_name = webapps.submit_case_change_register_form_no_value()

    menu = HomePage(driver, settings)
    menu.reports_menu()
    report = ReportPage(driver)
    case_id = report.get_case_id_from_case_list_explorer(case_name)

    menu.messaging_menu()
    cond_alert, subject = msg.create_cond_alert_for_doesnot_have_value(rerun_count, case_id=case_id)
    try:
        menu.applications_menu(UserData.dnd_application)
        load = ApplicationPage(driver)
        code = load.get_app_code(UserData.dnd_application)
        mobile = AndroidScreen(settings)
        mobile.verify_app_install(code)
        mobile.close_android_driver()
        export = ExportDataPage(driver)
        menu.data_menu()
        export.check_for_case_id(case_id)
        email = EmailVerification(settings)
        email.verify_email_sent(subject, settings['url'], sleep="YES")
    finally:
        # Removing the rule immediately (rather than waiting for the next
        # day's remove_all_cond_alert()) limits how long it stays active and
        # able to re-fire, e.g. via the "restart rule" retry path.
        menu.messaging_menu()
        msg.remove_cond_alert(cond_alert)

