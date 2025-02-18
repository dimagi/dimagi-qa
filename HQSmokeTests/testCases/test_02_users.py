import random
import time

import pytest

from HQSmokeTests.userInputs.user_inputs import UserData
from common_utilities.generate_random_string import fetch_random_string
from HQSmokeTests.testPages.home.home_page import HomePage
from HQSmokeTests.testPages.users.mobile_workers_page import MobileWorkerPage
from HQSmokeTests.testPages.users.group_page import GroupPage
from HQSmokeTests.testPages.users.web_user_page import WebUsersPage

""""Contains test cases related to the User's Mobile Worker module"""

group_id = dict()
group_id["user"] = None
group_id["value"] = None
group_id["group_name"] = None
group_id["active"] = None

@pytest.mark.user
@pytest.mark.groups
@pytest.mark.user_profiles
@pytest.mark.user_fields
@pytest.mark.mobileWorker
def test_initial_cleanup_items_in_users_menu(driver, settings):
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


@pytest.mark.user
@pytest.mark.mobileWorker
@pytest.mark.run(order=0)
def test_case_02_create_mobile_worker(driver, settings):
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
    group_id["user"] = username
    return group_id["user"]


@pytest.mark.user
@pytest.mark.mobileWorker
def test_case_03_create_and_assign_user_field(driver, settings):
    if group_id["user"]==None:
        pytest.skip("Skipping as user name is null")
    create = MobileWorkerPage(driver)
    menu = HomePage(driver, settings)
    menu.users_menu()
    create.mobile_worker_menu()
    create.create_new_user_fields("user_field_" + fetch_random_string())
    create.select_mobile_worker_created(group_id["user"])
    create.enter_value_for_created_user_field()
    create.update_information()



@pytest.mark.user
@pytest.mark.groups
def test_case_05_create_group_and_assign_user(driver, settings):
    if group_id["user"]==None:
        pytest.skip("Skipping as user name is null")
    menu = HomePage(driver, settings)
    menu.users_menu()
    visible = GroupPage(driver)
    user = MobileWorkerPage(driver)
    user.mobile_worker_menu()
    visible.click_group_menu()
    visible.delete_test_groups()
    print("Deleted the group")
    group_name = visible.add_group()
    id_value = visible.add_user_to_group(group_id["user"], group_name)
    print(id_value, group_name)
    group_id["value"] = id_value
    group_id["group_name"] = group_name
    return group_id["value"], group_id["group_name"]



@pytest.mark.user
@pytest.mark.mobileWorker
@pytest.mark.groups
@pytest.mark.userImport
@pytest.mark.userExport
def test_case_10_download_and_upload_users(driver, settings):
    if group_id["user"]==None:
        pytest.skip("Skipping as user name is null")
    user = MobileWorkerPage(driver)
    home = HomePage(driver, settings)
    home.users_menu()
    newest_file = user.download_mobile_worker()
    print("Group ID:", group_id["value"])
    user.check_for_group_in_downloaded_file(newest_file, group_id["value"])
    user.remove_role_in_downloaded_file(newest_file, group_id["user"])
    home.users_menu()
    user.upload_mobile_worker()


@pytest.mark.user
@pytest.mark.groups
def test_case_05_edit_user_groups(driver, settings):
    if group_id["group_name"]==None:
        pytest.skip("Skipping as group name is null")
    menu = HomePage(driver, settings)
    menu.users_menu()
    edit = GroupPage(driver)
    edit.click_group_menu()
    edit.edit_existing_group(group_id["group_name"])
    edit.remove_user_from_group()


@pytest.mark.user
@pytest.mark.mobileWorker
def test_case_04_deactivate_user(driver, settings):
    if group_id["user"]==None:
        pytest.skip("Skipping as user name is null")
    user = MobileWorkerPage(driver)
    menu = HomePage(driver, settings)
    menu.users_menu()
    user.mobile_worker_menu()
    text = user.deactivate_user(group_id["user"])
    user.verify_deactivation_via_login(group_id["user"], text)
    group_id["active"] = "No"


@pytest.mark.user
@pytest.mark.mobileWorker
def test_case_04_reactivate_user(driver, settings):
    if group_id["user"]==None or group_id["active"] == None:
        pytest.skip("Skipping as user/active name is null")
    user = MobileWorkerPage(driver)
    menu = HomePage(driver, settings)
    menu.users_menu()
    user.mobile_worker_menu()
    text = user.reactivate_user(group_id["user"])
    user.verify_reactivation_via_login(group_id["user"], text)


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

@pytest.mark.user
@pytest.mark.webUser
@pytest.mark.userInvitation
def test_case_13_new_webuser_invitation(driver, settings):
    menu = HomePage(driver, settings)
    webuser = WebUsersPage(driver)
    menu.users_menu()
    webuser.invite_new_web_user('admin')
    webuser.assert_invitation_sent()
    # yahoo_password = settings['invited_webuser_password']
    # webuser.assert_invitation_received(UserData.yahoo_url, UserData.yahoo_user_name, yahoo_password)
    # webuser.accept_webuser_invite(UserData.yahoo_user_name, yahoo_password)
    # login = LoginPage(driver, settings["url"])
    # login.login(settings["login_username"], settings["login_password"])
    webuser.delete_invite()


@pytest.mark.user
@pytest.mark.webUsers
@pytest.mark.downloadUsers
@pytest.mark.uploadUsers
def test_case_57_download_and_upload_web_users(driver):
    user = WebUsersPage(driver)
    user.download_web_users()
    user.upload_web_users()
