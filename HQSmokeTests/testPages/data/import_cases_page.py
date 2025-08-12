import os
import time

from openpyxl import load_workbook
from selenium.webdriver.common.by import By

from common_utilities.selenium.base_page import BasePage
from common_utilities.generate_random_string import fetch_random_string
from HQSmokeTests.userInputs.user_inputs import UserData

""""Contains test page elements and functions related to the Import Cases from Excel module"""


class ImportCasesPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.file_new_name = "reassign_cases_" + str(fetch_random_string()) + ".xlsx"
        self.sheet_name = "reassign_cases_" + str(fetch_random_string())

        self.village_name_cell = "C2"
        self.to_be_edited_file = os.path.abspath(os.path.join(UserData.USER_INPUT_BASE_DIR, "test_data/reassign_cases.xlsx"))
        self.renamed_file = os.path.abspath(os.path.join(UserData.USER_INPUT_BASE_DIR, "test_data/" + self.file_new_name))

        self.import_cases_menu = (By.LINK_TEXT, "Import Cases from Excel")
        self.download_file = (By.XPATH, "(//span[@data-bind='text: upload_file_name'])[1]")
        self.choose_file = (By.ID, "file")
        self.next_step = (By.XPATH, "(//button[@type='submit'])[1]")
        self.confirm_import = (By.XPATH, "//button[@type='submit'][contains(.,'Confirm Import')]/i")
        self.case_type = (By.XPATH, "//select[@id='case_type']")
        self.case_type_option_value = (By.XPATH, "//option[@value='pregnancy']")
        self.success = "(//span[text()='{}']//preceding::span[contains(@class,'success')])[1]"
        self.create_new_cases = (By.XPATH, "//input[@id='create_new_cases']")
        self.alert_msg = (By.XPATH, "//div[contains(@class,'alert alert-dismissible')]")
        self.value_hints = "//ul[contains(@data-bind,'valuesHints')]/li[.='{}']"
        self.invalid_value_warning = "//tr[2]//div[contains(@class,'alert-warning')]/h6[contains(.,'row had an invalid') or contains(.,'rows had invalid')][.//span[contains(@data-bind,'column') and text()='{}']]"
        self.success_with_warnings = (By.XPATH, "//tr[2]//td[./span[contains(.,'Success with warnings')]]")

    def replace_property_and_upload(self, casetype, filename=None, flag=None, column_list=None, list_warning = None):
        self.wait_to_click(self.import_cases_menu)
        time.sleep(2)
        if filename is None:
            self.edit_spreadsheet(self.to_be_edited_file, self.village_name_cell, self.renamed_file, self.sheet_name)
            print(str(self.renamed_file))
            filename = self.renamed_file
        self.wait_for_element(self.choose_file)
        self.send_keys(self.choose_file, filename)
        self.wait_for_element(self.next_step)
        if self.is_present(self.alert_msg):
            print("Upload might have failed. Reuploading...")
            self.reload_page()
            self.wait_for_element(self.choose_file)
            self.send_keys(self.choose_file, filename)
            self.wait_for_element(self.next_step)
        else:
            print("Upload successful.")
        self.click(self.next_step)
        self.is_visible_and_displayed(self.case_type)
        self.select_by_text(self.case_type, casetype)
        self.wait_for_element(self.create_new_cases)
        self.scroll_to_element(self.create_new_cases)
        self.wait_to_click(self.create_new_cases)
        time.sleep(2)
        self.wait_for_element(self.next_step)
        self.wait_to_click(self.next_step)
        time.sleep(2)
        if self.is_present_and_displayed(self.alert_msg, 20):
            print("Error message displayed on importing excel. Repeating process..")
            self.reload_page()
            self.wait_for_element(self.choose_file)
            self.send_keys(self.choose_file, filename)
            self.wait_for_element(self.next_step)
            self.click(self.next_step)
            self.is_visible_and_displayed(self.case_type)
            self.select_by_text(self.case_type, casetype)
            self.wait_for_element(self.create_new_cases)
            self.scroll_to_element(self.create_new_cases)
            self.wait_to_click(self.create_new_cases)
            time.sleep(2)
            self.wait_for_element(self.next_step)
            self.wait_to_click(self.next_step)
            time.sleep(2)
        else:
            print("No error present")
        self.wait_for_element(self.confirm_import)
        if column_list is not None:
            for item in column_list:
                assert self.is_present((By.XPATH,self.value_hints.format(item))), f"Hint for {item} is not present"
                print(f"Hint for {item} is present")
        time.sleep(2)
        self.scroll_to_bottom()
        self.scroll_to_element(self.confirm_import)
        self.js_click(self.confirm_import)
        print("Imported case!")
        if flag is None:
            self.wait_for_element((By.XPATH, self.success.format(self.file_new_name)),400)
        else:
            self.validate_data_dictionary_warning(list_warning)

    def edit_spreadsheet(self, edited_file, cell, renamed_file, sheet_name):
        workbook = load_workbook(filename=edited_file)
        sheet = workbook.active
        sheet[cell] = fetch_random_string()
        sheet.title = sheet_name
        workbook.save(filename=renamed_file)

    def import_parent_child_excel(self, filename):
        self.wait_to_click(self.import_cases_menu)
        self.wait_for_element(self.choose_file)
        print("file path: ", filename)
        if "/" in filename:
            text = str(filename).split("/")
            file = text[-1]
        else:
            text = str(filename).split("\\")
            file = text[-1]
        print(file)
        self.wait_to_clear_and_send_keys(self.choose_file, filename)
        self.wait_to_click(self.next_step)
        self.is_visible_and_displayed(self.case_type)
        self.select_by_text(self.case_type, UserData.child_type)
        self.wait_for_element(self.next_step)
        self.wait_to_click(self.next_step)
        self.wait_for_element(self.next_step)
        time.sleep(2)
        self.scroll_to_element(self.confirm_import)
        self.wait_to_click(self.confirm_import)
        print("Imported case!")
        self.wait_for_element((By.XPATH, self.success.format(file)), 100)
        print("Import Completed")

    def validate_data_dictionary_warning(self, list_warning):
        self.wait_for_element(self.success_with_warnings, 400)
        for item in list_warning:
            assert self.is_present_and_displayed((By.XPATH, self.invalid_value_warning.format(item))), f"{item} not present"
            print(f"{item} is present")