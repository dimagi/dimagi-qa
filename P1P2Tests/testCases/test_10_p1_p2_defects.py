import pytest

from HQSmokeTests.testPages.applications.app_preview import AppPreviewPage
from HQSmokeTests.testPages.applications.application_page import ApplicationPage
from HQSmokeTests.testPages.data.export_data_page import ExportDataPage
from HQSmokeTests.testPages.data.import_cases_page import ImportCasesPage
from HQSmokeTests.testPages.email.email_verification import EmailVerification
from HQSmokeTests.testPages.home.home_page import HomePage
from HQSmokeTests.testPages.project_settings.repeaters_page import RepeatersPage
from HQSmokeTests.testPages.reports.report_page import ReportPage

from HQSmokeTests.userInputs.user_inputs import UserData

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
def test_case_77_create_new_app(driver, settings):
    load = ApplicationPage(driver)
    app_name = load.create_application_with_verifications()
    app = AppPreviewPage(driver)
    lat, lon = app.submit_form_with_loc()
    home = HomePage(driver, settings)
    home.reports_menu()
    report = ReportPage(driver)
    report.verify_form_in_submit_history(app_name, lat, lon)
    load.delete_p1p2_application(app_name)
    values['flag'] = True
    return values


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


