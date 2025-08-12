import time

from selenium.webdriver.common.by import By
from common_utilities.selenium.base_page import BasePage
from Features.CaseSearch.constants import *

""""Contains test page elements and functions related to the CO BHA App"""


class BhaWorkflows(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

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

    def click_on_admit_new_client(self):
        self.wait_for_element(self.admit_new_client_on_caselist)
        self.wait_to_click(self.admit_new_client_on_caselist)

    def replace_one_char(self, original_string):
        index = 2
        new_character = "a"
        return original_string[:index] + new_character + original_string[index + 1:]

    def select_radio(self, value):
        time.sleep(4)
        radio_value = self.get_element(self.radio_option_value, value)
        if self.is_present_and_displayed(radio_value, 10):
            self.scroll_to_element(radio_value)
            self.wait_to_click(radio_value)
            time.sleep(4)
        else:
            print("Yes button is not present")

    def check_search_properties_present(self, properties):
        properties_labels = self.find_elements_texts(self.case_search_properties)
        for search_property in properties:
            assert search_property in properties_labels, "Property should be present"
            print("Property "+str(search_property)+" present in "+str(properties_labels))

    def expected_count_on_continue_button(self, number):
        count_on_continue = self.get_element(self.continue_button, number)
        assert self.is_displayed(count_on_continue), "Continue count not displayed"
        print("Continue count is displayed")

    def check_client_info_on_form(self, search_property, search_value):
        value_on_form_xpath = self.get_element(self.client_info, search_property)
        value_on_form = self.get_text(value_on_form_xpath)
        assert search_value in value_on_form,  "Value "+search_value+" is not present in "+value_on_form
        print("Value "+search_value+" is present in "+value_on_form)

    def select_clinic(self, clinic_name):
        time.sleep(4)
        if self.is_displayed(self.combobox_select_clinic):
            self.scroll_to_element(self.combobox_select_clinic)
            self.select_by_text(self.combobox_select_clinic, clinic_name)
        time.sleep(4)

    def remove_clinic(self, clinic_name):
        close_xpath = self.get_element(self.clinic_close_button, clinic_name)
        self.wait_to_click(close_xpath)
        time.sleep(4)

    def check_answer_options(self, label, displayed=None):
        answer_label = self.get_element(self.answer_option_label, label)
        if displayed == YES:
            assert self.is_displayed(answer_label), "Label "+label+" should be displayed"
            print("Label "+label+" is displayed")
        elif displayed == NO:
            assert not self.is_displayed(answer_label), "Label "+label+" should not be displayed"
            print("Label "+label+" is not displayed")

    def check_question_label(self, label, displayed=None):
        question_label = self.get_element(self.question_label, label)
        if displayed == YES:
            assert self.is_displayed(question_label), "Label "+label+" should be displayed"
            print("Label "+label+" is displayed")
        elif displayed == NO:
            assert not self.is_displayed(question_label), "Label "+label+" should not be displayed"
            print("Label "+label+" is not displayed")

    def check_headers_on_case_list(self, display_properties):
        for prop in display_properties:
            header = self.get_element(self.case_list_display_properties, prop)
            assert self.is_displayed(header), f"Navigated to {header}"
            print(f"Not Navigated to {header}")

    def check_property_on_case_list_report(self, case_link, case_property, case_property_value):
        self.driver.get(case_link)
        self.locator = (By.XPATH, self.case_prop_value.format(case_property, case_property_value))
        assert self.is_present(self.locator), f"Property {case_property_value} not present"
        print(f"Property {case_property_value} is present")

    def view_message_details(self, alert_type):
        self.wait_to_click(self.get_element(self.view_latest_details_by_type, alert_type))

    def check_if_alert_triggered(self, content, date):
        date_locator = self.get_element(self.content, date)
        content_locator = self.get_element(self.content, content)
        print(date_locator, " ", content_locator)
        assert self.is_present(content_locator), f"Content {content} not present"
        print(f"Content {content} is present")
        assert self.is_present(date_locator), f"Date {date} not present"
        print(f"Date {date} is present")
        self.switch_back_to_prev_tab()

    def check_values_on_caselist(self, row_num, expected_value, is_multi=NO):
        self.value_in_table = self.get_element(self.value_in_outputs, row_num)
        self.wait_for_element(self.value_in_table)
        values_ = self.find_elements_texts(self.value_in_table)
        print(expected_value, values_)  # added for debugging
        if is_multi == YES:
            assert all(item in values_ for item in expected_value) or any(item in values_ for item in expected_value), "Expected values are not present"
            print("Expected values are present")
        elif is_multi == NO:
            assert expected_value in values_, "Expected values are not present"
            print("Expected values are present")
