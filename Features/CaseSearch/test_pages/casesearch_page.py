import time

from dateutil.relativedelta import relativedelta
from datetime import datetime

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from common_utilities.selenium.base_page import BasePage
from Features.CaseSearch.constants import *

""""Contains test page elements and functions related to the Case Search functionality"""


class CaseSearchWorkflows(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

        self.value_in_table_format = "//td[@class='module-case-list-column'][{}]"
        self.case_name_format = "//tr[.//td[text()='{}']]"
        self.text_search_property_name_and_value_format = "//input[contains (@id, '{}') and @value='{}']"
        self.search_property_name_combobox = "//label[contains(text(),'{}')]"
        self.combobox_search_property_name_and_value_format = self.search_property_name_combobox + "//following::span[contains(text(),'{}')]"
        self.search_against_text_property_format = "//input[contains (@id, '{}')]"
        self.help_text_format = '//label[@for="{}"]//following::a[@data-content="{}"]'
        self.combox_select = "//label[contains(text(), '{}')]//following::select[contains(@class, 'query-field')][1]"
        self.search_for_address = "//*[contains(text(),'{}')]//following::input[contains(@aria-label,'Search')][1]"
        self.include_blanks = self.search_property_name_combobox + "//following::input[contains(@class,'search-for-blank')][1]"
        self.required_validation_on_top = "//div[@class='alert alert-danger']//following::li[contains(text(),'{}')]"
        self.required_validation_per_property_text = self.search_against_text_property_format + "//following::div[contains (text(),'{}')][1]"
        self.required_validation_per_property_combox = self.search_property_name_combobox + "//following::div[contains (text(),'{}')][1]"
        self.city_value_home = "//span[@class='caption webapp-markdown-output'][contains(text(), '{}')]"
        self.city_value_work = "//span[@class='caption webapp-markdown-output'][contains(text()[2], '{}')]"
        self.search_screen_title = "//h2[contains(text(), '{}')]"
        self.date_selected = "(//span[@class='drp-selected' and contains(text(),'{}')])[1]"
        self.dropdown_values = self.combox_select + "/option"
        self.menu_header = "//h1[contains(text(),'{}')]"
        self.menu_breadcrumb = "//li[contains(text(),'{}')]"
        self.webapps_home = (By.XPATH, "//i[@class='fcc fcc-flower']")
        self.case_detail_value = "//th[contains(text(), '{}')]//following-sibling::td[contains(text(), '{}')]"
        self.case_detail_tab = "//a[text()='{}']"
        # Reports
        self.case_type_select = (By.ID, "report_filter_case_type")
        self.report_search = (By.ID, "report_filter_search_query")
        self.report_apply_filters = (By.ID, "apply-filters")
        self.commcare_case_claim_case = "//a[contains(text(), '{}')]//following::*[text()='{}'][1]"

    def check_element_claimed(self, case_name):
        self.case = self.get_element(self.case_name_format, case_name)
        assert self.is_visible_and_displayed(self.case)

    def check_values_on_caselist(self, row_num, expected_value, is_multi=NO):
        self.value_in_table = self.get_element(self.value_in_table_format, row_num)
        values_ = self.find_elements_texts(self.value_in_table)
        # print(value, values_) # added for debugging
        if is_multi == YES:
            assert all(item in values_ for item in expected_value) or any(item in values_ for item in expected_value)
        elif is_multi == NO:
            assert expected_value in values_

    def check_default_values_displayed(self, search_property, default_value, search_format):
        if search_format == text:
            search_property = (
                By.XPATH, self.text_search_property_name_and_value_format.format(search_property, default_value))
        elif search_format == combobox:
            search_property = (
                By.XPATH, self.combobox_search_property_name_and_value_format.format(search_property, default_value))
        assert self.is_visible_and_displayed(search_property)

    def search_against_property(self, search_property, input_value, property_type, include_blanks=None):
        if property_type == TEXT_INPUT:
            self.search_property = self.get_element(self.search_against_text_property_format, search_property)
            self.wait_to_clear_and_send_keys(self.search_property, input_value)
            self.send_keys(self.search_property, Keys.TAB)
        elif property_type == COMBOBOX:
            self.combox_select_element = self.get_element(self.combox_select, search_property)
            self.select_by_text(self.combox_select_element, input_value)
            time.sleep(3)
        if include_blanks == YES:
            self.select_include_blanks(search_property)

    def date_range(self, no_of_days):
        today_date = datetime.today()
        sixty_days_ago = today_date - relativedelta(days=no_of_days)
        date_ranges = str(sixty_days_ago.date()) + " to " + str(today_date.date())
        return date_ranges

    def check_help_text(self, search_property, help_text):
        help_text = (By.XPATH, self.help_text_format.format(search_property, help_text))
        assert self.is_visible_and_displayed(help_text)

    def check_date_range(self, date_range):
        date = self.get_element(self.date_selected, date_range)
        assert self.is_present(date)

    def add_address(self, address, search_property):
        address_search = self.get_element(self.search_for_address, search_property)
        self.send_keys(address_search, address)
        time.sleep(5)
        self.send_keys(address_search, Keys.TAB)
        time.sleep(10)

    def check_value_on_form(self, city_address, type=HOME):
        if type == HOME:
            city_home = self.get_element(self.city_value_home, city_address)
            assert self.is_present(city_home)
        if type == WORK:
            city_work = self.get_element(self.city_value_work, city_address)
            assert self.is_present(city_work)

    def check_search_screen_title(self, title):
        title_on_screen = self.get_element(self.search_screen_title, title)
        assert self.is_displayed(title_on_screen)

    def assert_address_is_hidden(self, hidden_property):
        hidden = self.get_element(self.search_property_name_combobox, hidden_property)
        assert not self.is_displayed(hidden)

    def select_include_blanks(self, search_property):
        checkbox = self.get_element(self.include_blanks, search_property)
        time.sleep(2)
        self.js_click(checkbox)

    def check_validations_on_property(self, search_property, property_type, message=None, required_or_validated=YES):
        validation_message_on_top = self.get_element(self.required_validation_on_top, search_property)
        validation_message_per_prop = None
        if property_type == TEXT_INPUT:
            validation_message_per_prop = (
                By.XPATH, self.required_validation_per_property_text.format(search_property, message))
        elif property_type == COMBOBOX:
            validation_message_per_prop = (
                By.XPATH, self.required_validation_per_property_combox.format(search_property, message))
        if required_or_validated == YES:
            time.sleep(5)
            assert self.is_displayed(validation_message_on_top)
            assert self.is_displayed(validation_message_per_prop)
        elif required_or_validated == NO:
            time.sleep(5)
            assert not self.is_displayed(validation_message_on_top)
            assert not self.is_displayed(validation_message_per_prop)

    def check_dropdown_value(self, search_property, not_to_be_present):
        dropdown_values_ = self.get_element(self.dropdown_values, search_property)
        values = self.find_elements_texts(dropdown_values_)
        assert not_to_be_present not in values

    def check_eof_navigation(self, eof_nav, menu=None):
        if eof_nav == PREV_MENU:
            header = self.get_element(self.menu_header, menu)
            assert self.is_displayed(header)
        elif eof_nav == MENU or FIRST_MENU:
            header = self.get_element(self.menu_breadcrumb, menu)
            assert self.is_displayed(header)
        elif eof_nav == HOME_SCREEN:
            assert self.is_displayed(self.webapps_home)

    def select_case_detail_tab(self, tabname):
        tab = (By.XPATH, self.case_detail_tab.format(tabname))
        self.wait_to_click(tab)

    def check_value_on_case_detail(self, search_property, expected_value, tabname=None):
        self.select_case_detail_tab(tabname)
        value = (By.XPATH, self.case_detail_value.format(search_property, expected_value))
        assert self.is_visible_and_displayed(value)

    def check_case_claim_case_type(self, claimed_case_name, claimed_user):
        self.select_by_text(self.case_type_select, "commcare-case-claim")
        self.wait_to_clear_and_send_keys(self.report_search, claimed_case_name)
        self.wait_to_click(self.report_apply_filters)
        claim_case_type = (By.XPATH, self.commcare_case_claim_case.format(claimed_case_name, claimed_user))
        assert self.is_visible_and_displayed(claim_case_type)
