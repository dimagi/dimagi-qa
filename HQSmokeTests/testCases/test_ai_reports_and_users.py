"""
This module tests report visibility and loading, user creation,
user group management, export functionality, and web app access.
"""

import pytest
from common_utilities.selenium.webapps import WebApps
from common_utilities.hq_login.login_page import LoginPage
from HQSmokeTests.testPages.reports.report_page import ReportPage
from HQSmokeTests.testPages.home.home_page import HomePage
from HQSmokeTests.testPages.users.mobile_workers_page import MobileWorkerPage
from HQSmokeTests.testPages.users.group_page import GroupPage
from HQSmokeTests.testPages.data.export_data_page import ExportDataPage
from HQSmokeTests.testPages.webapps.web_apps_page import WebAppsPage
from HQSmokeTests.userInputs.user_inputs import UserData

@pytest.mark.reports
def test_01_verify_report_sections_displayed(driver, settings):
    """Verify all report sections are displayed and load correctly."""
    print("Step 1: Navigate to the HQ home page")
    home_page = HomePage(driver, settings)
    home_page.reports_menu()
    
    reports_page = ReportPage(driver, settings)

    print("Step 3: Verify Monitor Workers section is displayed")
    assert home_page.is_present_and_displayed(reports_page.get_element("locator_for_monitor_workers")), "Monitor Workers section not found"

    print("Step 4: Verify Inspect Data section is displayed")
    assert home_page.is_present_and_displayed(reports_page.get_element("locator_for_inspect_data")), "Inspect Data section not found"

    print("Step 5: Verify Manage Deployments section is displayed")
    assert home_page.is_present_and_displayed(reports_page.get_element("locator_for_manage_deployments")), "Manage Deployments section not found"

    print("Step 6: Verify Messaging section is displayed")
    assert home_page.is_present_and_displayed(reports_page.get_element("locator_for_messaging")), "Messaging section not found"

    print("Step 7: Open and run the Worker Activity report")
    reports_page.worker_activity_report()
    assert reports_page.check_if_report_loaded(), "Worker Activity report failed to load data"

    print("Step 8: Open and run the Daily Form Activity report")
    reports_page.daily_form_activity_report()
    assert reports_page.check_if_report_loaded(), "Daily Form Activity report failed to load data"

    print("Step 9: Open and run the Case Activity report")
    reports_page.case_activity_report()
    assert reports_page.check_if_report_loaded(), "Case Activity report failed to load data"

    print("Step 10: Open and run the Submit History report")
    reports_page.submit_history_report()
    assert reports_page.check_if_report_loaded(), "Submit History report failed to load data"

@pytest.mark.users
def test_02_create_mobile_worker(driver, settings):
    """Create a new mobile worker and verify it appears in the list."""
    home_page = HomePage(driver, settings)
    home_page.users_menu()
    
    mobile_worker_page = MobileWorkerPage(driver, settings)
    
    print("Step 2: Click on Mobile Workers")
    mobile_worker_page.mobile_worker_menu()

    print("Step 3: Click Add Mobile Worker")
    mobile_worker_page.create_mobile_worker()
    
    username = f"user_{str(int(time.time()))}"
    password = UserData.app_password

    print(f"Step 4: Enter a unique username: {username}")
    mobile_worker_page.mobile_worker_enter_username(username)

    print("Step 5: Enter a password")
    mobile_worker_page.mobile_worker_enter_password(password)

    print("Step 6: Save the new mobile worker")
    mobile_worker_page.click_create(username)
    
    print("Step 7: Search for the newly created worker in the list")
    assert mobile_worker_page.search_user(username), f"Mobile worker {username} not found in the list"

@pytest.mark.users
def test_03_create_user_group_and_add_worker(driver, settings):
    """Create a user group and add a mobile worker to it."""
    home_page = HomePage(driver, settings)
    home_page.users_menu()
    
    group_page = GroupPage(driver, settings)
    
    print("Step 2: Click on Groups")
    group_page.click_group_menu()

    group_name = f"group_{str(int(time.time()))}"
    print(f"Step 3: Create a new group with a unique name: {group_name}")
    group_page.add_group(group_name)
    
    username = UserData.app_login
    print(f"Step 4: Add an existing mobile worker {username} to the group")
    group_page.add_user_to_group(username, group_name)
    
    print("Step 5: Save the group")
    print("Step 6: Verify the group appears in the groups list")
    assert group_page.is_present_and_displayed(group_page.get_element("locator_for_group", group_name)), f"Group {group_name} not found"

@pytest.mark.data
def test_04_verify_export_data_functionality(driver, settings):
    """Verify export data functionality works."""
    home_page = HomePage(driver, settings)
    home_page.data_menu()
    
    export_data_page = ExportDataPage(driver, settings)
    
    print("Step 2: Click on Export Data")
    export_data_page.prepare_and_download_export(UserData.case_export_name)
    
    print("Step 3: Create a new case export")
    export_data_page.add_case_exports()
    
    print("Step 4: Verify the export appears in the exports list")
    assert export_data_page.verify_export_count(UserData.case_export_name), "Export not found in the list"
    
    print("Step 5: Download the export file")
    export_data_page.create_dse_and_download(UserData.case_export_name, type="case")

@pytest.mark.webApps
def test_05_verify_application_access_via_web_apps(driver, settings):
    """Verify application is accessible via Web Apps."""
    home_page = HomePage(driver, settings)
    home_page.web_apps_menu()
    
    webapps_page = WebAppsPage(driver, settings)
    
    print("Step 2: Verify the list of applications is displayed")
    assert webapps_page.verify_apps_presence(), "List of applications not displayed"
    
    app_name = UserData.village_application
    print(f"Step 3: Open the available application: {app_name}")
    webapps_page.login_as(app_name)
    
    print("Step 4: Verify the application menus are displayed")
    assert webapps_page.is_present_and_displayed(webapps_page.get_element("locator_for_app_menus")), "Application menus not displayed"