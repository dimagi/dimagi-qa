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
    """
        1. Navigate to Applications>New Application.
        2. Add few Surveys or Case List.
        3. Add few questions in the corresponding forms
        4. Click Save.
        5. Verify user is able to create a application using the app builder.
    """
    load = ApplicationPage(driver)
    load.create_new_application()


@pytest.mark.application
@pytest.mark.appBuilder
@pytest.mark.appSettings
def test_case_36_form_builder_explore(driver, settings):
    """
        1. Open the created Application
        2. Click through the settings pages of both the forms and the menus.
    """
    load = ApplicationPage(driver)
    load.form_builder_exploration()


@pytest.mark.application
@pytest.mark.appBuilder
@pytest.mark.appSettings
@pytest.mark.appActions
@pytest.mark.appDownloadXML
@pytest.mark.appUploadXML
def test_case_37_form_xml_download_upload(driver):
    """
        1. Go to Application, on the form settings' Actions tab, download the form XML
        2. Create a new form and on the Actions tab, upload the XML
        3. Ensure this new form is a copy of the original form
    """
    load = ApplicationPage(driver)
    load.create_new_application()
    load.form_xml_download_upload()



@pytest.mark.application
@pytest.mark.appBuilder
@pytest.mark.appSettings
def test_case_39_settings_exploration(driver):
    """
        1. Click on your new app's settings page
        2. Explore settings:
        Languages
        Multimedia
        Actions
        Add-ons
        Advanced Settings
    """
    load = ApplicationPage(driver)
    load.app_settings_exploration()
    load.delete_application()



@pytest.mark.application
@pytest.mark.appPreview
def test_case_40_app_preview(driver, settings):
    """
        1. Access App Preview
        2. Ensure you're able can access app preview and are able to submit a form using that tool
    """
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
    """
        1. After adding few questions in the form.
        2. Click on the application's name which says 'Updates are available'.
        3. Make a new version of this app.
        4. Verify you are able to publish the version of the app from deploy page.
        5. Deploy this app in mobile.
        6. Login into the app using mobile worker you just created above in the sheet.
        7. Verify you are able to login and access the form successfully
        8. Submit the form and ensure you can find your submissions in the Submit History Report
    """
    if 'staging' in settings['url']:
        pytest.xfail("Failing on Staging due to QA-7314")
    if  "eu" in settings["url"]:
        pytest.skip("App code is not getting displayed")
    if  "india" in settings["url"]:
        pytest.skip("App code limit exhausted for the month")
    load = ApplicationPage(driver)
    load.opening_dashboard()
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
    """
        1. Delete all the test apps created during script execution
    """
    load = ApplicationPage(driver)
    apps = load.get_all_application_name()
    load.delete_all_application(apps)
