"""
This module contains tests for verifying the correct display and functionality of report sections, 
the creation of mobile workers and user groups, the export data functionality, and the accessibility of applications via Web Apps.
"""

import pytest
from common_utilities.selenium.webapps import WebApps
from common_utilities.hq_login.login_page import LoginPage
from HQSmokeTests.testPages.home.home_page import HomePage
from HQSmokeTests.testPages.reports.report_page import ReportPage
from HQSmokeTests.testPages.users.mobile_workers_page import MobileWorkerPage
from HQSmokeTests.testPages.users.group_page import GroupPage
from HQSmokeTests.testPages.data.export_data_page import ExportDataPage
from HQSmokeTests.testPages.webapps.web_apps_page import WebAppsPage
from HQSmokeTests.userInputs.user_inputs import UserData


@pytest.mark.reports
def test_01_verify_report_sections(driver, settings):
    """
    Verify all report sections are displayed and load correctly:
    1. Navigate to Reports menu
    2. Verify each report section is displayed
    3. Run various reports and ensure they load with data
    """
    home_page = HomePage(driver, settings)
    home_page.reports_menu()

    report_page = ReportPage(driver)
    assert report_page.is_present_and_displayed('Monitor Workers Section'), "Monitor Workers section is not displayed"
    assert report_page.is_present_and_displayed('Inspect Data Section'), "Inspect Data section is not displayed"
    assert report_page.is_present_and_displayed('Manage Deployments Section'), "Manage Deployments section is not displayed"
    assert report_page.is_present_and_displayed('Messaging Section'), "Messaging section is not displayed"

    report_page.worker_activity_report()
    assert report_page.check_if_report_loaded(), "Worker Activity report did not load correctly"

    report_page.daily_form_activity_report()
    assert report_page.check_if_report_loaded(), "Daily Form Activity report did not load correctly"
    
    report_page.case_activity_report()
    assert report_page.check_if_report_loaded(), "Case Activity report did not load correctly"

    report_page.submit_history_report()
    assert report_page.check_if_report_loaded(), "Submit History report did not load correctly"


@pytest.mark.users
def test_02_create_and_verify_mobile_worker(driver, settings):
    """
    Create a new mobile worker and verify it appears in the list:
    1. Navigate to Mobile Workers
    2. Add a new mobile worker
    3. Verify the worker is in the list
    """
    home_page = HomePage(driver, settings)
    home_page.users_menu()

    mobile_worker_page = MobileWorkerPage(driver)
    mobile_worker_page.mobile_worker_menu()

    new_username = "testworker" + str(settings["random"])
    mobile_worker_page.create_mobile_worker()
    mobile_worker_page.mobile_worker_enter_username(new_username)
    mobile_worker_page.mobile_worker_enter_password(UserData.app_password)
    mobile_worker_page.click_create(new_username)

    mobile_worker_page.search_user(new_username)
    assert mobile_worker_page.is_present_and_displayed(new_username), "New mobile worker is not visible in the list"


@pytest.mark.users
def test_03_create_and_verify_user_group(driver, settings):
    """
    Create a user group and add a mobile worker to it:
    1. Navigate to Groups
    2. Create a new group and add a mobile worker
    3. Verify the group appears in the list
    """
    home_page = HomePage(driver, settings)
    home_page.users_menu()

    group_page = GroupPage(driver)
    group_page.click_group_menu()

    new_group_name = "testgroup" + str(settings["random"])
    group_page.add_group(new_group_name)
    
    # Assuming a predefined user is added for simplicity
    existing_user = UserData.mobile_testuser
    group_page.add_user_to_group(existing_user, new_group_name)

    assert group_page.is_present_and_displayed(new_group_name), "Group is not visible in the list"


@pytest.mark.data
def test_04_verify_export_data_functionality(driver, settings):
    """
    Verify export data functionality works:
    1. Navigate to Export Data
    2. Create and verify a case export
    3. Download export file
    """
    home_page = HomePage(driver, settings)
    home_page.data_menu()

    export_data_page = ExportDataPage(driver)
    export_data_page.add_case_exports()
    new_export_name = UserData.case_export_name + str(settings["random"])
    export_data_page.case_exports(new_export_name)

    assert export_data_page.is_present_and_displayed(new_export_name), "Export is not visible in the export list"
    export_data_page.prepare_and_download_export(new_export_name)
    assert export_data_page.assert_downloaded_file(new_export_name), "Export file download failed"


@pytest.mark.webApps
def test_05_verify_application_access_via_web_apps(driver, settings):
    """
    Verify application is accessible via Web Apps:
    1. Navigate to Web Apps
    2. Ensure the list of applications is displayed
    3. Open an application and verify menus are displayed
    """
    web_apps_page = WebApps(driver, settings)
    web_apps_page.open_app(UserData.village_application)
    
    web_apps_page.navigate_to_breadcrumb('Menu')
    assert web_apps_page.is_present_and_displayed('App Menu'), "App menu did not display correctly in Web Apps"