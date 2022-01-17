from HQSmokeTests.testPages.users.group_page import GroupPage
from HQSmokeTests.testPages.users.mobile_workers_page import MobileWorkerPage
from HQSmokeTests.testPages.users.org_structure_page import OrganisationStructurePage
from HQSmokeTests.testPages.users.roles_permissions_page import RolesPermissionPage


def test_cleanup(driver):
    clean = MobileWorkerPage(driver)
    clean2 = GroupPage(driver)
    clean3 = RolesPermissionPage(driver)
    clean4 = OrganisationStructurePage(driver)

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

    clean4.cleanup_location()
    print("Deleted the location and location field")
