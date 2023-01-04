import os
import time
from datetime import date

from HQSmokeTests.testPages.home.home_page import HomePage
from common_utilities.selenium.base_page import BasePage
from common_utilities.path_settings import PathSettings
from common_utilities.generate_random_string import fetch_random_string
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.by import By

""""Contains test page elements and functions related to the User's Organization structure module"""


def latest_download_file(type=".xlsx"):
    cwd = os.getcwd()
    try:
        os.chdir(PathSettings.DOWNLOAD_PATH)
        all_specific_files = filter(lambda x: x.endswith(type), os.listdir(os.getcwd()))
        files = sorted(all_specific_files, key=os.path.getctime)
        print(files)
        if files[-1].endswith(".log"):
            newest = sorted(files, key=os.path.getctime)[-2]
        elif files[-1].endswith(".xlsx"):
            newest = sorted(files, key=os.path.getctime)[-1]
        else:
            newest = max(files, key=os.path.getctime)
        print("File downloaded: " + newest)
        return newest
    finally:
        print("Restoring the path...")
        os.chdir(cwd)
        print("Current directory is-", os.getcwd())


class OrganisationStructurePage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

        self.new_location_name = "location_" + fetch_random_string()
        self.loc_field_name = "location_field_" + str(fetch_random_string())
        self.loc_level_name = "loc_level_" + fetch_random_string()

        self.org_menu_link_text = (By.LINK_TEXT, "Organization Structure")
        self.add_loc_btn_xpath = (
            By.XPATH, "//span[@data-bind='text: new_child_caption' and text()='New location at top level']")
        self.loc_name_xpath = (By.XPATH, "//input[@type='text']")
        self.create_loc_xpath = (By.XPATH, "//button[@type='submit']")
        self.loc_saved_success_msg = (By.XPATH, "//div[@class ='alert alert-margin-top fade in alert-success']")
        self.error_1_id = (By.ID, "error_1_id_name")
        self.edit_this_loc = (By.XPATH, "(//span[contains(text(),'updated_on:')])[1]")
        self.edit_loc_button_xpath = (By.XPATH,
                                      "(//span[contains(text(),'updated_on:')])[1]//preceding::a[@data-bind='attr: { href: loc_edit_url(uuid()) }'][1]")
        self.loc_name_input_id = (By.ID, "id_name")
        self.update_loc_xpath = (By.XPATH, "(//button[@type='submit'])[1]")
        self.location_created_xpath = (By.XPATH, "//span[text()='" + self.new_location_name + "']")
        self.renamed_location = (By.XPATH, "//span[text()='updated_on:" + str(date.today()) + "']")
        self.edit_loc_field_btn_xpath = (By.XPATH, "//a[@data-action='Edit Location Fields']")
        self.add_field_btn_xpath = (By.XPATH, "//button[@data-bind='click: addField']")
        self.loc_property_xpath = (By.XPATH, "(//input[@data-bind='value: slug'])[last()]")
        self.loc_label_xpath = (By.XPATH, "(//input[@data-bind='value: label'])[last()]")
        self.choice_selection = (By.XPATH, "(//div[contains(@data-bind, \"validationMode('choice')\")])[last()]")
        self.choices_button_xpath = (By.XPATH, "(//div[contains(text(), 'Choices')])[last()]")
        self.add_choice_btn_xpath = (By.XPATH, "(//button[@data-bind='click: addChoice'])[last()]")
        self.choice_xpath = (By.XPATH, "(//input[@data-bind='value: value'])[last()]")
        self.save_btn_id = (By.ID, "save-custom-fields")
        self.success_msg_xpath = (By.XPATH, "//div[@class='alert alert-margin-top fade in alert-success']")
        self.additional_info_drop_down = (
            By.XPATH, "//*[@id='select2-id_data-field-" + self.loc_field_name + "-container']")
        self.select_value_drop_down = (By.XPATH, "//li[text()='" + self.loc_field_name + "']")
        self.duplicate_msg_xpath = (By.XPATH, "//div[@class='alert alert-danger']")
        self.org_level_menu_link_text = (By.LINK_TEXT, "Organization Levels")
        self.new_org_level_btn_xpath = (By.XPATH, "//button[@data-bind='click: new_loctype']")
        self.org_level_value_xpath = (By.XPATH, "(//input[@data-bind='value: name'])[last()]")
        self.save_btn_xpath = (By.XPATH, "//button[@type='submit' and @class='btn btn-default pull-right btn-primary']")
        self.save_btn_delete = (By.XPATH, "//button[@class='btn btn-default pull-right']")
        self.download_loc_btn = (By.LINK_TEXT, "Download Organization Structure")
        self.upload_loc_btn = (By.LINK_TEXT, "Bulk Upload")
        self.upload = (By.XPATH, "//button[@class='btn btn-primary disable-on-submit']")
        self.import_complete = (By.XPATH, "//legend[text()='Import complete.']")
        self.download_filter = (By.XPATH, "//button[@data-bind='html: buttonHTML']")
        self.bulk_upload_id = (By.ID, "id_bulk_upload_file")
        self.test_locations = (By.XPATH, "//span[@class='loc_name']")
        self.test_location = (By.XPATH, "(//span[contains(text(),'Test Location [DO NOT DELETE!!!')])[1]")
        self.archive_buttton = (By.XPATH,
                                "//div[.//span[.='Test Location [DO NOT DELETE!!!]']]/preceding-sibling::div/button[normalize-space()= 'Archive']")
        self.archive_button_popup = (By.XPATH, "//button[@data-bind='click: archive_fn']")
        self.archive_success_message = (By.XPATH, "//span[@data-bind='html: message']")
        self.show_arhcived_locations_button = (By.XPATH, "//a[@class='btn btn-default pull-right'][contains(.,'Archived Locations')]")
        self.show_active_locations = (By.XPATH, "//a[@class='btn btn-default pull-right'][contains(.,'Active Locations')]")
        self.unarchive_button = (By.XPATH,
                                 '''//div[.//span[.='Test Location [DO NOT DELETE!!!]']]/preceding-sibling::div/button[normalize-space()= "Unarchive"]''')

        # cleanup
        self.delete_location_created = (
            By.XPATH, "//span[text ()='" + self.new_location_name + "']//preceding::button[@class='btn btn-danger'][1]")
        self.delete_confirm = (By.XPATH, '//input[@data-bind ="value: signOff, valueUpdate: \'input\'"]')
        self.delete_confirm_button = (
            By.XPATH, "//button[@data-bind ='click: delete_fn, css: {disabled: !(signOff() == count)}']")
        self.delete_loc_field = (By.XPATH, "(//a[@class='btn btn-danger'])[last()]")
        self.delete_org_level = (By.XPATH, "(//button[@class='btn btn-danger'])[last()]")
        self.delete_success = (By.XPATH, "//div[@class='alert fade in message-alert alert-success']")

    def organisation_menu_open(self):
        self.wait_to_click(self.org_menu_link_text)
        print(self.driver.title)
        assert "Organization Structure : Locations :: - CommCare HQ" in self.driver.title

    def create_location(self):
        self.wait_to_click(self.add_loc_btn_xpath)
        self.wait_to_clear_and_send_keys(self.loc_name_xpath, self.new_location_name)
        self.click(self.create_loc_xpath)
        assert self.is_present_and_displayed(self.loc_saved_success_msg), "Location not created!"
        self.wait_to_click(self.org_menu_link_text)
        self.driver.refresh()
        try:
            assert self.is_present_and_displayed(self.location_created_xpath), "Location not created!"
        except StaleElementReferenceException:
            assert self.is_present_and_displayed(self.location_created_xpath), "Location not created!"

    def edit_location(self):
        try:
            self.wait_to_click(self.org_menu_link_text)
            self.click(self.edit_loc_button_xpath)
            self.wait_to_clear_and_send_keys(self.loc_name_input_id, "updated_on:" + str(date.today()))
            self.click(self.update_loc_xpath)
            time.sleep(2)
            assert self.is_visible_and_displayed(self.loc_saved_success_msg), "Location editing not successful!"
            self.click(self.org_menu_link_text)
            self.driver.refresh()
            assert self.is_visible_and_displayed(self.renamed_location), "Location editing not successful!"
        except StaleElementReferenceException:
            print(StaleElementReferenceException)

    def edit_location_fields(self):
        self.click(self.org_menu_link_text)
        self.wait_to_click(self.edit_loc_field_btn_xpath)
        self.wait_to_click(self.add_field_btn_xpath)
        self.wait_to_clear_and_send_keys(self.loc_property_xpath, self.loc_field_name)
        self.wait_to_clear_and_send_keys(self.loc_label_xpath, self.loc_field_name)
        if self.is_present(self.choices_button_xpath):
            self.wait_to_click(self.choices_button_xpath)
        self.click(self.add_choice_btn_xpath)
        self.wait_to_clear_and_send_keys(self.choice_xpath, self.loc_field_name)
        self.click(self.save_btn_id)
        assert self.is_displayed(self.success_msg_xpath), "Location field edit not successful!"
        self.driver.refresh()

    def selection_location_field_for_location_created(self):
        try:
            self.click(self.org_menu_link_text)
            self.wait_to_click(self.edit_loc_button_xpath)
            self.wait_to_click(self.additional_info_drop_down)
            self.click(self.select_value_drop_down)
            self.click(self.update_loc_xpath)
            assert self.is_present_and_displayed(self.success_msg_xpath), "Location field not assigned!"
        except StaleElementReferenceException:
            print(StaleElementReferenceException)

    def create_org_level(self):
        self.click(self.org_level_menu_link_text)
        self.wait_to_click(self.new_org_level_btn_xpath)
        self.wait_to_clear_and_send_keys(self.org_level_value_xpath, self.loc_level_name)
        self.wait_to_click(self.save_btn_xpath)

    def download_locations(self):
        self.click(self.org_menu_link_text)
        self.click(self.download_loc_btn)
        self.wait_to_click(self.download_filter)
        try:
            self.wait_and_sleep_to_click(self.download_loc_btn)
            time.sleep(5)
        except TimeoutException:
            print("Still preparing for download..")
            assert False
        # verify_downloaded_location
        newest_file = latest_download_file()
        self.assert_downloaded_file(newest_file, "_locations"), "Download not completed!"
        print("File download successful")

    def upload_locations(self):
        self.click(self.org_menu_link_text)
        self.click(self.upload_loc_btn)
        newest_file = latest_download_file()
        file_that_was_downloaded = PathSettings.DOWNLOAD_PATH / newest_file
        self.send_keys(self.bulk_upload_id, str(file_that_was_downloaded))
        time.sleep(2)
        self.wait_to_click(self.upload)
        self.is_present_and_displayed(self.import_complete), "Upload not completed!"
        print("File uploaded successfully")

    def cleanup_location(self):
        # Delete User Field
        self.wait_to_click(self.org_menu_link_text)
        self.wait_to_click(self.edit_loc_field_btn_xpath)
        self.wait_to_click(self.delete_loc_field)
        self.wait_to_click(self.delete_org_level)
        self.wait_to_click(self.save_btn_id)
        print("Location field deleted successfully")
        self.delete_test_location()
        self.delete_test_org_level()

    def delete_test_org_level(self):
        # # Delete Org Level
        self.js_click(self.org_level_menu_link_text)
        time.sleep(3)
        list_org_level = self.driver.find_elements(By.XPATH, "//input[@class='loctype_name form-control']")
        print(len(list_org_level))
        if len(list_org_level) > 0:
            for i in range(len(list_org_level))[::-1]:
                text = list_org_level[i].get_attribute("value")
                print(text)
                if "loc_level_" in text:
                    self.driver.find_element(By.XPATH,
                                             "(//td[.//input[@class='loctype_name form-control']]/following-sibling::td//button[@class='btn btn-danger'])[" + str(
                                                 i + 1) + "]").click()
                    self.wait_to_click(self.save_btn_delete)
                    self.driver.refresh()
                    time.sleep(3)
                    list_org_level = self.driver.find_elements(By.XPATH, "//input[@class='loctype_name form-control']")
                else:
                    print("Not a text location")
        else:
            print("No location present")
        print("Org level deleted successfully")

    def delete_test_location(self):
        # Delete Location
        self.wait_to_click(self.org_menu_link_text)
        time.sleep(2)
        list_location = self.driver.find_elements(By.XPATH, "//span[@class='loc_name' and contains(.,'location_')]")
        print(list_location)
        print(len(list_location))
        if len(list_location) > 0:
            for i in range(len(list_location))[::-1]:
                text = list_location[i].text
                print(text)
                time.sleep(2)
                self.driver.find_element(By.XPATH,
                                         "(//div[./span[@class='loc_name' and contains(.,'location_')]]//preceding-sibling::div/button[@class='btn btn-danger'])[" + str(
                                             i + 1) + "]").click()
                self.wait_to_clear_and_send_keys(self.delete_confirm, "1")
                self.click(self.delete_confirm_button)
                assert self.is_present_and_displayed(self.delete_success), "Location Not Deleted!"
                print("Location deleted successfully")
                self.driver.refresh()
                time.sleep(3)
                list_location = self.driver.find_elements(By.XPATH,
                                                          "//span[@class='loc_name' and contains(.,'location_')]")
        else:
            print("No test locations present")

    def archive_location(self):
        self.wait_to_click(self.org_menu_link_text)
        active_loc = self.is_present_and_displayed(self.test_location, 10)
        if not active_loc:
            self.wait_to_click(self.show_arhcived_locations_button)
            self.wait_to_click(self.unarchive_button)
            self.assert_archived_location()
        else:
            self.assert_archived_location()

    def assert_archived_location(self):
        self.wait_to_click(self.org_menu_link_text)
        time.sleep(5)
        self.wait_for_element(self.test_location, 40)
        # self.is_present_and_displayed(self.test_location, 10)
        active_loc = self.find_elements(self.test_locations)
        loc_list = []
        print(active_loc)
        if len(active_loc) > 0:
            for i in range(len(active_loc)):
                print(active_loc[i].text)
                loc_list.append(active_loc[i].text)
        print("Active: ", loc_list)
        assert "Test Location [DO NOT DELETE!!!]" in loc_list, "Location not Unarchived successfully"
        # active_loc = self.get_text(self.test_location)
        self.wait_to_click(self.archive_buttton)
        self.wait_to_click(self.archive_button_popup)
        self.is_present_and_displayed(self.archive_success_message, 10)
        self.driver.refresh()
        check_archived_loc = self.is_present_and_displayed(self.test_location, 10)
        assert not check_archived_loc, "Location is still Active"
        self.wait_to_click(self.show_arhcived_locations_button)
        time.sleep(5)
        archived_loc = self.find_elements(self.test_locations)
        archive_list = []
        print(archived_loc)
        if len(archived_loc) > 0:
            for i in range(len(archived_loc)):
                print(archived_loc[i].text)
                archive_list.append(archived_loc[i].text)
        print("Archived: ", archive_list)
        assert "Test Location [DO NOT DELETE!!!]" in archive_list, "Location is not Archived"

    def unarchive_location(self, settings):
        self.wait_for_element(self.test_location, 40)
        archived_loc = self.is_present_and_displayed(self.test_location, 10)
        if not archived_loc:
            self.wait_to_click(self.show_active_locations)
            self.wait_to_click(self.archive_buttton)
            self.wait_to_click(self.archive_button_popup)
            self.assert_unarchived_location(settings)
        else:
            self.assert_unarchived_location(settings)

    def assert_unarchived_location(self, settings):
        if self.is_present(self.show_arhcived_locations_button):
            self.wait_to_click(self.show_arhcived_locations_button)
            time.sleep(5)
        archived_loc = self.get_text(self.test_location)
        self.wait_to_click(self.unarchive_button)
        self.driver.refresh()
        time.sleep(3)
        check_unarchived_loc = self.is_present_and_displayed(self.test_location, 10)
        assert not check_unarchived_loc, "Location is still Unarchived"
        self.wait_to_click(self.show_active_locations)
        home = HomePage(self.driver, settings)
        home.users_menu()
        self.wait_to_click(self.org_menu_link_text)
        time.sleep(5)
        unarchived_loc = self.find_elements(self.test_locations)
        loc_list = []
        print(unarchived_loc)
        if len(unarchived_loc) > 0:
            for i in range(len(unarchived_loc)):
                print(unarchived_loc[i].text)
                loc_list.append(unarchived_loc[i].text)
        print("unarchived: ",loc_list)
        assert "Test Location [DO NOT DELETE!!!]" in loc_list, "Location not Unarchived successfully"

