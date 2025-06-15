import os
import random
import time

import pandas as pd
from openpyxl import load_workbook
from selenium.webdriver import Keys

from common_utilities.selenium.base_page import BasePage
from common_utilities.path_settings import PathSettings
from common_utilities.generate_random_string import fetch_random_string, fetch_phone_number
from HQSmokeTests.userInputs.user_inputs import UserData
from HQSmokeTests.testPages.users.org_structure_page import latest_download_file, wait_for_download_to_finish
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By

""""Contains test page elements and functions related to the User's Mobile Workers module"""


class MobileWorkerPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

        # self.username = random.choice(UserData.mobile_username_list)
        # self.user = random.choice(UserData.mobile_user_list)
        self.file_new_name = "mobile_workers_" + str(fetch_random_string()) + ".xlsx"
        self.to_be_edited_file = os.path.abspath(
            os.path.join(UserData.USER_INPUT_BASE_DIR, "test_data/mobile_workers.xlsx")
            )
        self.renamed_file = os.path.abspath(
            os.path.join(UserData.USER_INPUT_BASE_DIR, "test_data/" + self.file_new_name)
            )
        self.username_cell = "A2"

        self.users_menu_id = (By.ID, "ProjectUsersTab")
        self.login_as_username = "//h3/b[.='{}']"
        self.profile_name_text = "test_profile_" + fetch_random_string()
        self.phone_number = UserData.area_code + fetch_phone_number()
        self.delete_profile_name = "(//input[contains(@data-bind,'value: name')]//following::a[contains(@class,'danger') and contains(@href,'delete')])[{}]"
        self.username_link = "//a[./i[@class='fa fa-user']][strong[.='{}']]"
        self.user_field_input = (By.XPATH, "//input[contains(@data-bind,'value: slug')]")
        self.remove_choice_button = "((//input[contains(@data-bind,'value: slug')]//following::a[contains(@class,'danger')][1])//preceding::*[contains(@data-bind,'removeChoice')][1])[{}]"
        self.confirm_user_field_delete = (
            By.XPATH, "(//a[.='Cancel']//following-sibling::button[contains(@class,'danger')])[last()]")
        self.delete_user_field = "(//input[contains(@data-bind,'value: slug')]//following::a[contains(@class,'danger')][1])[{}]"
        self.delete_success_mw = (By.XPATH, "//div[@class='alert alert-margin-top fade in alert-success']")
        self.confirm_delete_mw = (By.ID, "delete-user-icon")
        self.enter_username = (By.XPATH, '//input[@data-bind="value: signOff, valueUpdate: \'textchange\'"]')
        self.delete_mobile_worker = (By.XPATH, "//div[@class='alert alert-danger']//i[@class='fa fa-trash']")
        self.actions_tab_link_text = (By.LINK_TEXT, "Actions")
        # remove these two after locators page creation: redundant code
        self.web_apps_menu_id = (By.ID, "CloudcareTab")
        self.show_full_menu_id = (By.ID, "commcare-menu-toggle")
        self.user_name_span = (By.CLASS_NAME, "user_username")
        self.search_mw = (By.XPATH, "//div[@class='ko-search-box']//input[@type='text']")
        self.clear_button_mw = (
            By.XPATH, "//div[@class='ko-search-box']//button[@data-bind='click: clearQuery']/i")
        self.search_button_mw = (
            By.XPATH, "//div[@class='ko-search-box']//button[@data-bind='click: clickAction, visible: !immediate']/i")
        self.webapp_working_as = (By.XPATH, "//span[contains(.,'Working as')]//b")
        self.webapp_login_confirmation = (By.ID, 'js-confirmation-confirm')
        # self.webapp_login_with_username = (By.XPATH, self.login_as_usernames)
        self.webapp_login = (By.XPATH, "(//div[@class='js-restore-as-item appicon appicon-restore-as'])")
        self.confirm_reactivate_xpath_list = (By.XPATH,
                                              "((//div[@class='modal-footer'])/button[@data-bind='click: function(user) { user.is_active(true); }'])")
        self.reactivate_buttons_list = "//td[./a/strong[text()='{}']]/following-sibling::td/div[contains(@data-bind,'visible: !is_active()')]/button[contains(.,'Reactivate')]"
        self.deactivate_button = "//td[./a/strong[text()='{}']]/following-sibling::td/div[contains(@data-bind,'visible: is_active()')]/button[contains(.,'Deactivate')]"
        self.confirm_deactivate_xpath_list = (
            By.XPATH, "((//div[@class='modal-footer'])/button[@class='btn btn-danger'])")
        self.deactivate_buttons_list = (
            By.XPATH, "(//td/div[@data-bind='visible: is_active()']/button[@class='btn btn-default'])")
        self.show_deactivated_users_btn = (
            By.XPATH,
            '//button[contains(.,"Show Deactivated Mobile Workers")][not(@style="display: none;")]')
        self.show_reactivated_users_btn = (
            By.XPATH,
            '//button[contains(.,"Show Active Mobile Workers")][not(@style="display: none;")]')
        self.usernames_xpath = (By.XPATH, "//td/a/strong[@data-bind='text: username']")
        self.page_xpath = (By.XPATH,
                           "(//span[@data-bind='text: $data, visible: !$parent.showSpinner() || $data != $parent.currentPage()'])")

        self.users_menu_id = (By.ID, "ProjectUsersTab")
        self.mobile_workers_menu_link_text = (By.LINK_TEXT, "Mobile Workers")
        self.create_mobile_worker_id = (By.ID, "new-user-modal-trigger")
        self.already_taken_error = (By.XPATH, "//span[contains(.,'is already taken')]")
        self.mobile_worker_username_id = (By.ID, "id_username")
        self.user_available_check = (By.XPATH, "//i[@class='fa fa-check' and @style='']")
        self.mobile_worker_password_id = (By.ID, "id_new_password")
        self.create_button_xpath = (By.XPATH, '//button[@type="submit"][contains(.,"Create")]')
        self.error_message = (
            By.XPATH, "//span[@data-bind ='visible: $root.usernameAvailabilityStatus() !== $root.STATUS.NONE']")
        self.cancel_button = (
            By.XPATH, "//button[@type='submit'][contains(.,'Create')]/preceding-sibling::button[text()='Cancel']")
        self.new_user_created_xpath = (By.XPATH,
                                       "//*[@class='success']//a[contains(@data-bind,'attr: {href: edit_url}, visible: user_id')]//following-sibling::strong")
        self.NEW = (By.XPATH, "//span[@class='text-success']")
        self.edit_user_field_xpath = (By.XPATH, "//a[contains(.,'Edit User Fields')]")
        self.add_field_xpath = (By.XPATH, "//button[@data-bind='click: addField']")
        self.user_property_xpath = (By.XPATH, "(//input[contains(@data-bind,'value: slug')])[last()]")
        self.label_xpath = (By.XPATH, "(//input[contains(@data-bind,'value: label')])[last()]")
        self.add_choice_button_xpath = (By.XPATH, "(//*[contains(@data-bind,'addChoice')])[last()]")
        self.choices_button_xpath = (By.XPATH, "(//*[contains(.,'Choices')])[last()]")
        self.choice_xpath = (By.XPATH, "(//input[contains(@data-bind,'value: value')])[last()]")
        self.save_field_id = (By.ID, "save-custom-fields")
        self.duplicate_field_error = (By.XPATH, "//div[contains(text(), 'was duplicated, key names must be unique')]")
        self.user_field_success_msg = (By.XPATH, "//div[contains(@class,'alert-success')]")
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
        self.deactivate_btn_xpath = "//td/a/strong[text()='{}']/following::td[5]/div[@data-bind='visible: is_active()']/button"
        self.confirm_deactivate = (By.XPATH, "(//button[@class='btn btn-danger'])[1]")
        self.view_all_link_text = (By.LINK_TEXT, "View All")
        self.search_user_web_apps = (By.XPATH, "//input[@placeholder='Filter workers']")
        self.search_button_we_apps = (By.XPATH, "//button/i[contains(@class,'search')]")

        self.field_tab = (By.XPATH, "//a[@href='#tabs-fields']")
        self.profile_tab = (By.XPATH, "//a[@href='#tabs-profiles']")
        self.add_new_profile = (By.XPATH, "//button[@data-bind='click: addProfile']")
        self.profile_name = (By.XPATH, "//tr[last()]//input[contains(@data-bind,'value: name')]")
        self.profile_edit_button = (By.XPATH, "//tr[last()]//a[contains(@class,'enum-edit')]")
        self.p1p2_profile_edit = "//tr//input[contains(@value,'{}')]//following-sibling::a[contains(@class,'enum-edit')]"
        self.profile_delete_button = (
            By.XPATH, "//tbody[@data-bind='foreach: profiles']//tr[last()]//td[last()]//i[@class='fa fa-times']")
        self.add_profile_item = (
            By.XPATH, "//div[contains(@class,'hq-enum-modal ')]//a[@data-enum-action='add']/i[@class='fa fa-plus']")
        self.delete_profile_item = (By.XPATH, "//div[contains(@class,'hq-enum-modal ')]//i[@class='fa fa-remove']")
        self.profile_key = (
            By.XPATH, "//div[contains(@class,'hq-enum-modal ')]//input[@class='form-control enum-key']")
        self.profile_value = (
            By.XPATH, "//div[contains(@class,'hq-enum-modal ')]//input[@class='form-control enum-value']")
        self.done_button = (By.XPATH, "//div[contains(@class,'hq-enum-modal ')]//button[@class='btn btn-primary']")
        self.delete_field_choice = (
            By.XPATH,
            "//tbody[@data-bind='sortable: data_fields']//tr[last()]//td//*[contains(@data-bind,'removeChoice')]")
        self.field_delete = (
            By.XPATH, "//tbody[@data-bind='sortable: data_fields']//tr[last()]//td[last()]//i[@class='fa fa-times']")
        self.profile_combobox = (
            By.XPATH, "//span[@aria-labelledby='select2-id_data-field-commcare_profile-container']")
        self.profile_selection = (By.XPATH, "//li[contains(text(),'" + self.profile_name_text + "')]")
        self.profile_dropdown = (By.XPATH, "//select[@name='data-field-commcare_profile']")
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
        self.successfully_uploaded = (By.XPATH, "//p[contains(text(),'Successfully uploaded')]")
        self.import_complete = (By.XPATH, "//legend[text()='Bulk upload complete.']")
        self.download_filter = (By.XPATH, "//button[contains(.,'Download')]")
        self.error_403 = (By.XPATH, "//h1[text()='403 Forbidden']")

        self.bulk_user_delete_button = (By.XPATH, "//a[contains(@href,'users/commcare/delete')]")
        self.successfully_deleted = (By.XPATH, "//text()[contains(.,'user&#40;s&#41; deleted')]")
        self.no_user_found = (By.XPATH, "//div[contains(@class,'alert')][contains(.,'No Mobile Workers were found')]")

        self.role_dropdown = (By.XPATH, "//select[@id='id_role']")

    def search_user(self, username):
        self.wait_for_element(self.search_mw)
        self.wait_to_click(self.clear_button_mw)
        self.send_keys(self.search_mw, username)
        self.wait_to_click(self.search_button_mw)


    def search_webapps_user(self, username):
        self.wait_to_click(self.web_apps_menu_id)
        self.wait_to_click(self.webapp_login)
        print("Waiting for the login page to load.....")
        time.sleep(2)
        self.wait_for_element(self.search_user_web_apps, 20)
        self.send_keys(self.search_user_web_apps, username)
        self.js_click(self.search_button_we_apps)
        time.sleep(2)

    def mobile_worker_menu(self):
        self.wait_to_click(self.mobile_workers_menu_link_text)
        assert "Mobile Workers : Users :: - CommCare HQ" in self.driver.title, "Unable find the Users Menu."

    def create_mobile_worker(self):
        try:
            self.wait_to_click(self.create_mobile_worker_id)
            self.wait_for_element(self.mobile_worker_username_id)
        except (TimeoutException, NoSuchElementException):
            print("TIMEOUT ERROR: Couldn't find create mobile worker button. ")

    def mobile_worker_enter_username(self, username):
        self.send_keys(self.mobile_worker_username_id, username)
        self.wait_for_element(self.user_available_check, 40)
        return username

    def mobile_worker_enter_password(self, password):
        self.send_keys(self.mobile_worker_password_id, password)

    def click_create(self, username):
        self.wait_to_click(self.create_button_xpath)
        time.sleep(2)
        self.wait_for_element(self.NEW, 200)
        new_user_created = self.get_text(self.new_user_created_xpath)
        print("Username is : " + new_user_created)
        assert username == new_user_created, "Could find the new mobile worker created"
        print("Mobile Worker Created")

    def check_for_group_in_downloaded_file(self, newest_file, group_id_value):
        path = os.path.join(PathSettings.DOWNLOAD_PATH, newest_file)
        print(path)
        time.sleep(2)
        data = pd.read_excel(path, sheet_name='groups')
        df = pd.DataFrame(data, columns=['id'])
        assert group_id_value in df['id'].values, "Group is not present"

    def edit_profile_in_downloaded_file(self, newest_file, user):
        path = os.path.join(PathSettings.DOWNLOAD_PATH, newest_file)
        print(path)
        time.sleep(2)
        data = pd.read_excel(path, sheet_name='users')
        df = pd.DataFrame(data)
        print("Before: ",df)
        df = df.drop(columns="phone-number 1")
        df = df.query("username == '" + user + "'")
        df.loc[(df['username'] == user), 'user_profile'] = UserData.p1p2_profile
        print("After: ",df)
        df.to_excel(path, sheet_name='users', index=False)

    def remove_role_in_downloaded_file(self, newest_file, user):
        path = os.path.join(PathSettings.DOWNLOAD_PATH, newest_file)
        print(path)
        time.sleep(2)
        data = pd.read_excel(path, sheet_name='users')
        df = pd.DataFrame(data)
        df = df.query("username == '" + user + "'")
        df = df.drop(columns="role")
        df.to_excel(path, sheet_name='users', index=False)

    def edit_user_field(self):
        self.wait_for_element(self.edit_user_field_xpath)
        self.js_click(self.edit_user_field_xpath)

    def add_field(self):
        self.wait_for_element(self.add_field_xpath)
        self.js_click(self.add_field_xpath)

    def add_user_property(self, user_pro):
        self.wait_for_element(self.user_property_xpath)
        self.clear(self.user_property_xpath)
        self.send_keys(self.user_property_xpath, user_pro + Keys.TAB)
        

    def add_label(self, label):
        self.clear(self.label_xpath)
        self.send_keys(self.label_xpath, label + Keys.TAB)
        

    def add_choice(self, choice):
        if self.is_present(self.choices_button_xpath):
            self.click(self.choices_button_xpath)
            time.sleep(2)
        else:
            print("Choices button not present")
        self.scroll_to_element(self.add_choice_button_xpath)
        self.wait_for_element(self.add_choice_button_xpath)
        self.wait_to_click(self.add_choice_button_xpath)
        self.clear(self.choice_xpath)
        self.send_keys(self.choice_xpath, choice + Keys.TAB)
        time.sleep(3)

    def save_field(self):
        if self.is_enabled(self.save_field_id):
            self.wait_for_element(self.save_field_id)
            self.click(self.save_field_id)
            time.sleep(2)
            assert self.is_present(self.user_field_success_msg) or self.is_present(
                self.duplicate_field_error
                ), "Unable to save userfield/profile."
            print("User Field/Profile Added or is already present")
        else:
            print("Save Button is not enabled")

    def select_mobile_worker_created(self, username):
        self.wait_to_click(self.mobile_worker_on_left_panel)
        self.search_user(username)
        if not self.is_present((By.XPATH, self.username_link.format(username))):
            print("Username not present")
            self.wait_to_click(self.show_deactivated_users_btn)
        self.wait_to_click((By.XPATH, self.username_link.format(username)))
        self.wait_for_element(self.user_name_span)
        print("Mobile Worker page opened.")

    def enter_value_for_created_user_field(self):
        self.scroll_to_element(self.additional_info_select)
        self.select_by_text(self.additional_info_select, "user_field_" + fetch_random_string())
        assert self.is_displayed(self.user_file_additional_info), "Unable to assign user field to user."

    def update_information(self):
        self.wait_to_click(self.update_info_button)
        time.sleep(4)
        assert self.is_displayed(self.user_field_success_msg), "Unable to update user."
        print("User Field Visible and Added for User")
        

    def deactivate_user(self, username):
        try:
            self.search_user(username)
            self.wait_for_element((By.XPATH, self.username_link.format(username)), 50)
            self.js_click(self.deactivate_buttons_list)
            self.wait_for_element(self.confirm_deactivate_xpath_list)
            self.js_click(self.confirm_deactivate_xpath_list)
            time.sleep(2)
            self.is_invisible(self.confirm_deactivate_xpath_list)
            assert self.is_present_and_displayed((By.XPATH, self.reactivate_buttons_list.format(username)), 20)
            self.mobile_worker_menu()
            self.wait_for_element(self.show_deactivated_users_btn)
            self.js_click(self.show_deactivated_users_btn)
            self.search_user(username)
            assert self.is_present_and_displayed((By.XPATH, self.reactivate_buttons_list.format(username)), 20)
            print("Deactivation successful")
            return "Success"
        except (TimeoutException, NoSuchElementException):
            print("TIMEOUT ERROR: Deactivation Unsuccessful.")
            return "Not Success"

    def verify_deactivation_via_login(self, username, text):
        if text == "Success":
            self.search_webapps_user(username)
            assert self.is_present_and_displayed((By.XPATH, self.login_as_username.format(username)),
                                                 10
                                                 ) == False, "Deactivated mobile worker still visible"
            self.wait_to_click(self.show_full_menu_id)
        else:
            assert False

    def reactivate_user(self, username):
        try:
            self.mobile_worker_menu()
            self.search_user(username)
            time.sleep(2)
            if self.is_present(self.no_user_found):
                if self.is_present(self.show_deactivated_users_btn):
                    print("No Active Mobile Workers found")
                    self.wait_to_click(self.show_deactivated_users_btn)
                    self.wait_for_element(self.show_reactivated_users_btn)
                    self.wait_for_element((By.XPATH, self.username_link.format(username)))
                    assert self.is_present((By.XPATH, self.reactivate_buttons_list.format(username))), "Mobile Worker is not in the deactivated users list"
                    print("Found Mobile worker in the deactivated users list")
                    self.js_click((By.XPATH, self.reactivate_buttons_list.format(username)))
                    self.wait_for_element(self.confirm_reactivate_xpath_list)
                    self.js_click(self.confirm_reactivate_xpath_list)
                    time.sleep(5)
                    self.wait_for_element((By.XPATH, self.deactivate_button.format(username)))
                    self.is_invisible(self.confirm_reactivate_xpath_list)
                    self.reload_page()
                    time.sleep(5)
                    self.mobile_worker_menu()
                    self.search_user(username)
                    assert self.is_present_and_displayed((By.XPATH, self.deactivate_button.format(username)), 20)
                    print("Reactivation successful")
                    time.sleep(2)
            elif self.is_present((By.XPATH, self.username_link.format(username))):
                print("This might be a rerun so skipping this steps")
                print("User is already activated")
                self.mobile_worker_menu()
                self.search_user(username)
                assert self.is_present_and_displayed((By.XPATH, self.deactivate_button.format(username)), 20)
                time.sleep(2)
            return "Success"
        except (TimeoutException, NoSuchElementException):
            print("TIMEOUT ERROR: Reactivation unsuccessful.")
            return "Not Success"

    def verify_reactivation_via_login(self, username, text):
        if text == "Success":
            self.search_webapps_user(username)
            assert self.is_present_and_displayed((By.XPATH, self.login_as_username.format(username))
                                                 ), "user is not activated"
            self.wait_to_click((By.XPATH, self.login_as_username.format(username)))
            self.wait_to_click(self.webapp_login_confirmation)
            self.wait_to_click(self.show_full_menu_id)
            self.wait_for_element(self.webapp_working_as, 50)
            login_username = self.get_text(self.webapp_working_as)
            print("Logged in user: ", login_username)
            print("Provided user: ", username)
            assert login_username == username, "Reactivated user is not visible."
            print("Working as " + username + " : Reactivation successful!")
            time.sleep(1)
        else:
            assert False

    def cleanup_mobile_worker(self):
        try:
            self.wait_to_click(self.actions_tab_link_text)
            self.wait_to_click(self.delete_mobile_worker)
            self.wait_to_clear_and_send_keys(self.enter_username, self.username + "@" + self.get_domain()
                                             + ".commcarehq.org"
                                             )
            self.wait_to_click(self.confirm_delete_mw)
        except (TimeoutException, NoSuchElementException):
            print("TIMEOUT ERROR: Could not delete the mobile worker")
            self.is_present_and_displayed(self.delete_success_mw), "Mobile User Deletion Unsuccessful"

    def cleanup_user_field(self):
        
        self.wait_to_click(self.delete_user_field)
        self.wait_to_click(self.confirm_user_field_delete)
        self.wait_to_click(self.done_button)

    def delete_test_user_field(self):
        try:
            time.sleep(3)
            list_profile = self.find_elements(self.user_field_input)
            print(len(list_profile))
            if len(list_profile) > 0:
                for i in range(len(list_profile))[::-1]:
                    time.sleep(3)
                    text = list_profile[i].get_attribute("value")
                    if "field_" in text:
                        if self.is_present((By.XPATH, self.remove_choice_button.format(str(i + 1)))):
                            self.wait_for_element((By.XPATH, self.remove_choice_button.format(str(i + 1))))
                            self.scroll_to_element((By.XPATH, self.remove_choice_button.format(str(i + 1))))
                            self.wait_to_click((By.XPATH, self.remove_choice_button.format(str(i + 1))))
                        else:
                            print("Choice is not present")
                        time.sleep(2)
                        self.wait_for_element((By.XPATH, self.delete_user_field.format(str(i + 1))))
                        self.wait_to_click((By.XPATH, self.delete_user_field.format(str(i + 1))))
                        # self.driver.find_element(By.XPATH,
                        #                          "(//input[contains(@data-bind,'value: slug')]//following::a[@class='btn btn-danger' and @data-toggle='modal'][1])[" + str(
                        #                              i + 1) + "]").click()
                        time.sleep(2)
                        self.wait_to_click(self.confirm_user_field_delete)
                        
                        list_profile = self.driver.find_elements(By.XPATH,
                                                                 "//input[contains(@data-bind,'value: slug')]"
                                                                 )
                    else:
                        print("Its not a test user field")
                self.save_field()
            else:
                print("No test user field present in the list")
        except Exception:
            print("All user fields might not have been deleted")

    def download_mobile_worker(self):
        self.mobile_worker_menu()
        self.wait_to_click(self.download_worker_btn)
        self.wait_for_element(self.download_filter)
        self.click(self.download_filter)
        time.sleep(2)
        try:
            self.wait_for_element(self.download_users_btn, 150)
            print("Clicking on Download link")
            self.js_click(self.download_users_btn)
            wait_for_download_to_finish()
        except TimeoutException:
            print("TIMEOUT ERROR: Still preparing for download..Celery might be down..")
            assert False
        # verify_downloaded_workers
        newest_file = latest_download_file()
        if '_users_' in newest_file:
            self.assert_downloaded_file(newest_file, "_users_"), "Download Not Completed!"
        else:
            print("Not the expected file. Downloading again...")
            self.js_click(self.download_users_btn)
            wait_for_download_to_finish()
            newest_file = latest_download_file()
            self.assert_downloaded_file(newest_file, "_users_"), "Download Not Completed!"
        print("File download successful")
        return newest_file

    def upload_mobile_worker(self):
        self.mobile_worker_menu()
        try:
            self.wait_to_click(self.bulk_upload_btn)
            newest_file = latest_download_file()
            file_that_was_downloaded = PathSettings.DOWNLOAD_PATH / newest_file
            time.sleep(2)
            self.send_keys(self.choose_file, str(file_that_was_downloaded))
            self.wait_and_sleep_to_click(self.upload)
            self.wait_for_element(self.successfully_uploaded, 150)
        except (TimeoutException, NoSuchElementException):
            print("TIMEOUT ERROR: Could not upload file")
        assert self.is_present_and_displayed(self.import_complete), "Upload Not Completed! Taking Longer to process.."
        print("File uploaded successfully")
        time.sleep(2)

    def click_profile(self):
        self.wait_for_element(self.profile_tab)
        self.wait_to_click(self.profile_tab)

    def click_fields(self):
        self.wait_to_click(self.field_tab)

    def add_profile(self, user_field):
        self.wait_to_click(self.add_new_profile)
        self.wait_to_clear_and_send_keys(self.profile_name, self.profile_name_text + Keys.TAB)
        time.sleep(2)
        self.wait_to_click(self.profile_edit_button)
        time.sleep(2)
        self.wait_for_element(self.add_profile_item)
        self.wait_to_click(self.add_profile_item)
        self.send_keys(self.profile_key, user_field)
        self.send_keys(self.profile_value, user_field)
        self.wait_to_click(self.done_button)

    def select_profile(self):
        self.wait_to_click(self.profile_combobox)
        
        self.wait_to_click(self.profile_selection)

    def add_phone_number(self):
        self.wait_to_clear_and_send_keys(self.phone_number_field, self.phone_number)
        
        self.wait_to_click(self.add_number_button)
        time.sleep(3)
        assert self.is_present_and_displayed(self.registered_phone_number), "Phone Number not registered."
        print("Phone Number registered successfully")

    def select_location(self):
        self.wait_to_click(self.location_tab)
        self.wait_to_click(self.location_combobox)
        self.wait_to_click(self.location_selection)
        self.wait_to_click(self.location_update_button)

    def remove_user_field(self):
        self.wait_to_click(self.delete_field_choice)
        self.wait_to_click(self.field_delete)
        self.wait_to_click(self.confirm_user_field_delete)

    def remove_profile(self, field):
        time.sleep(2)
        self.scroll_to_element((By.XPATH, self.p1p2_profile_edit.format(field)))
        self.wait_to_click((By.XPATH, self.p1p2_profile_edit.format(field)))
        time.sleep(2)
        self.wait_for_element(self.delete_profile_item)
        self.wait_to_click(self.delete_profile_item)
        
        self.wait_to_click(self.done_button)
        time.sleep(2)
        self.scroll_to_element(self.profile_delete_button)
        self.wait_to_click(self.profile_delete_button)
        time.sleep(3)
        self.scroll_to_element(self.confirm_user_field_delete)
        self.wait_to_click(self.confirm_user_field_delete)
        time.sleep(3)

    def delete_profile(self):
        try:
            list_profile = self.driver.find_elements(By.XPATH, "//input[contains(@data-bind,'value: name')]")
            if len(list_profile) > 0:
                for i in range(len(list_profile))[::-1]:
                    text = list_profile[i].get_attribute("value")
                    if "test_profile" in text:
                        self.scroll_to_element((By.XPATH, self.delete_profile_name.format(str(i + 1))))
                        self.wait_to_click((By.XPATH, self.delete_profile_name.format(str(i + 1))))
                        time.sleep(2)
                        self.wait_for_element(self.confirm_user_field_delete)
                        self.click(self.confirm_user_field_delete)
                        
                        list_profile = self.driver.find_elements(By.XPATH,
                                                                 "//input[contains(@data-bind,'value: name')]"
                                                                 )
                    else:
                        print("Its not a test profile")
                self.save_field()
            else:
                print("No test profile present in the list")
        except Exception:
            print("All profile might not have been deleted")

    def create_new_mobile_worker(self, user):
        self.create_mobile_worker()
        user = self.mobile_worker_enter_username(user)
        self.mobile_worker_enter_password(fetch_random_string())
        self.wait_to_click(self.create_button_xpath)
        time.sleep(4)
        self.is_present_and_displayed(self.NEW, 100)
        new_user_created = self.get_text(self.new_user_created_xpath)
        print("Username is : " + new_user_created)
        assert user == new_user_created, "Could find the new mobile worker created"
        print("Mobile Worker Created")

    def create_new_user_fields(self, userfield):
        self.edit_user_field()
        self.add_field()
        self.add_user_property(userfield)
        self.add_label(userfield)
        self.add_choice(userfield)
        self.save_field()

    def select_user_and_update_fields(self, user, field):
        self.select_mobile_worker_created(user)
        self.select_by_text(self.additional_info_select2, field)
        self.wait_to_click(self.update_info_button)
        assert self.is_displayed(self.user_file_additional_info2), "Unable to assign user field to user."

    def select_and_delete_mobile_worker(self, user):
        
        self.wait_to_click(self.mobile_worker_on_left_panel)
        
        self.wait_to_clear_and_send_keys(self.search_mw, user)
        
        self.wait_to_click(self.search_button_mw)
        time.sleep(3)
        self.wait_to_click((By.LINK_TEXT, user))
        try:
            self.wait_to_click(self.actions_tab_link_text)
            self.wait_to_click(self.delete_mobile_worker)
            self.wait_to_clear_and_send_keys(self.enter_username, user + "@" + self.get_domain()
                                             + ".commcarehq.org"
                                             )
            self.wait_to_click(self.confirm_delete_mw)
        except (TimeoutException, NoSuchElementException):
            print("TIMEOUT ERROR: Could not delete the mobile worker")
            self.is_present_and_displayed(self.delete_success_mw), "Mobile User Deletion Unsuccessful"

    def delete_bulk_users(self):
        try:
            latest = PathSettings.DOWNLOAD_PATH / self.download_mobile_worker()
            print(latest)
            new_data = pd.read_excel(latest, sheet_name='users')
            print('Original Row count: ', new_data.shape)
            # filter the test users
            new_data = new_data[new_data['username'].str.startswith(("user_", "username_"))]
            print('Filtered Row count: ', new_data.shape)
            new_data.drop(new_data.columns.difference(['username']), axis=1, inplace=True)
            print("New Data", new_data)
            print("New data values", new_data.values)
            if new_data.empty == False:
                writer = pd.ExcelWriter(latest, engine='openpyxl')
                # write data to the excel sheet
                new_data.to_excel(writer, sheet_name='users', index=False)
                # close file
                writer.close()
                self.bulk_delete_mobile_worker_upload(latest)
            else:
                print("No test users to delete")
        except Exception:
            print("All users might not have been deleted")

    def bulk_delete_mobile_worker_upload(self, file_path):
        self.mobile_worker_menu()
        try:
            self.wait_to_click(self.bulk_user_delete_button)
            time.sleep(2)
            self.send_keys(self.choose_file, str(file_path))
            self.wait_and_sleep_to_click(self.upload)
            
            self.wait_for_element(self.successfully_deleted, 70)
            # if self.is_present_and_displayed(self.successfully_deleted, 50):
            print("User(s) deleted successfully")
            # elif self.is_present_and_displayed(self.no_user_found, 50):
            #     print("No test user present")
        except (TimeoutException, NoSuchElementException):
            print("TIMEOUT ERROR: Could not upload file")

    def bulk_upload_mobile_worker(self):
        self.wait_to_click(self.users_menu_id)
        self.mobile_worker_menu()
        try:
            self.wait_to_click(self.bulk_upload_btn)
            self.edit_username_in_excel(self.to_be_edited_file, self.username_cell, self.renamed_file)
            
            self.wait_to_clear_and_send_keys(self.choose_file, self.renamed_file)
            self.wait_and_sleep_to_click(self.upload)
            self.wait_for_element(self.successfully_uploaded, 150)
        except (TimeoutException, NoSuchElementException):
            print("TIMEOUT ERROR: Could not upload file")
        assert self.is_present_and_displayed(self.import_complete), "Upload Not Completed! Taking Longer to process.."
        print("File uploaded successfully")

    def edit_username_in_excel(self, edited_file, cell, renamed_file, sheet_name='users'):
        workbook = load_workbook(filename=edited_file)
        sheet = workbook.active
        sheet[cell] = "user_p1p2_" + fetch_random_string()
        sheet.title = sheet_name
        workbook.save(filename=renamed_file)

    def update_role_for_mobile_worker(self, role):
        self.wait_for_element(self.role_dropdown)
        self.select_by_text(self.role_dropdown, role)
        self.update_information()

    def verify_role_for_mobile_worker(self, role):
        self.wait_for_element(self.role_dropdown)
        text = self.get_selected_text(self.role_dropdown)
        print(text)
        assert text == role, "Role is not the same as set before upload"

    def verify_profile_change(self, profile):
        self.wait_for_element(self.profile_dropdown)
        text = self.get_selected_text(self.profile_dropdown)
        print(text)
        assert text == profile, "Profile is not the same as set before upload"
