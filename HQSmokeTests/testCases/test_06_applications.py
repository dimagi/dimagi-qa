from HQSmokeTests.testPages.applications.app_preview import AppPreviewPage
from HQSmokeTests.testPages.applications.application_page import ApplicationPage
from HQSmokeTests.testPages.android.android_screen import AndroidScreen
from HQSmokeTests.testPages.home.home_page import HomePage
from HQSmokeTests.testPages.reports.report_page import ReportPage


def test_case_35_create_new_app(driver):

    load = ApplicationPage(driver)
    load.create_new_application()


def test_case_36_form_builder_explore(driver):

    load = ApplicationPage(driver)
    load.form_builder_exploration()


def test_case_37_form_xml_download_upload(driver):

    load = ApplicationPage(driver)
    load.form_xml_download_upload()

def test_case_39_settings_exploration(driver):

    load = ApplicationPage(driver)
    load.app_settings_exploration()
    load.delete_application()


def test_case_40_app_preview(driver):

    menu = HomePage(driver)
    menu.applications_menu()
    load = AppPreviewPage(driver)
    load.check_access_to_app_preview()
    load.submit_form_on_app_preview()


def test_case_38_create_new_build_deploy_to_mobile(driver, settings):

    load = ApplicationPage (driver)
    install_code, field_text = load.update_form_field()
    print(install_code, field_text)
    mobile = AndroidScreen(settings)
    mobile.install_app_and_submit_form(install_code, field_text)
    mobile.close_android_driver()
    home = HomePage(driver)
    home.reports_menu()
    report = ReportPage(driver)
    report.verify_app_data_submit_history(field_text)



