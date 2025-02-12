import random
import time

import pytest

from HQSmokeTests.testPages.android.android_screen import AndroidScreen
from HQSmokeTests.testPages.applications.application_page import ApplicationPage
from HQSmokeTests.testPages.users.group_page import GroupPage
from HQSmokeTests.userInputs.user_inputs import UserData
from common_utilities.generate_random_string import fetch_random_string
from HQSmokeTests.testPages.home.home_page import HomePage
from HQSmokeTests.testPages.users.mobile_workers_page import MobileWorkerPage


""""Contains test cases related to the User's Mobile Worker module"""

group_id = dict()
group_id["user_new"] = "username_"+fetch_random_string()+"_new"



@pytest.mark.user
@pytest.mark.mobileWorker
@pytest.mark.mobileWorker
@pytest.mark.p1p2EscapeDefect
def test_case_89_verify_user_location_alert(driver, settings):
    mw = MobileWorkerPage(driver)
    menu = HomePage(driver, settings)
    menu.users_menu()
    mw.mobile_worker_menu()
    mw.select_mobile_worker_created(UserData.app_login)
    mw.select_location()
    mw.remove_location()
    mw.verify_location_alert_not_present()

@pytest.mark.user
@pytest.mark.mobileWorker
@pytest.mark.user_profiles
@pytest.mark.user_fields
@pytest.mark.user_organization
@pytest.mark.p1p2EscapeDefect
def test_case_54_add_custom_user_data_profile_to_mobile_worker(driver, settings):
    create = MobileWorkerPage(driver)
    menu = HomePage(driver, settings)
    menu.users_menu()
    create.delete_bulk_users()
    menu.users_menu()
    create.mobile_worker_menu()
    create.create_new_mobile_worker(group_id["user_new"])
    create.create_new_user_fields("field_" + fetch_random_string())
    create.click_profile()
    create.add_profile("field_" + fetch_random_string())
    create.save_field()
    create.select_user_and_update_fields(group_id["user_new"], "field_" + fetch_random_string())
    create.add_phone_number()
    create.select_profile()
    create.update_information()
    create.select_location()
    time.sleep(2)
    menu.users_menu()
    newest_file = create.download_mobile_worker()
    create.edit_profile_in_downloaded_file(newest_file, group_id["user_new"])
    menu.users_menu()
    create.upload_mobile_worker()
    create.select_mobile_worker_created(group_id["user_new"])
    create.verify_profile_change(UserData.p1p2_profile)
    create.mobile_worker_menu()
    create.delete_bulk_users()
    menu.users_menu()
    create.mobile_worker_menu()
    create.edit_user_field()
    create.click_profile()
    create.remove_profile()
    create.save_field()
    create.click_fields()
    create.remove_user_field()
    create.save_field()


@pytest.mark.user
@pytest.mark.groups
@pytest.mark.user_profiles
@pytest.mark.user_fields
@pytest.mark.mobileWorker
def test_aftertest_cleanup_items_in_users_menu(driver, settings):
    clean = MobileWorkerPage(driver)
    clean2 = GroupPage(driver)

    menu = HomePage(driver, settings)
    menu.users_menu()
    clean.delete_bulk_users()

    menu.users_menu()
    clean.mobile_worker_menu()
    clean.edit_user_field()
    clean.click_profile()
    clean.delete_profile()
    print("Removed all test profiles")

    menu.users_menu()
    clean.mobile_worker_menu()
    clean.edit_user_field()
    clean.delete_test_user_field()
    print("Deleted the user field")

    clean.mobile_worker_menu()
    clean2.click_group_menu()
    clean2.delete_test_groups()
    print("Deleted the group")


@pytest.mark.application
@pytest.mark.appSettings
@pytest.mark.p1p2EscapeDefect
def test_case_91_login_with_new_password(driver, settings):
    menu = HomePage(driver, settings)
    menu.applications_menu(UserData.village_application)
    load = ApplicationPage(driver)
    code = load.get_app_code(UserData.village_application)
    username = "username_" + fetch_random_string()
    worker = MobileWorkerPage(driver)
    menu = HomePage(driver, settings)
    menu.users_menu()
    worker.delete_bulk_users()
    worker.mobile_worker_menu()
    worker.create_mobile_worker()
    worker.mobile_worker_enter_username(username)
    worker.mobile_worker_enter_password(fetch_random_string())
    worker.click_create(username)
    mobile = AndroidScreen(settings)
    mobile.verify_login_with_old_password(code, username, fetch_random_string())
    worker.mobile_worker_menu()
    worker.select_mobile_worker_created(username)
    worker.reset_mobile_worker_password("new_"+fetch_random_string())
    mobile.verify_login_with_new_password(username, "new_"+fetch_random_string())
    mobile.close_android_driver()
