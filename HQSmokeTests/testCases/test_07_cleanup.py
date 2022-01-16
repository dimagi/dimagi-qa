import pytest

from HQSmokeTests.testPages.applications.application_page import ApplicationPage
from HQSmokeTests.testPages.data.export_data_page import ExportDataPage
from HQSmokeTests.testPages.reports.report_page import ReportPage
from HQSmokeTests.testPages.users.group_page import GroupPage
from HQSmokeTests.testPages.users.mobile_workers_page import MobileWorkerPage
from HQSmokeTests.testPages.users.org_structure_page import OrganisationStructurePage
from HQSmokeTests.testPages.users.roles_permissions_page import RolesPermissionPage


def test_cleanup_mobile_worker(driver):

    clean = MobileWorkerPage(driver)
    clean.mobile_worker_menu()
    clean.select_mobile_worker_created()
    clean.cleanup_mobile_worker()
    print("Deleted the mobile worker")


def test_cleanup_user_field(driver):

    clean = MobileWorkerPage(driver)
    clean.mobile_worker_menu()
    clean.edit_user_field()
    clean.cleanup_user_field()
    clean.save_field()
    print("Deleted the user field")


def test_cleanup_group(driver):

    clean = GroupPage(driver)
    clean2 = MobileWorkerPage(driver)
    clean2.mobile_worker_menu()
    clean.click_group_menu()
    clean.cleanup_group()
    print("Deleted the group")


@pytest.mark.order(after="test_TC_06_edit_role")
def test_cleanup_role(driver):

    clean = RolesPermissionPage(driver)
    clean.roles_menu_click()
    clean.cleanup_role()
    print("Deleted the role")


@pytest.mark.order(after="test_TC_11_download_and_upload_locations")
def test_cleanup_location(driver):
    org = OrganisationStructurePage(driver)
    org.cleanup()


@pytest.mark.order(after="test_TC_29_powerBI_tableau_integration_form")
def test_delete_all_bulk_exports(driver):
    export = ExportDataPage(driver)
    export.data_tab()
    export.delete_all_bulk_exports()


@pytest.mark.order(after="test_TC_39_settings_exploration")
def test_delete_app(driver):
    load = ApplicationPage(driver)
    load.delete_application()


@pytest.mark.order(after="test_TC_20_scheduled_report")
def test_delete_saved_and_scheduled_report(driver):
    load = ReportPage(driver)
    load.delete_scheduled_and_saved_reports()

