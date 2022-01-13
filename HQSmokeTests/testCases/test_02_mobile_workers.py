from HQSmokeTests.userInputs.generateUserInputs import fetch_random_string
from HQSmokeTests.testPages.mobileWorkersPage import MobileWorkerPage


def test_01_create_mobile_worker(driver):
    worker = MobileWorkerPage(driver)
    worker.mobile_worker_menu()
    worker.create_mobile_worker()
    worker.mobile_worker_enter_username("username_" + str(fetch_random_string()))
    worker.mobile_worker_enter_password(fetch_random_string())
    worker.click_create()


def test_02_user_field_creation(driver):
    create = MobileWorkerPage(driver)
    create.mobile_worker_menu()
    create.edit_user_field()
    create.add_field()
    create.add_user_property("user_field_" + fetch_random_string())
    create.add_label("user_field_" + fetch_random_string())
    create.add_choice("user_field_" + fetch_random_string())
    create.save_field()


def test_03_user_field_visible(driver):
    visible = MobileWorkerPage(driver)
    visible.select_mobile_worker_created()
    visible.enter_value_for_created_user_field()
    visible.update_information()


def test_04_deactivate_and_reactivate_user(driver):
    user = MobileWorkerPage(driver)
    user.mobile_worker_menu()
    user.deactivate_user()
    user.verify_deactivation_via_login()
    user.reactivate_user()
    user.verify_reactivation_via_login()


def test_05_download_and_upload_users(driver):
    user = MobileWorkerPage(driver)
    user.download_mobile_worker()
    user.upload_mobile_worker()
