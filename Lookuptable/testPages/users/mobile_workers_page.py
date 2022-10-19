import os
import time

import pandas as pd

from common_utilities.selenium.base_page import BasePage
from common_utilities.path_settings import PathSettings
from common_utilities.generate_random_string import fetch_random_string, fetch_phone_number
from HQSmokeTests.userInputs.user_inputs import UserData
from HQSmokeTests.testPages.users.org_structure_page import latest_download_file
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By

""""Contains test page elements and functions related to the User's Mobile Workers module"""


class MobileWorkerPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

        self.username = "username_" + fetch_random_string()
        self.username2 = "user_" + fetch_random_string()
        self.login_as_username = (By.XPATH, "//h3/b[.='" + self.username + "']")
        self.profile_name_text = "test_profile_" + fetch_random_string()
        self.phone_number = UserData.area_code + fetch_phone_number()

        self.username_link = (By.LINK_TEXT, self.username)
        self.username2_link = (By.LINK_TEXT, self.username2)
        self.confirm_user_field_delete = (By.XPATH, "//button[@class='btn btn-danger']")
        self.delete_user_field = (By.XPATH,
                                  "(//input[@data-bind='value: slug'])[last()]//following::a[@class='btn btn-danger' and @data-toggle='modal'][1]")
        self.delete_success_mw = (By.XPATH, "//div[@class='alert alert-margin-top fade in alert-success']")
        self.confirm_delete_mw = (By.ID, "delete-user-icon")
        self.enter_username = (By.XPATH, '//input[@data-bind="value: signOff, valueUpdate: \'textchange\'"]')
        self.delete_mobile_worker = (By.XPATH, "//div[@class='alert alert-danger']//i[@class='fa fa-trash']")
        self.actions_tab_link_text = (By.LINK_TEXT, "Actions")
        # remove these two after locators page creation: redundant code
        self.web_apps_menu_id = (By.ID, "CloudcareTab")
        self.show_full_menu_id = (By.ID, "commcare-menu-toggle")
        self.search_mw = (By.XPATH, "//div[@class='ko-search-box']//input[@type='text']")
        self.search_button_mw = (
            By.XPATH, "//div[@class='ko-search-box']//button[@data-bind='click: clickAction, visible: !immediate']")
        self.webapp_working_as = (By.XPATH, "//div[@class='restore-as-banner module-banner']/b")
        self.webapp_login_confirmation = (By.ID, 'js-confirmation-confirm')
        # self.webapp_login_with_username = (By.XPATH, self.login_as_usernames)
        self.webapp_login = (By.XPATH, "(//div[@class='js-restore-as-item appicon appicon-restore-as'])")
        self.confirm_reactivate_xpath_list = (By.XPATH,
                                              "((//div[@class='modal-footer'])/button[@data-bind='click: function(user) { user.is_active(true); }'])")
        self.reactivate_buttons_list = (By.XPATH,
                                        "//td[./a/strong[text()='" + self.username + "']]/following-sibling::td/div[contains(@data-bind,'visible: !is_active()')]/button[contains(.,'Reactivate')]")
        self.deactivate_button = (By.XPATH,
                                  "//td[./a/strong[text()='" + self.username + "']]/following-sibling::td/div[contains(@data-bind,'visible: is_active()')]/button[contains(.,'Deactivate')]")
        self.confirm_deactivate_xpath_list = (
            By.XPATH, "((//div[@class='modal-footer'])/button[@class='btn btn-danger'])")
        self.deactivate_buttons_list = (
            By.XPATH, "(//td/div[@data-bind='visible: is_active()']/button[@class='btn btn-default'])")
        self.show_deactivated_users_btn = (
            By.XPATH,
            '//button[@data-bind="visible: !deactivatedOnly(), click: function() { deactivatedOnly(true); }"]')
        self.usernames_xpath = (By.XPATH, "//td/a/strong[@data-bind='text: username']")
        self.page_xpath = (By.XPATH,
                           "(//span[@data-bind='text: $data, visible: !$parent.showSpinner() || $data != $parent.currentPage()'])")

        self.users_menu_id = (By.ID, "ProjectUsersTab")
        self.mobile_workers_menu_link_text = (By.LINK_TEXT, "Mobile Workers")
        self.create_mobile_worker_id = (By.ID, "new-user-modal-trigger")
        self.mobile_worker_username_id = (By.ID, "id_username")
        self.mobile_worker_password_id = (By.ID, "id_new_password")
        self.create_button_xpath = (By.XPATH, '//button[@type="submit"]')
        self.error_message = (
            By.XPATH, "//span[@data-bind ='visible: $root.usernameAvailabilityStatus() !== $root.STATUS.NONE']")
        self.cancel_button = (By.XPATH, "//button[text()='Cancel']")
        self.new_user_created_xpath = (By.XPATH,
                                       "//*[@class='success']//a[contains(@data-bind,'attr: {href: edit_url}, visible: user_id')]//following-sibling::strong")
        self.NEW = (By.XPATH, "//span[@class='text-success']")
        self.edit_user_field_xpath = (By.XPATH, "//*[@id='btn-edit_user_fields']")
        self.add_field_xpath = (By.XPATH, "//button[@data-bind='click: addField']")
        self.user_property_xpath = (By.XPATH, "(//input[@data-bind='value: slug'])[last()]")
        self.label_xpath = (By.XPATH, "(//input[@data-bind='value: label'])[last()]")
        self.choices_button_xpath = (By.XPATH, "(//div[contains(text(), 'Choices')])[last()]")
        self.add_choice_button_xpath = (By.XPATH, "(//button[@data-bind='click: addChoice'])[last()]")
        self.choice_xpath = (By.XPATH, "(//input[@data-bind='value: value'])[last()]")
        self.save_field_id = (By.ID, "save-custom-fields")
        self.duplicate_field_error = (By.XPATH, "//div[contains(text(), 'was duplicated, key names must be unique')]")
        self.user_field_success_msg = (By.XPATH, "//div[@class='alert alert-margin-top fade in alert-success']")
        self.mobile_worker_on_left_panel = (By.XPATH, "//a[@data-title='Mobile Workers']")
        self.next_page_button_xpath = (By.XPATH, "//a[contains(@data-bind,'click: nextPage')]")
        self.additional_info_dropdown = (
            By.ID, "select2-id_data-field-user_field_" + fetch_random_string() + "-container")
        self.select_value_dropdown = (By.XPATH,
                                      "//select[@name = 'data-field-user_field_" + fetch_random_string() + "']/option[text()='user_field_" + fetch_random_string() + "']")
        self.additional_info_select = (
            By.XPATH, "//select[@name = 'data-field-user_field_" + fetch_random_string() + "']")
        self.additional_info_select2 = (By.XPATH, "//select[@name = 'data-field-field_" + fetch_random_string() + "']")

        self.additional_info_dropdown2 = (
            By.ID, "select2-id_data-field-" + "field_" + fetch_random_string() + "-container")
        self.select_value_dropdown2 = (By.XPATH,
                                       "//select[@name = 'data-field-field_" + fetch_random_string() + "']/option[text()='field_" + fetch_random_string() + "']")

        self.update_info_button = (By.XPATH, "//button[text()='Update Information']")
        self.user_file_additional_info = (
            By.XPATH, "//label[@for='id_data-field-user_field_" + fetch_random_string() + "']")
        self.user_file_additional_info2 = (
            By.XPATH, "//label[@for='id_data-field-field_" + fetch_random_string() + "']")
        self.deactivate_btn_xpath = (By.XPATH,
                                     "//td/a/strong[text()='" + self.username + "']/following::td[5]/div[@data-bind='visible: is_active()']/button")
        self.confirm_deactivate = (By.XPATH, "(//button[@class='btn btn-danger'])[1]")
        self.show_full_menu_id = (By.ID, "commcare-menu-toggle")
        self.view_all_link_text = (By.LINK_TEXT, "View All")
        self.search_user_web_apps = (By.XPATH, "//input[@placeholder='Filter workers']")
        self.search_button_we_apps = (By.XPATH, "//div[@class='input-group-btn']")

        self.field_tab = (By.XPATH, "//a[@href='#tabs-fields']")
        self.profile_tab = (By.XPATH, "//a[@href='#tabs-profiles']")
        self.add_new_profile = (By.XPATH, "//button[@data-bind='click: addProfile']")
        self.profile_name = (By.XPATH, "//tr[last()]//input[@data-bind='value: name']")
        self.profile_edit_button = (By.XPATH, "//tr[last()]//a[@class='btn btn-default enum-edit']")
        self.profile_delete_button = (
            By.XPATH, "//tbody[@data-bind='foreach: profiles']//tr[last()]//td[last()]//i[@class='fa fa-times']")
        self.add_profile_item = (
            By.XPATH, "//div[@class='modal fade hq-enum-modal in']//a[@data-enum-action='add']/i[@class='fa fa-plus']")
        self.delete_profile_item = (By.XPATH, "//div[@class='modal fade hq-enum-modal in']//i[@class='fa fa-remove']")
        self.profile_key = (
            By.XPATH, "//div[@class='modal fade hq-enum-modal in']//input[@class='form-control enum-key']")
        self.profile_value = (
            By.XPATH, "//div[@class='modal fade hq-enum-modal in']//input[@class='form-control enum-value']")
        self.done_button = (By.XPATH, "//div[@class='modal fade hq-enum-modal in']//button[@class='btn btn-primary']")

        self.field_delete = (
            By.XPATH, "//tbody[@data-bind='sortable: data_fields']//tr[last()]//td[last()]//i[@class='fa fa-times']")
        self.profile_combobox = (
            By.XPATH, "//span[@aria-labelledby='select2-id_data-field-commcare_profile-container']")
        self.profile_selection = (By.XPATH, "//li[contains(text(),'" + self.profile_name_text + "')]")
        self.phone_number_field = (By.XPATH, "//input[@name='phone_number']")
        self.add_number_button = (By.XPATH, "//button[.='Add Number']")
        self.registered_phone_number = (By.XPATH, "//label[contains(text(),'+" + self.phone_number + "')]")

        self.location_tab = (By.XPATH, "//a[@href='#commtrack-data']")
        self.location_combobox = (By.XPATH, "//span[@class='select2-selection select2-selection--multiple']")
        self.location_selection = (By.XPATH, "//li[contains(text(),'updated')]")
        self.location_update_button = (By.XPATH, "//button[contains(text(),'Update Location Settings')]")

        # Download and Upload
        self.download_worker_btn = (By.LINK_TEXT, "Download Mobile Workers")
        self.download_users_btn = (By.LINK_TEXT, "Download Users")
        self.bulk_upload_btn = (By.LINK_TEXT, "Bulk Upload")
        self.choose_file = (By.XPATH, "//input[@id='id_bulk_upload_file']")
        self.upload = (By.XPATH, "//button[@class='btn btn-primary disable-on-submit']")
        self.import_complete = (By.XPATH, "//legend[text()='Bulk upload complete.']")
        self.download_filter = (By.XPATH, "//button[@data-bind='html: buttonHTML']")
        self.error_403 = (By.XPATH, "//h1[text()='403 Forbidden']")

    def search_user(self):
        self.wait_to_clear_and_send_keys(self.search_mw, self.username)
        time.sleep(2)
        self.wait_to_click(self.search_button_mw)

    def search_webapps_user(self):
        self.wait_to_click(self.web_apps_menu_id)
        self.wait_to_click(self.webapp_login)
        time.sleep(1)
        self.send_keys(self.search_user_web_apps, self.username)
        self.wait_to_click(self.search_button_we_apps)
        time.sleep(5)

    def mobile_worker_menu(self):
        try:
            self.wait_to_click(self.users_menu_id)
            time.sleep(1)
        except TimeoutException:
            if not self.is_displayed(self.users_menu_id):
                self.click(self.show_full_menu_id)
                time.sleep(2)
                self.click(self.users_menu_id)
            elif self.is_displayed(self.error_403):
                self.driver.back()
                self.click(self.users_menu_id)
        except StaleElementReferenceException:
            self.driver.refresh()
            self.click(self.users_menu_id)
        self.wait_to_click(self.mobile_workers_menu_link_text)
        assert "Mobile Workers : Users :: - CommCare HQ" in self.driver.title, "Unable find the Users Menu."

    def create_mobile_worker(self):
        try:
            self.wait_to_click(self.create_mobile_worker_id)
            time.sleep(1)
        except (TimeoutException, NoSuchElementException):
            print("TIMEOUT ERROR: Couldn't find create mobile worker button. ")

    def mobile_worker_enter_username(self, username):
        self.send_keys(self.mobile_worker_username_id, username)

    def mobile_worker_enter_password(self, password):
        self.send_keys(self.mobile_worker_password_id, password)

    def click_create(self):
        self.wait_to_click(self.create_button_xpath)
        time.sleep(5)
        self.is_present_and_displayed(self.NEW)
        new_user_created = self.get_text(self.new_user_created_xpath)
        print("Username is : " + new_user_created)
        assert self.username == new_user_created, "Could find the new mobile worker created"
        print("Mobile Worker Created")

    def check_for_group_in_downloaded_file(self, newest_file, group_id_value):
        path = os.path.join(PathSettings.DOWNLOAD_PATH, newest_file)
        print(path)
        time.sleep(5)
        data = pd.read_excel(path, sheet_name='groups')
        df = pd.DataFrame(data, columns=['id'])
        assert group_id_value in df['id'].values, "Group is not present"

    def edit_user_field(self):
        self.wait_to_click(self.edit_user_field_xpath)

    def add_field(self):
        self.wait_to_click(self.add_field_xpath)

    def add_user_property(self, user_pro):
        self.clear(self.user_property_xpath)
        self.send_keys(self.user_property_xpath, user_pro)

    def add_label(self, label):
        self.clear(self.label_xpath)
        self.send_keys(self.label_xpath, label)

    def add_choice(self, choice):
        self.wait_to_click(self.choices_button_xpath)
        self.wait_to_click(self.add_choice_button_xpath)
        self.clear(self.choice_xpath)
        self.send_keys(self.choice_xpath, choice)

    def save_field(self):
        if self.is_enabled(self.save_field_id):
            self.wait_to_click(self.save_field_id)
            time.sleep(5)
            assert self.is_present(self.user_field_success_msg) or self.is_present(
                self.duplicate_field_error), "Unable to save userfield/profile."
            print("User Field/Profile Added or is already present")
        else:
            print("Save Button is not enabled")

    def select_mobile_worker_created(self):
        time.sleep(2)
        self.wait_to_click(self.mobile_worker_on_left_panel)
        time.sleep(2)
        self.search_user()
        time.sleep(3)
        if not self.is_present(self.username_link):
            self.click(self.show_deactivated_users_btn)
        self.click(self.username_link)

    def enter_value_for_created_user_field(self):
        self.select_by_text(self.additional_info_select, "user_field_" + fetch_random_string())
        assert self.is_displayed(self.user_file_additional_info), "Unable to assign user field to user."

    def update_information(self):
        time.sleep(2)
        self.wait_to_click(self.update_info_button)
        time.sleep(4)
        assert self.is_displayed(self.user_field_success_msg), "Unable to update user."
        print("User Field Visible and Added for User")
        time.sleep(2)

    def deactivate_user(self):
        try:
            self.search_user()
            time.sleep(1)
            self.wait_to_click(self.deactivate_buttons_list)
            self.wait_to_click(self.confirm_deactivate_xpath_list)
            time.sleep(5)
            assert self.is_present_and_displayed(self.reactivate_buttons_list)
        except (TimeoutException, NoSuchElementException):
            print("TIMEOUT ERROR: Deactivation Unsuccessful.")

    def verify_deactivation_via_login(self):
        self.search_webapps_user()
        assert self.is_present_and_displayed(self.login_as_username,
                                             10) == False, "Deactivated mobile worker still visible"
        self.wait_to_click(self.show_full_menu_id)

    def reactivate_user(self):
        try:
            time.sleep(1)
            self.mobile_worker_menu()
            self.wait_to_click(self.show_deactivated_users_btn)
            self.search_user()
            time.sleep(1)
            self.wait_to_click(self.reactivate_buttons_list)
            self.wait_to_click(self.confirm_reactivate_xpath_list)
            time.sleep(5)
            assert self.is_present_and_displayed(self.deactivate_button)
        except (TimeoutException, NoSuchElementException):
            print("TIMEOUT ERROR: Reactivation unsuccessful.")

    def verify_reactivation_via_login(self):
        self.search_webapps_user()
        assert self.is_present_and_displayed(self.login_as_username), "user is not activated"
        self.wait_to_click(self.login_as_username)
        self.wait_to_click(self.webapp_login_confirmation)
        self.click(self.show_full_menu_id)
        login_username = self.get_text(self.webapp_working_as)
        assert login_username == self.username, "Reactivated user is not visible."
        print("Working as " + self.username + " : Reactivation successful!")
        time.sleep(1)

    def cleanup_mobile_worker(self):
        try:
            self.wait_to_click(self.actions_tab_link_text)
            self.wait_to_click(self.delete_mobile_worker)
            self.wait_to_clear_and_send_keys(self.enter_username, self.username + "@" + self.get_domain()
                                             + ".commcarehq.org")
            self.wait_to_click(self.confirm_delete_mw)
        except (TimeoutException, NoSuchElementException):
            print("TIMEOUT ERROR: Could not delete the mobile worker")
            self.is_present_and_displayed(self.delete_success_mw), "Mobile User Deletion Unsuccessful"

    def cleanup_user_field(self):
        time.sleep(1)
        self.wait_to_click(self.delete_user_field)
        self.wait_to_click(self.confirm_user_field_delete)
        self.wait_to_click(self.done_button)

    def delete_test_user_field(self):
        list_profile = self.driver.find_elements(By.XPATH, "//input[@data-bind='value: slug']")
        if len(list_profile) > 0:
            for i in range(len(list_profile))[::-1]:
                text = list_profile[i].get_attribute("value")
                if "field_" in text:
                    self.driver.find_element(By.XPATH,
                                             "(//input[@data-bind='value: slug']//following::a[@class='btn btn-danger' and @data-toggle='modal'][1])[" + str(
                                                 i + 1) + "]").click()
                    self.wait_to_click(self.confirm_user_field_delete)
                    time.sleep(2)
                    list_profile = self.driver.find_elements(By.XPATH, "//input[@data-bind='value: slug']")
                else:
                    print("Its not a test user field")
            self.save_field()
        else:
            print("No test user field present in the list")

    def download_mobile_worker(self):
        time.sleep(1)
        self.mobile_worker_menu()
        self.wait_to_click(self.download_worker_btn)
        self.wait_to_click(self.download_filter)
        try:
            self.wait_and_sleep_to_click(self.download_users_btn)
            time.sleep(5)
        except TimeoutException:
            print("TIMEOUT ERROR: Still preparing for download..Celery might be down..")
            assert False
        # verify_downloaded_workers
        newest_file = latest_download_file()
        self.assert_downloaded_file(newest_file, "_users_"), "Download Not Completed!"
        print("File download successful")
        return newest_file

    def upload_mobile_worker(self):
        self.mobile_worker_menu()
        try:
            self.click(self.bulk_upload_btn)
            newest_file = latest_download_file()
            file_that_was_downloaded = PathSettings.DOWNLOAD_PATH / newest_file
            time.sleep(5)
            self.send_keys(self.choose_file, str(file_that_was_downloaded))
            self.wait_and_sleep_to_click(self.upload)
        except (TimeoutException, NoSuchElementException):
            print("TIMEOUT ERROR: Could not upload file")
        assert self.is_present_and_displayed(self.import_complete), "Upload Not Completed! Taking Longer to process.."
        print("File uploaded successfully")

    def click_profile(self):
        self.wait_to_click(self.profile_tab)

    def click_fields(self):
        self.click(self.field_tab)

    def add_profile(self, user_field):
        self.wait_to_click(self.add_new_profile)
        self.wait_to_clear_and_send_keys(self.profile_name, self.profile_name_text)
        time.sleep(2)
        self.wait_to_click(self.profile_edit_button)
        time.sleep(2)
        self.js_click(self.add_profile_item)
        self.send_keys(self.profile_key, user_field)
        self.send_keys(self.profile_value, user_field)
        self.wait_to_click(self.done_button)

    def select_profile(self):
        self.wait_to_click(self.profile_combobox)
        time.sleep(1)
        self.wait_to_click(self.profile_selection)

    def add_phone_number(self):
        self.wait_to_clear_and_send_keys(self.phone_number_field, self.phone_number)
        time.sleep(1)
        self.js_click(self.add_number_button)
        time.sleep(3)
        assert self.is_present_and_displayed(self.registered_phone_number), "Phone Number not registered."
        print("Phone Number registered successfully")

    def select_location(self):
        self.wait_to_click(self.location_tab)
        self.wait_to_click(self.location_combobox)
        self.wait_to_click(self.location_selection)
        self.wait_to_click(self.location_update_button)

    def remove_user_field(self):
        self.wait_to_click(self.field_delete)
        self.wait_to_click(self.confirm_user_field_delete)

    def remove_profile(self):
        self.wait_to_click(self.profile_edit_button)
        self.wait_to_click(self.delete_profile_item)
        self.wait_to_click(self.done_button)
        time.sleep(2)
        self.wait_to_click(self.profile_delete_button)
        self.wait_to_click(self.confirm_user_field_delete)

    def delete_profile(self):
        list_profile = self.driver.find_elements(By.XPATH, "//input[@data-bind='value: name']")
        if len(list_profile) > 0:
            for i in range(len(list_profile))[::-1]:
                text = list_profile[i].get_attribute("value")
                if "test_profile" in text:
                    self.driver.find_element(By.XPATH,
                                             "(//input[@data-bind='value: name']//following::a[@class='btn btn-danger' and @data-toggle='modal'][1])[" + str(
                                                 i + 1) + "]").click()
                    self.wait_to_click(self.confirm_user_field_delete)
                    time.sleep(2)
                    list_profile = self.driver.find_elements(By.XPATH, "//input[@data-bind='value: name']")
                else:
                    print("Its not a test profile")
            self.save_field()
        else:
            print("No test profile present in the list")

    def create_new_mobile_worker(self):
        self.create_mobile_worker()
        self.mobile_worker_menu()
        self.mobile_worker_enter_username("user_" + str(fetch_random_string()))
        self.mobile_worker_enter_password(fetch_random_string())
        self.wait_to_click(self.create_button_xpath)
        time.sleep(4)
        self.is_present_and_displayed(self.NEW)
        new_user_created = self.get_text(self.new_user_created_xpath)
        print("Username is : " + new_user_created)
        assert self.username2 == new_user_created, "Could find the new mobile worker created"
        print("Mobile Worker Created")

    def create_new_user_fields(self, userfield):
        self.edit_user_field()
        self.add_field()
        self.add_user_property(userfield)
        self.add_label(userfield)
        self.add_choice(userfield)
        self.save_field()

    def select_user_and_update_fields(self, user):
        time.sleep(2)
        self.wait_to_click(self.mobile_worker_on_left_panel)
        time.sleep(2)
        self.wait_to_clear_and_send_keys(self.search_mw, user)
        time.sleep(2)
        self.wait_to_click(self.search_button_mw)
        time.sleep(3)
        self.click(self.username2_link)
        self.select_by_text(self.additional_info_select2, "field_" + fetch_random_string())
        assert self.is_displayed(self.user_file_additional_info2), "Unable to assign user field to user."

    def select_and_delete_mobile_worker(self, user):
        time.sleep(2)
        self.wait_to_click(self.mobile_worker_on_left_panel)
        time.sleep(2)
        self.wait_to_clear_and_send_keys(self.search_mw, user)
        time.sleep(2)
        self.wait_to_click(self.search_button_mw)
        time.sleep(3)
        self.click(self.username2_link)
        try:
            self.wait_to_click(self.actions_tab_link_text)
            self.wait_to_click(self.delete_mobile_worker)
            self.wait_to_clear_and_send_keys(self.enter_username, self.username2 + "@" + self.get_domain()
                                             + ".commcarehq.org")
            self.wait_to_click(self.confirm_delete_mw)
        except (TimeoutException, NoSuchElementException):
            print("TIMEOUT ERROR: Could not delete the mobile worker")
            self.is_present_and_displayed(self.delete_success_mw), "Mobile User Deletion Unsuccessful"
