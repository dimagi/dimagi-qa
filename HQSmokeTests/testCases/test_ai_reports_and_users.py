"""
Test Module: test_ai_reports_and_users.py

Contains automated test cases for verifying report sections, user functionalities,
data export capabilities, and application accessibility in Web Apps.
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

@pytest.mark.report
@pytest.mark.smoke
def test_01_verify_all_report_sections_load_correctly(driver, settings):
    """
    Verify all report sections are displayed and load correctly.
    Steps:
    1. Navigate to the HQ home page
    2. Click on the Reports menu
    3. Verify Monitor Workers section is displayed
    4. Verify Inspect Data section is displayed
    5. Verify Manage Deployments section is displayed
    6. Verify Messaging section is displayed
    7. Open and run Worker Activity report
    8. Open and run Daily Form Activity report
    9. Open and run Case Activity report
    10. Open and run Submit History report
    Expected Result: All report sections are visible and each report loads with data.
    """
    home_page = HomePage(driver, settings)
    home_page.reports_menu()
    
    report_page = ReportPage(driver)
    assert report_page.is_present_and_displayed(report_page.get_element("Monitor Workers")), "Monitor Workers section not displayed"
    assert report_page.is_present_and_displayed(report_page.get_element("Inspect Data")), "Inspect Data section not displayed"
    assert report_page.is_present_and_displayed(report_page.get_element("Manage Deployments")), "Manage Deployments section not displayed"
    assert report_page.is_present_and_displayed(report_page.get_element("Messaging")), "Messaging section not displayed"

    print("All report sections are displayed.")
    
    report_page.worker_activity_report()
    assert report_page.check_if_report_loaded(), "Worker Activity report did not load with data"
    print("Worker Activity report loaded successfully.")
    
    report_page.daily_form_activity_report()
    assert report_page.check_if_report_loaded(), "Daily Form Activity report did not load with data"
    print("Daily Form Activity report loaded successfully.")
    
    report_page.case_activity_report()
    assert report_page.check_if_report_loaded(), "Case Activity report did not load with data"
    print("Case Activity report loaded successfully.")
    
    report_page.submit_history_report()
    assert report_page.check_if_report_loaded(), "Submit History report did not load with data"
    print("Submit History report loaded successfully.")

@pytest.mark.users
@pytest.mark.mobileWorker
def test_02_create_new_mobile_worker_verify_in_list(driver, settings):
    """
    Create a new mobile worker and verify it appears in the list.
    Steps:
    1. Navigate to Users menu
    2. Click on Mobile Workers
    3. Click Add Mobile Worker
    4. Enter a unique username
    5. Enter a password
    6. Save the new mobile worker
    7. Search for the newly created worker in the list
    Expected Result: New mobile worker is created and visible in the mobile workers list.
    """
    username = "unique_user_" + str(int(time.time()))  # Generating a unique username

    home_page = HomePage(driver, settings)
    home_page.users_menu()
    
    mobile_worker_page = MobileWorkerPage(driver)
    mobile_worker_page.mobile_worker_menu()
    mobile_worker_page.create_mobile_worker()
    mobile_worker_page.mobile_worker_enter_username(username)
    mobile_worker_page.mobile_worker_enter_password(UserData.app_password)
    mobile_worker_page.click_create(username)
    print("New mobile worker created.")

    mobile_worker_page.search_user(username)
    assert mobile_worker_page.is_present_and_displayed(mobile_worker_page.get_element(username)), "New mobile worker not found in list"
    print("New mobile worker is present in the list.")

@pytest.mark.users
@pytest.mark.groups
def test_03_create_user_group_add_mobile_worker(driver, settings):
    """
    Create a user group and add a mobile worker to it.
    Steps:
    1. Navigate to Users menu
    2. Click on Groups
    3. Create a new group with a unique name
    4. Add an existing mobile worker to the group
    5. Save the group
    6. Verify the group appears in the groups list
    Expected Result: Group is created and the mobile worker is assigned to it.
    """
    group_name = "Group_" + str(int(time.time()))  # Generating a unique group name

    home_page = HomePage(driver, settings)
    home_page.users_menu()
    
    group_page = GroupPage(driver)
    group_page.click_group_menu()
    group_page.add_group(group_name)
    print(f"New group '{group_name}' created.")

    group_page.add_user_to_group(UserData.mobile_testuser, group_name)
    print(f"Mobile worker '{UserData.mobile_testuser}' added to group '{group_name}'.")

    assert group_page.is_present_and_displayed(group_page.get_element(group_name)), "New group not found in list"
    print("Group with mobile worker is present in the list.")

@pytest.mark.data
@pytest.mark.exports
def test_04_verify_export_data_functionality(driver, settings):
    """
    Verify export data functionality works.
    Steps:
    1. Navigate to Data menu
    2. Click on Export Data
    3. Create a new case export
    4. Verify the export appears in the exports list
    5. Download the export file
    Expected Result: Export file is created and downloaded successfully.
    """
    home_page = HomePage(driver, settings)
    home_page.data_menu()
    
    export_data_page = ExportDataPage(driver)
    export_name = UserData.case_export_name

    export_data_page.add_case_exports()
    export_data_page.case_exports(export_name)
    print(f"Case export '{export_name}' created.")

    assert export_data_page.verify_export_count(export_name), "Export not found in exports list"
    print("Export appears in the exports list.")
    
    export_data_page.download_export_without_condition(export_name)
    print("Export file downloaded successfully.")
    export_data_page.assert_downloaded_file(export_name, "Export file")

@pytest.mark.webApps
@pytest.mark.smoke
def test_05_verify_application_accessible_via_web_apps(driver, settings):
    """
    Verify the application is accessible via Web Apps.
    Steps:
    1. Navigate to Web Apps
    2. Verify the list of applications is displayed
    3. Open one of the available applications
    4. Verify the application menus are displayed
    Expected Result: Application loads correctly in Web Apps.
    """
    webapps = WebApps(driver, settings)
    webapps.open_app(UserData.village_application)
    webapps_page = WebAppsPage(driver)
    assert webapps_page.verify_apps_presence(), "Applications list not displayed"
    print("Applications list is displayed.")
    
    webapps.open_menu("Case List")
    assert webapps_page.is_present_and_displayed(webapps_page.get_element("Case List")), "Application menu not displayed correctly"
    print("Application menus are displayed correctly.")