import pytest

from HQSmokeTests.testPages.applications.app_preview import AppPreviewPage
from HQSmokeTests.testPages.applications.application_page import ApplicationPage
from HQSmokeTests.testPages.android.android_screen import AndroidScreen
from HQSmokeTests.testPages.home.home_page import HomePage
from HQSmokeTests.testPages.reports.report_page import ReportPage
from HQSmokeTests.userInputs.user_inputs import UserData

""""Contains test cases related to the Application module"""


@pytest.mark.application
@pytest.mark.appBuilder
def test_case_35_create_new_app(driver):
    load = ApplicationPage(driver)
    load.create_new_application()


@pytest.mark.application
@pytest.mark.appBuilder
@pytest.mark.appSettings
def test_case_36_form_builder_explore(driver, settings):
    load = ApplicationPage(driver)
    load.form_builder_exploration()


@pytest.mark.application
@pytest.mark.appBuilder
@pytest.mark.appSettings
@pytest.mark.appActions
@pytest.mark.appDownloadXML
@pytest.mark.appUploadXML
def test_case_37_form_xml_download_upload(driver):
    load = ApplicationPage(driver)
    load.form_xml_download_upload()



@pytest.mark.application
@pytest.mark.appBuilder
@pytest.mark.appSettings
def test_case_39_settings_exploration(driver):
    load = ApplicationPage(driver)
    load.app_settings_exploration()
    load.delete_application()



@pytest.mark.application
@pytest.mark.appPreview
def test_case_40_app_preview(driver, settings):
    menu = HomePage(driver, settings)
    menu.applications_menu(UserData.reassign_cases_application)
    load = AppPreviewPage(driver)
    load.check_access_to_app_preview()
    load.submit_form_on_app_preview()


@pytest.mark.application
@pytest.mark.appBuilder
@pytest.mark.androidTest
@pytest.mark.reportSubmitHistory
@pytest.mark.appReleases
def test_case_38_create_new_build_deploy_to_mobile(driver, settings):
    if 'staging' in settings['url']:
        pytest.xfail("Failing on Staging due to QA-7314")
    load = ApplicationPage(driver)
    install_code, field_text = load.update_form_field()
    print(install_code, field_text)
    mobile = AndroidScreen(settings)
    mobile.install_app_and_submit_form(install_code, field_text)
    mobile.close_android_driver()
    home = HomePage(driver, settings)
    home.reports_menu()
    report = ReportPage(driver)
    report.verify_app_data_submit_history(field_text)

@pytest.mark.application
@pytest.mark.appSettings
def test_case_cleanup_app_deletion(driver):
    load = ApplicationPage(driver)
    apps = load.get_all_application_name()
    load.delete_all_application(apps)
