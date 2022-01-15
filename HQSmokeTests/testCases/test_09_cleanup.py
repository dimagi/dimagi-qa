import pytest

from HQSmokeTests.testPages.groupPage import GroupPage
from HQSmokeTests.testPages.mobileWorkersPage import MobileWorkerPage

@pytest.mark.order(1)
def test_cleanup_mobile_worker(driver):

    clean = MobileWorkerPage(driver)
    clean.mobile_worker_menu()
    clean.select_mobile_worker_created()
    clean.cleanup_mobile_worker()
    print("Deleted the mobile worker")


@pytest.mark.order(2)
def test_cleanup_user_field(driver):

    clean = MobileWorkerPage(driver)
    clean.mobile_worker_menu()
    clean.edit_user_field()
    clean.cleanup_user_field()
    clean.save_field()
    print("Deleted the user field")


@pytest.mark.order(3)
def test_cleanup_group(driver):

    clean = GroupPage(driver)
    clean2 = MobileWorkerPage(driver)
    clean2.mobile_worker_menu()
    clean.click_group_menu()
    clean.cleanup_group()
    print("Deleted the group")
