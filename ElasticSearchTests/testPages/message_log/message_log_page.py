import html
import os
import time

import dateutil.relativedelta
import pandas as pd

from datetime import datetime, timedelta, date
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from natsort import natsorted
from selenium.webdriver import ActionChains

from HQSmokeTests.testPages.data.export_data_page import latest_download_file
from common_utilities.path_settings import PathSettings

from common_utilities.selenium.base_page import BasePage
from common_utilities.generate_random_string import fetch_random_string
from ElasticSearchTests.userInputs.user_inputs import UserData

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

""""Contains test page elements and functions related to the Reports module"""


class MessageLogPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

        # Mobile Worker Reports
        self.reports_menu_id = (By.ID, "ProjectReportsTab")
        self.message_log_rep = (By.LINK_TEXT, "Message Log")
        self.message_log_TITLE = "Message Log - CommCare HQ"

        # Report Elements
        self.apply_id = (By.ID, "apply-filters")
        self.report_content_id = (By.ID, "report-content")
        self.homepage = (By.XPATH, ".//a[@href='/homepage/']")
        self.date_range_error = (By.XPATH, "//td[contains(.,'You are limited to a span of 90 days,')]")
        self.report_loading = (By.XPATH, "//div[@id='report_table_message_log_processing'][@style='display: block;']")
        self.report_loading_done = (
        By.XPATH, "//div[@id='report_table_message_log_processing'][@style='display: none;']")

        self.form_activity_results = (By.XPATH, "//table[@id='report_table_message_log']/tbody/tr")
        self.form_activity_results_cells = (By.XPATH, "//table[@id='report_table_message_log']/tbody/tr/td")
        self.message_type_field = (By.XPATH, "//span[contains(@class, 'container')]")
        self.message_type_input = (By.XPATH, "(//textarea[@class='select2-search__field'])[1]")
        self.no_results = (By.XPATH, "//li[.='No results found']")
        self.message_type_dropdown = (By.XPATH, "//select[contains(@class,'report-filter-multi-option')]")
        self.location_filter_dropdown = (By.XPATH, "//select[contains(@data-bind,'show_location_filter')]")
        self.location_dropdown = (By.XPATH, "//select[contains(@data-bind,'value: selected_child')]")
        self.location_filter_section = (By.XPATH, "//div[@data-bind='visible: show_location_filter_bool()'][not(@style='display: none;')]")
        self.second_location_dropdown = (By.XPATH, "//label[./text()='Location']//following-sibling::div//select[2]")

        self.remove_buttons = (By.XPATH, "//ul//button")
        self.custome_remove_button = "//span[contains(.,'{}')]//preceding-sibling::button[@class='select2-selection__choice__remove']"
        self.user_remove_btn = (By.XPATH, "(//button[@class='select2-selection__choice__remove'])[last()]")
        self.user_from_list = "//li[contains(.,'{}')]"
        self.export_to_excel = (By.XPATH, "//a[@id='export-report-excel']")
        self.export_success = (By.XPATH,
                               "//span[.='Your requested Excel report will be sent to the email address defined in your account settings.']")
        self.user_column = (
        By.XPATH, "(//thead/tr/th[@aria-controls='report_table_message_log']/div[contains(.,'Username')])[1]")
        self.group_column = (
        By.XPATH, "(//thead/tr/th[@aria-controls='report_table_message_log']/div[contains(.,'Group')])[1]")
        self.total_column = (By.XPATH, "(//thead/tr/th[@aria-controls='report_table_message_log']/div[contains(.,'Total')])[1]")
        self.users_list_item = "//ul[@role='listbox']/li[contains(.,'{}')]"
        self.users_list = (By.XPATH, "//ul[contains(@class,'select2-results__options')]/li")
        self.users_list_empty = (
        By.XPATH, "//ul[contains(@id,'select2-emw-bi-results')]/li[.='The results could not be loaded.']")

        self.date_input = (By.XPATH, "//input[@id='filter_range']")
        self.cancel_date = (
        By.XPATH, "//div[contains(@class,'show-calendar')]//div[@class='drp-buttons']//button[.='Cancel']")
        self.apply_date = (
            By.XPATH, "//div[contains(@class,'show-calendar')]//div[@class='drp-buttons']//button[.='Apply']")
        self.date_range_label = (By.XPATH, "//div[./input[@id='filter_range']]//following-sibling::div/*[contains(.,\"This report's timezone is\")]")
        self.date_range_type = "//li[@data-range-key='{}']"
        self.column_names = "(//thead/tr/th[@aria-controls='report_table_message_log']/div[@data-title='{}'])[1]"
        self.column_group_names = (By.XPATH, "(//thead)[1]/tr/th/div")
        self.user_names_column_list = (By.XPATH, "//table[@id='report_table_message_log']//tbody//td[1]")
        self.last_submission_column_list = (By.XPATH, "//table[@id='report_table_message_log']//tbody//td[4]")
        self.result_table = (By.XPATH, "(//div[@id='report-content']//table//tbody//td[not(contains(@class,'dataTables_empty'))])[1]")
        self.results_rows = (By.XPATH, "//tbody/tr/td[4]")
        self.result_rows_names = "//tbody/tr/td[2][contains(.,'{}')]"
        self.hide_filters_options = (By.XPATH, "//a[.='Hide Filter Options']")
        self.show_filters_options = (By.XPATH, "//a[.='Show Filter Options']")
        self.user_sort = "(//text()[contains(.,'{}')][not(contains(.,'View Form'))]//preceding-sibling::i[@class='icon-white fa dt-sort-icon'])[1]"
        self.sorting_value = "(//th[contains(.,'{}')][@aria-controls='report_table_message_log'])[1]"
        self.active_cases_column_list = (By.XPATH, "//table[@id='report_table_message_log']//tbody//td[7]")
        self.total_cases_shared_column_list = (By.XPATH, "//table[@id='report_table_message_log']//tbody//td[8]")
        self.column_name_headers = "//table[@id='report_table_message_log']//thead//th/div/div[contains(.,'{}')]"

        # columns
        self.timestamp_column_list = (By.XPATH, "//table[@id='report_table_message_log']//tbody//td[1]")
        self.user_names_column_list = (By.XPATH, "//table[@id='report_table_message_log']//tbody//td[2]")
        self.user_names_column_first = (
            By.XPATH, "(//table[@id='report_table_message_log']//tbody//td[2])[1]")
        self.phone_number_column_list = (By.XPATH, "//table[@id='report_table_message_log']//tbody//td[3]")
        self.direction_column_list = (By.XPATH, "//table[@id='report_table_message_log']//tbody//td[4]")
        self.message_column_list = (By.XPATH, "//table[@id='report_table_message_log']//tbody//td[5]")
        self.status_column_list = (By.XPATH, "//table[@id='report_table_message_log']//tbody//td[6]")
        self.event_column_list = (By.XPATH, "//table[@id='report_table_message_log']//tbody//td[7]")
        self.type_column_list = (By.XPATH, "//table[@id='report_table_message_log']//tbody//td[8]")

        # View Form Page
        self.view_form_tabs = "//li/a[contains(.,'{}')]"
        self.form_data_table = (By.XPATH, "//table[contains(@class,'form-data-table')]")
        self.archive_this_form = (By.XPATH, "//button[contains(.,'Archive this form')]")
        self.restore_this_form = (By.XPATH, "//button[contains(.,'Restore this form')]")
        self.delete_this_form = (By.XPATH, "//button[contains(.,'Delete this form')]")
        self.delete_confirm_button = (By.XPATH, "//div[@class='modal-footer']/*[contains(@class,'btn btn-danger')]")
        self.delete_case_confirm = (By.XPATH, "//*[@data-target='#delete_case_confirmation']")
        self.case_text = (By.XPATH, "//p[contains(.,'delete this form, type')]/strong")
        self.textarea_delete_popup = (By.XPATH, "//p[contains(.,'delete this form, type')][./strong]//following-sibling::textarea")
        self.archive_success_msg = (By.XPATH, "//div[contains(@class,'alert-margin-top')][contains(.,'Form was successfully archived')]")
        self.restore_success_msg = (
        By.XPATH, "//div[contains(@class,'alert-margin-top')][contains(.,'Form was successfully restored')]")


        # Pagination
        self.page_list_dropdown = (By.XPATH, "//select[@name='report_table_message_log_length']")
        self.table_info = (By.XPATH, "//div[@id='report_table_message_log_info']")
        self.prev_page_button = (By.XPATH, "//ul[@class='pagination']/li[@class='prev']/a")
        self.next_page_button = (By.XPATH, "//ul[@class='pagination']/li[@class='next']/a")
        self.prev_page_button_disabled = (By.XPATH, "//ul[@class='pagination']/li[@class='prev disabled']/a")
        self.next_page_button_disabled = (By.XPATH, "//ul[@class='pagination']/li[@class='next disabled']/a")
        self.page_button = "//ul[@class='pagination']/li/a[.='{}']"
        self.pagination_list = (By.XPATH, "//ul[@class='pagination']/li/a")
        self.pagination_page_numbers = (
        By.XPATH, "//ul[@class='pagination']/li[not(contains(@class,'next'))][not(contains(@class,'prev'))]")

        # Custom date selector
        self.from_month = (By.XPATH,
                           "//div[contains(@class,'show-calendar')]//div[@class='drp-calendar left']//select[@class='monthselect']")
        self.from_year = (By.XPATH,
                          "//div[contains(@class,'show-calendar')]//div[@class='drp-calendar left']//select[@class='yearselect']")
        self.from_date = "(//div[contains(@class,'show-calendar')]//div[@class='drp-calendar left']//descendant::tbody//td[.='{}'][not(contains(@class,'off available'))])[1]"

        self.to_month = (By.XPATH,
                         "//div[contains(@class,'show-calendar')]//div[@class='drp-calendar right']//select[@class='monthselect']")
        self.to_year = (By.XPATH,
                        "//div[contains(@class,'show-calendar')]//div[@class='drp-calendar right']//select[@class='yearselect']")
        self.to_date = "(//div[contains(@class,'show-calendar')]//div[@class='drp-calendar right']//descendant::tbody//td[.='{}'][not(contains(@class,'off available'))])[1]"
        self.apply_date = (
        By.XPATH, "//div[contains(@class,'show-calendar')]//div[@class='drp-buttons']//button[.='Apply']")
        self.remove_active_worker = (By.XPATH,
                                     "//span[.='[Active Mobile Workers]']//preceding-sibling::button[@class='select2-selection__choice__remove']")
        self.remove_deactive_worker = (By.XPATH,
                                       "//span[.='[Deactivated Mobile Workers]']//preceding-sibling::button[@class='select2-selection__choice__remove']")
        self.selected_value = "//span[.='{}']//preceding-sibling::button[@class='select2-selection__choice__remove']"
        # Save Report and Favorites
        self.favorite_button = (By.XPATH, "//button[contains(.,'Favorites')]")
        self.empty_fav_list = (By.XPATH, '//a[.="You don\'t have any favorites"]')
        self.saved_fav = "//a[contains(.,'{}')][contains(@data-bind,'text: name')]"
        self.save_config_button = (By.XPATH, "//button[@data-bind='click: setConfigBeingEdited']")
        self.name_field = (By.XPATH, "//input[@data-bind='value: name']")
        self.description_field = (By.XPATH, "//textarea[@data-bind='value: description']")
        self.date_range_field_select = (By.XPATH, "//select[@data-bind='value: date_range']")
        self.save_report_button = (By.XPATH, "//div[@class='btn btn-primary'][.='Save']")
        self.try_again_button = (By.XPATH, "//div[@class='btn btn-primary'][.='Try Again']")
        self.report_save_error = (By.XPATH, "//div[.='Some required fields are missing. Please complete them before saving.']")
        self.cancel_report_button = (By.XPATH, "//div/a[.='Cancel']")
        self.saved_reports_menu_link = (By.LINK_TEXT, 'My Saved Reports')
        self.saved_report_created = "//a[text()='{}']"
        self.delete_saved = "(//a[text()='{}']//following::button[@class='btn btn-danger add-spinner-on-click'])[1]"
        self.saved_report_title = (By.XPATH, "//h4[@data-bind='text: modalTitle']")


        # Email report
        self.email_report_btn = (By.XPATH, "//a[@id='email-report']")
        self.email_subject_field = (By.XPATH, "//input[@id='id_subject']")
        self.email_form_cancel_btn = (By.XPATH, "//input[@id='button-id-close']")
        self.send_email_btn = (By.XPATH, "//input[@id='submit-id-submit_btn']")
        self.email_success_message = (By.XPATH, "//*[.='Report successfully emailed']")

        # Message Log Verification
        self.total_form_counts = "//td[contains(.,'{}')]//following-sibling::td[last()]"
        self.message_log_table_info = (By.XPATH, "//div[@id='report_table_message_log_info']")
        self.empty_table = (By.XPATH, "//tr/td[contains(.,'No data available to display.')]")
        self.message_log_table_title = (By.XPATH, "//h2[@class='panel-title'][contains(.,'Message Log')]")
        self.panel_body_text = (By.XPATH, "//div[@class='panel-body-datatable']")

        self.messaging_list = (By.XPATH, "//h2[.='Messaging']//following-sibling::ul[1]/li/a")
        self.messaging_section = (By.XPATH, "//div[@id='hq-sidebar'][.//h2[.='Messaging']]")

        # Edit Mobile Worker Page
        self.edit_mobile_worker_title = "Edit Mobile Worker : Users :: - CommCare HQ"
        self.username = (By.XPATH, "//span[@class='user_username']")

    def verify_page(self):
        self.wait_to_click(self.message_log_rep)
        self.wait_for_element(self.apply_id, 100)
        self.verify_messaging_section()
        assert self.message_log_TITLE in self.driver.title, "This is not the Message Log page."
        text = self.get_text(self.panel_body_text)
        print(text)
        assert "Why can't I see any data?" in text
        assert "Please choose your filters above and click Apply to see report data." in text

    def hide_filters(self):
        self.wait_to_click(self.message_log_rep)
        self.wait_for_element(self.hide_filters_options)
        self.click(self.hide_filters_options)
        
        assert not self.is_visible_and_displayed(self.message_type_dropdown, 10), "Message type dropdown is still present"
        assert not self.is_visible_and_displayed(self.location_filter_dropdown,
                                                 10), "Location filter dropdown is still present"
        assert not self.is_visible_and_displayed(self.date_input, 10), "Date Range field is still present"
        assert not self.is_visible_and_displayed(self.favorite_button,
                                                 10), "Favorite button is still present"
        assert not self.is_visible_and_displayed(self.save_config_button,
                                                 10), "Save button is still present"
        assert self.is_present(self.show_filters_options), "Show Filters Options is not present"
        print("All filters are hidden!")

    def show_filters(self):
        self.wait_for_element(self.show_filters_options)
        self.click(self.show_filters_options)
        
        assert self.is_present(self.date_input), "Date Range field is not present"
        assert self.is_present(self.message_type_dropdown), "Message type dropdown is not present"
        assert self.is_present(self.location_filter_dropdown), "Location filter dropdown is not present"
        assert self.is_present(self.favorite_button), "Favorite button is not present"
        assert self.is_present(self.save_config_button), "Save button is not present"
        assert self.is_present(self.hide_filters_options), "Show Filters Options is not present"
        print("All filters are shown!")

    def verify_messaging_section(self):
        self.wait_for_element(
            self.messaging_section), "Messaging section is not present in the left panel"
        print("Messaging section is present in the left panel")
        elements = self.find_elements(self.messaging_list)
        link_list = []
        for items in elements:
            link_list.append(items.text)
        print(link_list)
        assert "Message Log" in link_list, "Message Log is not present in the Messaging section"
        print("Message Log is present in the Messaging section")
        assert sorted(link_list) == sorted(
            UserData.messaging_list), "Messaging section list mismatched"
        print("Messaging section has the list: ", link_list)


    def verify_message_log_page_fields_columns(self):
        self.wait_to_click(self.message_log_rep)
        time.sleep(2)
        self.wait_for_element(self.apply_id, 100)
        assert self.message_log_TITLE in self.driver.title, "This is not the Message Log page."
        assert self.is_present(self.date_input), "Date Range field is not present"
        assert self.is_present(self.message_type_dropdown), "Message Type dropdown is not present"
        assert self.is_present(self.location_filter_dropdown), "Location Filter dropdown is not present"
        assert self.is_present(self.apply_id), "Apply button is not present"
        assert self.is_present(self.favorite_button), "Favorite button is not present"
        assert self.is_present(self.save_config_button), "Save button is not present"
        assert self.is_present(self.hide_filters_options), "Show Filters Options is not present"
        assert self.is_present(self.date_range_label), "Timezone label is not present next to Date Range field"
        self.wait_to_click(self.date_input)
        assert self.is_present((By.XPATH, self.date_range_type.format(UserData.date_range[0])))
        assert self.is_present((By.XPATH, self.date_range_type.format(UserData.date_range[1])))
        assert self.is_present((By.XPATH, self.date_range_type.format(UserData.date_range[2])))
        assert self.is_present((By.XPATH, self.date_range_type.format(UserData.date_range[3])))
        self.wait_to_click((By.XPATH, self.date_range_type.format(UserData.date_range[3])))
        assert self.is_present(self.from_year)
        assert self.is_present(self.to_year)
        assert self.is_present(self.apply_date)
        assert self.is_present(self.cancel_date)
        print("All elements of the Date Popup is present")
        self.click(self.cancel_date)
        assert not self.is_visible_and_displayed((By.XPATH, self.date_range_type.format(UserData.date_range[0])), 10)
        assert not self.is_visible_and_displayed((By.XPATH, self.date_range_type.format(UserData.date_range[1])), 10)
        assert not self.is_visible_and_displayed((By.XPATH, self.date_range_type.format(UserData.date_range[2])), 10)
        assert not self.is_visible_and_displayed((By.XPATH, self.date_range_type.format(UserData.date_range[3])), 10)
        assert not self.is_visible_and_displayed(self.from_year, 10)
        assert not self.is_visible_and_displayed(self.to_year, 10)
        assert not self.is_visible_and_displayed(self.apply_date, 10)
        assert not self.is_visible_and_displayed(self.cancel_date, 10)
        print("Date pop up cancelled")
        self.wait_to_click(self.date_input)
        self.wait_to_click((By.XPATH, self.date_range_type.format(UserData.date_range[2])))
        
        text = self.get_attribute(self.date_input, "value")
        date_string, start_date, end_date = self.value_date_range_30_days()
        assert date_string == text
        selected = self.get_selected_text(self.location_filter_dropdown)
        assert selected == UserData.location_filter[0], "Default selected value is incorrect "+selected
        
        type_list = self.get_all_dropdown_options(self.message_type_dropdown)
        assert UserData.message_type == type_list , "Default selected value is incorrect " + selected
        
        self.select_by_text(self.location_filter_dropdown, UserData.location_filter[1])
        self.wait_for_element(self.location_dropdown)
        selected = self.get_selected_text(self.location_dropdown)
        assert selected == UserData.location_dropdown_default[0], "Default selected value is incorrect " + selected

        self.wait_to_click(self.apply_id)
        # assert self.is_present(self.report_loading), "Loading Report block is not present"
        time.sleep(2)
        self.wait_for_element(self.result_table, 300)
        self.wait_for_element(self.report_content_id, 120)
        print("Report loaded successfully!")
        self.scroll_to_bottom()
        time.sleep(100)
        assert self.is_present(self.page_list_dropdown), "Page list dropdown not present"
        assert self.is_present(self.next_page_button), "Next page button not present"
        pages = self.find_elements(self.pagination_page_numbers)
        assert len(pages) > 0, "Number of pages not present"
        self.scroll_to_element(self.report_content_id)
        list_col = self.find_elements(self.column_group_names)
        col_values = []
        print(len(list_col))
        for item in list_col:
            col_values.append(item.text)
        print(col_values)
        assert col_values == UserData.ml_column_names, "All Columns not present"


    def date_generator(self, start, end):
        start_date = parse(start)
        end_date = parse(end)  # perhaps date.now()
        date_list = []
        delta = end_date - start_date  # returns timedelta
        for i in range(delta.days + 1):
            day = start_date + timedelta(days=i)
            day = str(day.strftime('%Y-%m-%d'))
            date_list.append(day)
            print(day)
        return date_list


    def remove_default_users(self):
        self.wait_for_element(self.users_field)
        count = self.find_elements(self.remove_buttons)
        print(len(count))
        for i in range(len(count)):
             count[0].click()
             
             if len(count) != 1:
                ActionChains(self.driver).send_keys(Keys.TAB).perform()
                
             count = self.find_elements(self.remove_buttons)

    def verify_date_column_name_headers(self, date_list):
        print(len(date_list))
        print(date_list)
        if len(date_list)>0:
            for item in date_list:
                assert self.is_present((By.XPATH, self.column_name_headers.format(item))), "Date "+ item +" not present"
                print("Column for date "+ item+ " is present in the table")


    def verify_users_in_the_group(self):
        list_el = self.find_elements(self.results_rows)
        if len(list_el) > 0:
            for items in list_el:
                text = items.text
                assert (ele in text for ele in UserData.automation_group_users), "User " + text + " is not part of the selected group."
                print("User " + text + " is part of the selected group.")

    def verify_users_used_in_the_group(self, user_names):
        list = self.find_elements(self.results_rows)
        if len(list) > 0:
            for items in list:
                text = items.text
                assert (ele in text for ele in user_names) or text == 'Unknown', "User " + text + " is not part of the selected group."
                print("User " + text + " is part of the selected group.")

    def verify_users_used_not_in_the_group(self, user_names):
        list_users = self.find_elements(self.results_rows)
        text_list = list()
        if len(list_users) > 0:
            for items in list_users:
                text = items.text
                text_list.append(text)
        check = any(item in user_names for item in text_list)
        assert check is False, "User is still present"
        print("Following User(s) not present: ", user_names)

    def message_log_pagination_list(self):
        self.wait_to_click(self.message_log_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.message_log_TITLE in self.driver.title, "This is not the Message Log page."
        self.wait_to_click(self.date_input)
        self.wait_to_click((By.XPATH, self.date_range_type.format(UserData.date_range[3])))
        date_string, start_date, end_date = self.get_custom_dates_past(0, 0, 0)
        self.select_date_from_picker(start_date, end_date)
        
        text = self.get_attribute(self.date_input, "value")
        print(text)
        assert text == date_string
        
        self.wait_to_click(self.apply_id)
        time.sleep(2)
        self.wait_for_element(self.result_table, 300)
        self.wait_for_element(self.report_content_id, 120)
        print("Report loaded successfully!")
        self.scroll_to_element(self.result_table)
        self.select_by_value(self.page_list_dropdown, UserData.pagination[0])
        time.sleep(2)
        pages = self.find_elements(self.pagination_list)
        pages_count = len(pages) - 2
        print("Total Pages: ", pages_count)
        first_page = pages[1].text
        last_page = pages[-2].text
        if pages_count > 1:
            assert self.is_present(self.prev_page_button_disabled), "Previous button is not disabled."
            print("Previous button disabled correctly")
            print("Clicking on page " + last_page)
            self.wait_to_click((By.XPATH, self.page_button.format(last_page)))
            time.sleep(15)
            assert self.is_present(self.next_page_button_disabled), "Next button is not disabled."
            print("Next button disabled correctly")
            time.sleep(2)
            print("Clicking on page " + first_page)
            self.wait_to_click((By.XPATH, self.page_button.format(first_page)))
            time.sleep(15)
            list1 = self.find_elements(self.user_names_column_list)
            list1_names = list()
            for item in list1:
                list1_names.append(item.text)
            self.wait_to_click(self.next_page_button)
            time.sleep(2)
            list2 = self.find_elements(self.user_names_column_list)
            list2_names = list()
            for item in list2:
                list2_names.append(item.text)
            print(list1_names, list2_names)
            if len(set(list1_names)) <= 1:
                print("List contains identical values")
            else:
                assert list1_names != list2_names, "Both Pages have same values"
            print("Next button functioning correctly.")
            self.wait_to_click(self.prev_page_button)
            time.sleep(2)
            list3 = self.find_elements(self.user_names_column_list)
            list3_names = list()
            for item in list3:
                list3_names.append(item.text)
            print(list1_names, list2_names, list3_names)
            if len(set(list3_names)) <= 1:
                print("List contains identical values")
            else:
                assert list1_names == list3_names and list2_names != list3_names, "Page contains same data as the previous"
            print("Prev button functioning correctly.")
        else:
            print("Not enough users are present.")
            assert self.is_present(self.prev_page_button_disabled)
            assert self.is_present(self.next_page_button_disabled)
            print("Both Previous and Next Page buttons are disabled correctly.")

    def verify_sorted_list(self, col_name):
        self.select_by_value(self.page_list_dropdown, UserData.pagination[3])
        time.sleep(2)
        self.wait_to_click((By.XPATH, self.user_sort.format(col_name)))
        time.sleep(15)
        if "User Name" in col_name:
            list1 = self.find_elements(self.user_names_column_list)
        elif "Timestamp" in col_name:
            list1 = self.find_elements(self.timestamp_column_list)
        elif "Direction" in col_name:
            list1 = self.find_elements(self.direction_column_list)
        elif "Phone Number" in col_name:
            list1 = self.find_elements(self.phone_number_column_list)
        elif "Message" in col_name:
            list1 = self.find_elements(self.message_column_list)
        elif "Status" in col_name:
            list1 = self.find_elements(self.status_column_list)
        elif "Event" in col_name:
            list1 = self.find_elements(self.event_column_list)
        elif "Type" in col_name:
            list1 = self.find_elements(self.type_column_list)
        else:
            print("Invalid Column Name")
        sorting = self.get_attribute((By.XPATH, self.sorting_value.format(col_name)), "aria-sort")

        list1_names = list()
        for item in list1:
            list1_names.append(item.text)
        print(list1_names)
        print("List is sorted in "+ sorting+" order")
        self.wait_to_click((By.XPATH, self.user_sort.format(col_name)))
        time.sleep(15)
        if "User Name" in col_name:
            list2 = self.find_elements(self.user_names_column_list)
        elif "Timestamp" in col_name:
            list2 = self.find_elements(self.timestamp_column_list)
        elif "Direction" in col_name:
            list2 = self.find_elements(self.direction_column_list)
        elif "Phone Number" in col_name:
            list2 = self.find_elements(self.phone_number_column_list)
        elif "Message" in col_name:
            list2 = self.find_elements(self.message_column_list)
        elif "Status" in col_name:
            list2 = self.find_elements(self.status_column_list)
        elif "Event" in col_name:
            list2 = self.find_elements(self.event_column_list)
        elif "Type" in col_name:
            list2 = self.find_elements(self.type_column_list)
        else:
            print("Invalid Column Name")
        list2_names = list()
        for item in list2:
            list2_names.append(item.text)
        rev_list = list(reversed(list1_names))
        print(list2_names)
        print(rev_list)
        assert list2_names == rev_list, "List is not sorted"
        sorting_new = self.get_attribute((By.XPATH, self.sorting_value.format(col_name)), "aria-sort")
        assert sorting_new != sorting, "List sorting not changed"
        print("List is sorted in "+ sorting_new+" order")

    def verify_pagination_dropdown(self):
        info = self.get_text(self.table_info)
        info = str(info).split(" ")
        print("Total records: ", info[-2])
        for item in UserData.pagination:
            self.select_by_value(self.page_list_dropdown, item)
            time.sleep(15)
            list_rows = self.find_elements(self.user_names_column_list)
            self.scroll_to_element(self.page_list_dropdown)
            print("Updated info: ", self.get_text(self.table_info))
            print(len(list_rows))
            if int(info[-2]) < int(item):
                assert int(len(list_rows)) == int(info[-2]), "List does not have all records."
                print("Records displayed correctly for " + item)
            elif int(info[-2]) >= int(item):
                assert int(len(list_rows)) == int(item), "List does not have all records."
                print("Records displayed correctly for " + item)
            else:
                print("No records to display")


    def value_date_range_7_days(self):
        presentday = datetime.now()  # or presentday = datetime.today()
        # Get Today minus 7 days date
        week_ago = presentday - timedelta(7)
        return str(week_ago.strftime('%Y-%m-%d') + " to " + presentday.strftime('%Y-%m-%d')), week_ago.strftime(
            '%Y-%m-%d'), presentday.strftime('%Y-%m-%d')

    def value_date_range_30_days(self):
        presentday = datetime.now()  # or presentday = datetime.today()
        # Get Today minus 7 days date
        pastday = presentday - timedelta(30)
        return str(pastday.strftime('%Y-%m-%d') + " to " + presentday.strftime('%Y-%m-%d')), pastday.strftime(
            '%Y-%m-%d'), presentday.strftime('%Y-%m-%d')

    def value_date_range_last_month(self):
        last_day_of_prev_month = date.today().replace(day=1) - timedelta(days=1)
        start_day_of_prev_month = date.today().replace(day=1) - timedelta(days=last_day_of_prev_month.day)
        print(start_day_of_prev_month, last_day_of_prev_month)
        return str(start_day_of_prev_month.strftime('%Y-%m-%d') + " to " + last_day_of_prev_month.strftime(
            '%Y-%m-%d')), start_day_of_prev_month.strftime(
            '%Y-%m-%d'), last_day_of_prev_month.strftime('%Y-%m-%d')

    def message_log_search(self, date_range=UserData.date_range[0]):
        date_string = start_date = end_date = ''
        self.wait_to_click(self.message_log_rep)
        time.sleep(2)
        self.wait_for_element(self.apply_id, 100)
        assert self.message_log_TITLE in self.driver.title, "This is not the Message Log page."
        self.wait_to_click(self.date_input)
        self.wait_to_click((By.XPATH, self.date_range_type.format(date_range)))
        text = self.get_attribute(self.date_input, "value")
        print(text)
        if date_range == UserData.date_range[0]:
            date_string, start_date, end_date = self.value_date_range_7_days()
        elif date_range == UserData.date_range[1]:
            date_string, start_date, end_date = self.value_date_range_last_month()
        elif date_range == UserData.date_range[2]:
            date_string, start_date, end_date = self.value_date_range_30_days()
        assert text == date_string
        
        self.click(self.message_type_field)
        self.send_keys(self.message_type_input, UserData.message_type[6])
        self.wait_to_click((By.XPATH, self.users_list_item.format(UserData.message_type[6])))
        
        self.wait_to_click(self.apply_id)
        time.sleep(2)
        self.wait_for_element(self.result_table, 300)
        self.wait_for_element(self.report_content_id, 120)
        print("Report loaded successfully!")
        self.scroll_to_element(self.result_table)
        time.sleep(2)
        type_list = self.find_elements(self.type_column_list)
        for items in type_list:
            assert str(items.text).lower() == str(UserData.message_type[6]).lower(), "Message type mismatch"
        date_list = self.find_elements(self.timestamp_column_list)
        for items in date_list:
            self.date_validator(items.text, start_date, end_date)
        print("Log Submission Dates are with range for " + date_range)



    def verify_dropdown_options(self, locator, list_to_compare):
        print("List to compare: ", list_to_compare)
        assert list_to_compare == self.get_all_dropdown_options(locator), "Dropdown does not have all the options"
        print("All module/form options are present in the dropdown")


    def date_validator(self, date_value, start_date, end_date):
        dt = parse(date_value)
        st = parse(start_date)
        et = parse(end_date)
        dt = dt.date()
        st = st.date()
        et = et.date()
        print(dt, st, et)
        if st <= dt <= et:
            assert True, "Date outside date range"
            print("within range")
        else:
            print("not within range")
            assert False

    def message_log_search_custom_date(self):
        self.wait_to_click(self.message_log_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.message_log_TITLE in self.driver.title, "This is not the Message Log page."
        self.wait_to_click(self.date_input)
        self.wait_to_click((By.XPATH, self.date_range_type.format(UserData.date_range[3])))
        date_string, start_date, end_date = self.get_custom_dates_past(20, 0, 0)
        self.select_date_from_picker(start_date, end_date)
        
        text = self.get_attribute(self.date_input, "value")
        print(text)
        assert text == date_string
        self.click(self.message_type_field)
        self.send_keys(self.message_type_input, UserData.message_type[6])
        self.wait_to_click((By.XPATH, self.users_list_item.format(UserData.message_type[6])))
        
        self.wait_to_click(self.apply_id)
        time.sleep(2)
        self.wait_for_element(self.result_table, 300)
        self.wait_for_element(self.report_content_id, 120)
        print("Report loaded successfully!")
        self.scroll_to_element(self.result_table)
        time.sleep(2)
        type_list = self.find_elements(self.type_column_list)
        for items in type_list:
            assert str(items.text).lower() == str(UserData.message_type[6]).lower(), "Message type mismatch"
        date_list = self.find_elements(self.timestamp_column_list)
        for items in date_list:
            self.date_validator(items.text, start_date, end_date)
        print("Log Submission Dates are with range for " + UserData.date_range[3])


    def get_custom_dates_past(self, days, months, years):
        presentday = datetime.now()  # or presentday = datetime.today()
        pastday = presentday - relativedelta(days=days, months=months, years=years)
        return str(pastday.strftime('%Y-%m-%d') + " to " + presentday.strftime('%Y-%m-%d')), pastday.strftime(
            '%Y-%m-%d'), presentday.strftime('%Y-%m-%d')

    def get_custom_dates_future(self, days, months, years):
        presentday = datetime.now()  # or presentday = datetime.today()
        futureday = presentday + relativedelta(days=days, months=months, years=years)
        return str(presentday.strftime('%Y-%m-%d') + " to " + futureday.strftime('%Y-%m-%d')), presentday.strftime(
            '%Y-%m-%d'), futureday.strftime('%Y-%m-%d')

    def select_date_from_picker(self, start_date, end_date):
        start_date = parse(start_date)
        start_day = str(start_date.day)
        start_month = str(start_date.month - 1)
        start_year = str(start_date.year)
        end_date = parse(end_date)
        end_day = str(end_date.day)
        end_month = str(end_date.month - 1)
        end_year = str(end_date.year)
        self.wait_for_element(self.from_month)
        self.select_by_value(self.from_year, start_year)
        
        self.select_by_value(self.from_month, start_month)
        
        self.wait_to_click((By.XPATH, self.from_date.format(start_day)))
        
        self.wait_for_element(self.to_month)
        self.select_by_value(self.to_year, end_year)
        
        self.select_by_value(self.to_month, end_month)
        
        self.wait_to_click((By.XPATH, self.to_date.format(end_day)))
        
        self.wait_to_click(self.apply_date)

    def message_log_save_report(self):
        self.wait_to_click(self.message_log_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.message_log_TITLE in self.driver.title, "This is not the Message Log page."
        self.wait_to_click(self.date_input)
        self.wait_to_click((By.XPATH, self.date_range_type.format(UserData.date_range[3])))
        date_string, start_date, end_date = self.get_custom_dates_past(0, 0, 1)
        self.select_date_from_picker(start_date, end_date)
        
        text = self.get_attribute(self.date_input, "value")
        print(text)
        assert text == date_string
        
        self.click(self.message_type_field)
        self.send_keys(self.message_type_input, UserData.message_type[6])
        self.wait_to_click((By.XPATH, self.users_list_item.format(UserData.message_type[6])))
        
        self.wait_to_click(self.apply_id)
        time.sleep(2)
        self.wait_for_element(self.result_table, 300)
        self.wait_for_element(self.report_content_id, 120)
        print("Report loaded successfully!")
        self.scroll_to_element(self.result_table)
        type_list = self.find_elements(self.type_column_list)
        for items in type_list:
            assert str(items.text).lower() == str(UserData.message_type[6]).lower(), "Message type mismatch"
        time.sleep(2)
        report_name = "Saved Message Log Report " + fetch_random_string()
        self.verify_favorite_empty(report_name)
        self.save_report_donot_save(report_name)
        report = self.save_report(report_name)
        self.wait_to_click(self.message_log_rep)
        self.wait_for_element(self.apply_id, 100)
        self.verify_favorite_created(report)
        time.sleep(2)
        text = self.get_attribute(self.date_input, "value")
        assert text == date_string
        print("Dates are with in range for " + UserData.date_range[0])
        type_list = self.find_elements(self.type_column_list)
        for items in type_list:
            assert str(items.text).lower() == str(UserData.message_type[6]).lower(), "Message type mismatch"
        self.delete_saved_report(report)
        self.wait_to_click(self.message_log_rep)
        self.verify_favorite_empty(report_name)

    def verify_favorite_empty(self, report=None):
        self.wait_to_click(self.favorite_button)
        if report == None:
            self.wait_for_element(self.empty_fav_list)
        else:
            assert not self.is_visible_and_displayed((By.XPATH, self.saved_fav.format(report)),
                                                     30), "Favorite is already Present"
        print("No Favorites yet.")

    def verify_favorite_created(self, report):
        self.wait_to_click(self.favorite_button)
        assert not self.is_visible_and_displayed(self.empty_fav_list, 10), "Favorites Already Present"
        self.wait_for_element((By.XPATH, self.saved_fav.format(report)))
        print("Favorites added.")
        self.wait_to_click((By.XPATH, self.saved_fav.format(report)))

    def delete_saved_report(self, report):
        self.wait_to_click(self.saved_reports_menu_link)
        self.wait_for_element((By.XPATH, self.saved_report_created.format(report)), 120)
        print("Report Present!")
        self.click((By.XPATH, self.delete_saved.format(report)))
        print("Deleted Saved Report")
        time.sleep(2)
        self.reload_page()
        assert not self.is_visible_and_displayed((By.XPATH, self.saved_report_created.format(report)), 20)
        print("Deleted Report Successfully")

    def save_report_donot_save(self, report_name):
        self.wait_for_element(self.save_config_button)
        self.wait_to_click(self.save_config_button)
        self.wait_to_clear_and_send_keys(self.name_field, report_name)
        self.wait_to_clear_and_send_keys(self.description_field, report_name)
        assert self.is_present(self.date_range_field_select)
        assert self.is_present(self.name_field)
        assert self.is_present(self.description_field)
        assert self.is_present(self.cancel_report_button)
        assert self.is_present(self.save_report_button)
        text = self.get_selected_text(self.date_range_field_select)
        print(text)
        assert UserData.date_range[0].casefold() == text.casefold(), "Date Range does not match"
        print("Date range is matching")
        text = self.get_text(self.saved_report_title)
        print(text)
        assert report_name in text, "Report Name is visible in the Title"
        self.wait_to_click(self.cancel_report_button)
        
        assert not self.is_visible_and_displayed(self.name_field, 10), "Save Report Form not closed"
        assert not self.is_visible_and_displayed(self.description_field, 10)
        assert not self.is_visible_and_displayed(self.date_range_field_select, 10)
        assert not self.is_visible_and_displayed(self.cancel_report_button, 10)
        assert not self.is_visible_and_displayed(self.save_report_button, 10)
        print("Save Report Form is closed")

    def save_report(self, report_name):
        time.sleep(15)
        self.wait_for_element(self.save_config_button)
        self.wait_to_click(self.save_config_button)
        text = self.get_selected_text(self.date_range_field_select)
        print(text)
        assert UserData.date_range[0].casefold() == text.casefold(), "Date Range does not match"
        print("Date range is matching")
        self.clear(self.name_field)
        self.wait_to_click(self.save_report_button)
        time.sleep(3)
        assert self.is_present(self.report_save_error), "Error not displayed"
        print("Error is correctly displayed")
        self.wait_to_clear_and_send_keys(self.name_field, report_name)
        self.clear(self.description_field)
        text = self.get_text(self.saved_report_title)
        print(text)
        assert report_name in text, "Report Name is visible in the Title"
        self.wait_to_click(self.try_again_button)
        
        self.reload_page()
        self.wait_to_click(self.saved_reports_menu_link)
        self.wait_for_element((By.XPATH, self.saved_report_created.format(report_name)), 120)
        print("Report Saved successfully!")
        print("Report name: ", report_name)
        return report_name

    def verify_deleted_group(self):
        self.wait_to_click(self.message_log_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.message_log_TITLE in self.driver.title, "This is not the Message Log page."
        self.click(self.message_type_field)
        self.send_keys(self.message_type_input, UserData.deleted_group)
        
        assert self.is_present(self.no_results), "No results not displayed"
        print("Deleted Group is not present in the Group list")

    def verify_valid_group_with_user(self):
        self.wait_to_click(self.message_log_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.message_log_TITLE in self.driver.title, "This is not the Message Log page."
        self.click(self.message_type_field)
        self.send_keys(self.message_type_input, UserData.user_group)
        
        self.wait_to_click((By.XPATH, self.users_list_item.format(UserData.user_group)))
        
        self.wait_to_click(self.apply_id)
        time.sleep(2)
        self.wait_for_element(self.result_table, 300)
        self.wait_for_element(self.report_content_id, 120)
        print("Report loaded successfully!")
        self.scroll_to_element(self.result_table)
        self.verify_users_in_the_group()
        time.sleep(2)
        for items in UserData.automation_group_users:
            self.wait_to_click((By.PARTIAL_LINK_TEXT, items))
            time.sleep(15)
            assert self.edit_mobile_worker_title in self.driver.title, "This is not the Edit Mobile Worker page."
            self.wait_for_element(self.username)
            assert self.get_text(self.username) == items, "Username not matching: "+items+" and "+self.get_text(self.username)
            print("Username matching: "+items+" and "+self.get_text(self.username))
            
            self.driver.back()
            time.sleep(2)

    def report_filter_message_type(self):
        self.wait_to_click(self.message_log_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.message_log_TITLE in self.driver.title, "This is not the Message Log page."
        self.wait_to_click(self.message_type_field)
        self.wait_for_element(self.message_type_input)
        self.send_keys(self.message_type_input, fetch_random_string())
        
        assert self.is_present(self.no_results), "No results not displayed"
        self.clear(self.message_type_input)
        self.send_keys(self.message_type_input, UserData.message_type[6])
        self.wait_to_click((By.XPATH, self.users_list_item.format(UserData.message_type[6])))
        
        self.send_keys(self.message_type_input, UserData.message_type[2])
        self.wait_to_click((By.XPATH, self.users_list_item.format(UserData.message_type[2])))
        
        assert self.is_present((By.XPATH, self.selected_value.format(UserData.message_type[6]))), "Message type is not present for "+ UserData.message_type[6]
        print("Message type is present for " + UserData.message_type[6])
        assert self.is_present(
            (By.XPATH, self.selected_value.format(UserData.message_type[2]))), "Message type is not present for " + \
                                                                               UserData.message_type[2]
        print("Message type is present for " + UserData.message_type[2])
        self.wait_to_click((By.XPATH, self.selected_value.format(UserData.message_type[6])))
        
        assert not self.is_present(
            (By.XPATH, self.selected_value.format(UserData.message_type[6]))), "Message type is still present for " + \
                                                                               UserData.message_type[6]
        self.wait_to_click((By.XPATH, self.selected_value.format(UserData.message_type[2])))
        
        assert not self.is_present(
            (By.XPATH, self.selected_value.format(UserData.message_type[6]))), "Message type is still present for " + \
                                                                               UserData.message_type[2]

        print("Message Type are working fine")


    def report_filter_location_filter(self, filter):
        self.wait_to_click(self.message_log_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.message_log_TITLE in self.driver.title, "This is not the Message Log page."
        self.wait_to_click(self.date_input)
        self.wait_to_click((By.XPATH, self.date_range_type.format(UserData.date_range[3])))
        date_string, start_date, end_date = self.get_custom_dates_past(0, 0, 1)
        self.select_date_from_picker(start_date, end_date)
        
        text = self.get_attribute(self.date_input, "value")
        print(text)
        assert text == date_string
        
        self.select_by_text(self.location_filter_dropdown, filter)
        if filter == "On":
            self.wait_for_element(self.location_dropdown)
            assert self.is_present(self.location_filter_section), "Location dropdown not present"
            print(self.get_selected_text(self.location_dropdown))
            assert UserData.location_dropdown_default[0] == self.get_selected_text(self.location_dropdown), "Incorrect default value is present"
            self.select_by_text(self.location_dropdown, UserData.location_dropdown_default[1])
        time.sleep(2)
        self.wait_to_click(self.apply_id)
        time.sleep(2)
        self.wait_for_element(self.result_table, 300)
        self.wait_for_element(self.report_content_id, 120)
        print("Report loaded successfully!")
        info = self.get_text(self.message_log_table_info)
        print(info)
        info = str(info).split(" ")
        print("Total records: ", info[-2])
        print("Form Count matching")
        if info[-2] == '0':
            assert self.is_present(self.empty_table)
            print("No data to be displayed")
        else:
            date_list = self.find_elements(self.timestamp_column_list)
            for items in date_list:
                self.date_validator(items.text, start_date, end_date)
            print("Log Submission Dates are with range for " + date_string)

    def export_message_log_to_excel(self):
        self.wait_to_click(self.message_log_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.message_log_TITLE in self.driver.title, "This is not the Message Log page."
        self.wait_to_click(self.date_input)
        self.wait_to_click((By.XPATH, self.date_range_type.format(UserData.date_range[3])))
        date_string, start_date, end_date = self.get_custom_dates_past(0, 0, 0)
        self.select_date_from_picker(start_date, end_date)
        
        text = self.get_attribute(self.date_input, "value")
        print(text)
        assert text == date_string
        time.sleep(2)
        self.wait_to_click(self.apply_id)
        time.sleep(2)
        self.wait_for_element(self.result_table, 300)
        self.wait_for_element(self.report_content_id, 120)
        print("Report loaded successfully!")
        assert self.is_present(self.export_to_excel), "Export to Excel button is not displayed"
        print("Export to Excel button is displayed")
        self.select_by_value(self.page_list_dropdown, UserData.pagination[3])
        time.sleep(2)
        self.wait_to_click((By.XPATH, self.user_sort.format("Timestamp")))
        time.sleep(15)
        sorting = self.get_attribute((By.XPATH, self.sorting_value.format("Timestamp")), "aria-sort")
        if sorting != "ascending":
            self.wait_to_click((By.XPATH, self.user_sort.format("Timestamp")))
            time.sleep(15)
            sorting = self.get_attribute((By.XPATH, self.sorting_value.format("Timestamp")), "aria-sort")
            assert sorting == "ascending"
        else:
            print("List is in ascending order")
        self.wait_for_element(self.form_activity_results)
        col = self.find_elements(self.form_activity_results_cells)
        list = []
        for c in col:
            list.append(c.text)
        print(list)
        self.wait_to_click(self.export_to_excel)
        time.sleep(15)
        print("Export to excel successful")
        return list

    def compare_message_log_with_webdata(self, web_data):
        print(web_data)
        web_data = [sub.replace('+', '') for sub in web_data]
        newest_file = latest_download_file()
        path = os.path.join(PathSettings.DOWNLOAD_PATH, newest_file)
        print(path)
        new_data = pd.read_excel(path, sheet_name=0, index_col=None)
        new_data.drop(new_data.columns[[0, 1]], axis=1, inplace=True)
        print(new_data.values)
        ext_list = []
        ext_list.extend(new_data.values.tolist())
        list = []
        for i in range(len(ext_list))[:]:
            list += ext_list[i]
        print("List New: ", list)
        print("Old data rows: ", len(web_data), "New data rows: ", len(list))
        print("Old List: ", web_data)
        print("New list: ", list)
        assert len(web_data) == len(list), "Data in Both Excel and Searched results do not match"
        print("Both Excel and Searched results have same amount of data")
        for i in range(len(list)):
            print("Comparing ", html.unescape(str(list[i])), " with ", str(web_data[i]))
            assert html.unescape(str(list[i])) == str(web_data[i]) or html.unescape(str(list[i])) in str(web_data[i]), "Comparison failed for " + list[i] + " and " + web_data[i]
