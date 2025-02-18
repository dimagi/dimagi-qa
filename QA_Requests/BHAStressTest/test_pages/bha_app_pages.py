import csv
from datetime import datetime
import os
import time

from selenium.webdriver.common.by import By

from QA_Requests.BHAStressTest.user_inputs.bha_user_inputs import BhaUserInput
from common_utilities.generate_random_string import fetch_random_string
from common_utilities.selenium.base_page import BasePage
from Features.CaseSearch.constants import *

""""Contains test page elements and functions related to the CO BHA App"""


# filename = os.path.abspath(
#                 os.path.join(UserData.USER_INPUT_BASE_DIR,
#                              "test_data/import_to_parent_" + UserData.parent_2_id + ".xlsx"
#                              )
#                 )

class BhaWorkflows(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

        self.textarea_value = "Test " + fetch_random_string()
        self.app_name_format = "//div[@aria-label='{}']/div/h3"
        self.app_header_format = "//h1[contains(text(),'{}')]"
        self.menu_name_format = '//*[contains(@aria-label,"{}")]'
        self.menu_name_header_format = "//h1[@class='page-title' and contains(text(),'{}')]"
        self.form_name_format = "//h3[contains(text(), '{}')]"
        self.form_name_header_format = "//h1[contains(text(), '{}')]"
        self.current_page = "//a[@aria-current='page' and contains(.,'{}')]"
        self.setting_button = (By.XPATH, "//h3[contains(@id,'setting')]")
        self.sync_button = (By.XPATH, "//button[contains(@class,'sync')]")
        self.done_button = (By.XPATH, "//button[contains(@class,'done')]")
        self.webapps_home = (By.XPATH, "//i[@class='fcc fcc-flower']")
        self.form_submit = (By.XPATH, "//div[contains(@id,'submit')]//button[contains(@class,'submit')]")
        self.form_submission_successful = (By.XPATH,
                                           "//div[contains(@class,'alert-success')][contains(text(), 'successfully saved') or .//p[contains(text(), 'successfully saved')]]")

        self.breadcrumb_format = "//li[contains(@class,'breadcrumb')][contains(text(),'{}') or ./a[contains(.,'{}')]]"
        self.form_textarea = "//label[contains(.,'{}')]//following-sibling::div//textarea"
        self.form_file_input = "//label[contains(.,'Upload the {}th Image') or contains(.,'Upload the {}st Image') or contains(.,'Upload the {}nd Image') or contains(.,'Upload the {}rd Image')]//following-sibling::div//input"

        self.admit_new_client_on_caselist = (By.XPATH, "//button[text()='Admit New Client']")
        self.radio_option_value = "//input[contains(@value,'{}')]"
        self.case_search_properties = (By.XPATH, "//label[contains(@class,'label')]")
        self.continue_button = "//span[@id='multi-select-btn-text' and text()='{}']"
        self.client_info = " (//h2[contains(text(), 'Client Information')]/following::strong[contains(text(),'{}')]//ancestor::li[1])[1]"
        self.combobox_select_clinic = (By.XPATH, "//select[contains(@class,'select2-hidden-accessible')]")
        self.answer_option_label = "//p[text()='{}']"
        self.question_label = "//span[text()='{}']"
        self.clinic_close_button = "//button[@aria-label='Remove item' and contains(@aria-describedby , '{}')]"
        self.case_list_display_properties = "(//tr[.//th[contains(text(),'{}')]])[1]"
        self.case_prop_value = "//th[@title='{}']/following::td[contains(text(),'{}')]"
        self.value_in_outputs = "//div[@class='list-grid-style-{} box']//strong"

        # Messages
        self.view_latest_details_by_type = "(//a[contains(text(),'{}')]/following::a[text()='View Details'])[1]"
        self.content = "//*[contains(@title,'{}')]/parent::*"

    def open_app(self, app_name):
        time.sleep(2)
        if self.is_present_and_displayed(self.webapps_home, 20):
            self.js_click(self.webapps_home)
        self.application = self.get_element(self.app_name_format, app_name)
        self.application_header = self.get_element(self.app_header_format, app_name)
        self.scroll_to_element(self.application)
        self.js_click(self.application)
        time.sleep(10)
        self.wait_for_element(self.application_header, timeout=200)

    def open_menu(self, menu_name):
        self.caselist_menu = self.get_element(self.menu_name_format, menu_name)
        self.caselist_header = self.get_element(self.menu_name_header_format, menu_name)
        self.scroll_to_element(self.caselist_menu)
        self.js_click(self.caselist_menu)
        time.sleep(5)
        self.wait_for_element((By.XPATH, self.current_page.format(menu_name)), timeout=60)
        assert self.is_visible_and_displayed(self.caselist_header)

    def open_form(self, form_name):
        self.form_header = self.get_element(self.form_name_header_format, form_name)
        if self.is_displayed(self.form_header):
            print("Auto advance enabled")
        else:
            self.form_name = self.get_element(self.form_name_format, form_name)
            self.wait_for_element(self.form_name, timeout=50)
            self.scroll_to_element(self.form_name)
            self.js_click(self.form_name)
            time.sleep(5)
            self.wait_for_element((By.XPATH, self.current_page.format(form_name)), timeout=50)

    def stress_load_files(self, app, menu, form):
        for i in range(0, 40):
            print("Running loop for file count: ", str(i + 1))
            self.wait_to_click(self.webapps_home)
            self.open_app(app)
            self.open_menu(menu)
            self.open_form(form)
            time_value = self.enter_form_value((i + 1))
            self.write_to_file(str(i + 1), str(time_value))

    def enter_form_value(self, count):
        self.wait_for_element((By.XPATH, self.form_textarea.format(BhaUserInput.textarea_label)))
        self.send_keys((By.XPATH, self.form_textarea.format(BhaUserInput.textarea_label)), self.textarea_value+" "+str(count))
        filename = os.path.abspath(os.path.join(BhaUserInput.USER_INPUT_BASE_DIR,
                                                "test_data/stress_test_file.pdf"
                                                )
                                   )
        for i in range(0, count):
            self.scroll_to_element((By.XPATH, self.form_file_input.format(str(i+1), str(i+1), str(i+1), str(i+1))))
            self.send_keys((By.XPATH, self.form_file_input.format(str(i+1), str(i+1), str(i+1), str(i+1))),
                           filename
                           )
        self.scroll_to_element(self.form_submit)
        start_time = datetime.now()
        self.js_click(self.form_submit)
        self.wait_for_element(self.form_submission_successful, 600)
        end_time = datetime.now()
        total_time = (end_time - start_time).total_seconds()
        return total_time

    def write_to_file(self, file_count, time_value):
        text = "Files uploaded " + file_count
        data = [text, time_value]
        print(data)
        filename = os.path.abspath(os.path.join(BhaUserInput.USER_INPUT_BASE_DIR,
                                                "time_records_new.csv"
                                                )
                                   )
        with open(filename, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(data)
        csvfile.close()

    def create_csv_file(self):
        filename = os.path.abspath(os.path.join(BhaUserInput.USER_INPUT_BASE_DIR,
                                                "time_records_new.csv"
                                                )
                                   )
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['file_count', 'time_taken']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
        csvfile.close()
