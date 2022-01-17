from HQSmokeTests.testPages.others.home_page import HomePage
from HQSmokeTests.testPages.applications.application_page import ApplicationPage
from HQSmokeTests.testPages.data.export_data_page import ExportDataPage
from HQSmokeTests.testPages.reports.report_page import ReportPage
from HQSmokeTests.testPages.users.group_page import GroupPage
from HQSmokeTests.testPages.users.mobile_workers_page import MobileWorkerPage
from HQSmokeTests.testPages.users.org_structure_page import OrganisationStructurePage
from HQSmokeTests.testPages.users.roles_permissions_page import RolesPermissionPage


def test_cleanup(driver):
    clean = MobileWorkerPage(driver)
    clean2 = GroupPage(driver)
    clean3 = RolesPermissionPage(driver)
    clean4 = OrganisationStructurePage(driver)
    clean5 = ExportDataPage(driver)
    clean6 = ApplicationPage(driver)
    clean7 = ReportPage(driver)

    clean.mobile_worker_menu()
    clean.select_mobile_worker_created()
    clean.cleanup_mobile_worker()
    print("Deleted the mobile worker")

    clean.mobile_worker_menu()
    clean.edit_user_field()
    clean.cleanup_user_field()
    clean.save_field()
    print("Deleted the user field")

    clean.mobile_worker_menu()
    clean2.click_group_menu()
    clean2.cleanup_group()
    print("Deleted the group")

    clean3.roles_menu_click()
    clean3.cleanup_role()
    print("Deleted the role")

    clean4.cleanup()
    print("Deleted the location and location field")







