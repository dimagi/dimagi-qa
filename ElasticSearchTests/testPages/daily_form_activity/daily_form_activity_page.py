import html
import os
import time

import dateutil.relativedelta
import pandas as pd

from datetime import datetime, timedelta, date
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
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


class DailyFormActivityPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

        # Mobile Worker Reports
        self.reports_menu_id = (By.ID, "ProjectReportsTab")
        self.daily_form_activity_rep = (By.LINK_TEXT, "Daily Form Activity")
        self.DAILY_FORM_ACTIVITY_TITLE = "Daily Form Activity - CommCare HQ"

        # Report Elements
        self.apply_id = (By.ID, "apply-filters")
        self.report_content_id = (By.ID, "report-content")
        self.homepage = (By.XPATH, ".//a[@href='/homepage/']")
        self.date_range_error = (By.XPATH, "//td[contains(.,'You are limited to a span of 90 days,')]")

        self.form_activity_results = (By.XPATH, "//table[@id='report_table_daily_form_stats']/tbody/tr")
        self.form_activity_results_cells = (By.XPATH, "//table[@id='report_table_daily_form_stats']/tbody/tr/td")
        self.users_field = (By.XPATH, "(//textarea[@class='select2-search__field'])[1]")
        self.filter_dates_by = (By.XPATH, "//select[@id='report_filter_sub_time']")
        self.remove_buttons = (By.XPATH, "//ul//button")
        self.user_remove_btn = (By.XPATH, "(//button[@class='select2-selection__choice__remove'])[last()]")
        self.user_from_list = "//li[contains(.,'{}')]"
        self.export_to_excel = (By.XPATH, "//a[@id='export-report-excel']")
        self.export_success = (By.XPATH,
                               "//span[.='Your requested Excel report will be sent to the email address defined in your account settings.']")
        self.user_column = (
        By.XPATH, "(//thead/tr/th[@aria-controls='report_table_daily_form_stats']/div[contains(.,'Username')])[1]")
        self.group_column = (
        By.XPATH, "(//thead/tr/th[@aria-controls='report_table_daily_form_stats']/div[contains(.,'Group')])[1]")
        self.total_column = (By.XPATH, "(//thead/tr/th[@aria-controls='report_table_daily_form_stats']/div[contains(.,'Total')])[1]")
        self.users_list_item = "//ul[@role='listbox']/li[contains(.,'{}')]"
        self.users_list = (By.XPATH, "//ul[contains(@class,'select2-results__options')]/li")
        self.users_list_empty = (
        By.XPATH, "//ul[contains(@id,'select2-emw-bi-results')]/li[.='The results could not be loaded.']")

        self.date_input = (By.XPATH, "//input[@id='filter_range']")
        self.date_range_type = "//li[@data-range-key='{}']"
        self.column_names = "(//thead/tr/th[@aria-controls='report_table_daily_form_stats']/div[@data-title='{}'])[1]"
        self.column_group_names = "(//thead/tr/th//strong[.='{}'])[1]"
        self.user_names_column_list = (By.XPATH, "//table[@id='report_table_daily_form_stats']//tbody//td[1]")
        self.last_submission_column_list = (By.XPATH, "//table[@id='report_table_daily_form_stats']//tbody//td[4]")
        self.result_table = (By.XPATH, "(//div[@id='report-content']//table//tbody//td[1])[1]")
        self.results_rows = (By.XPATH, "//tbody/tr")
        self.result_rows_names = "//tbody/tr/td[1][contains(.,'{}')]"
        self.hide_filters_options = (By.XPATH, "//a[.='Hide Filter Options']")
        self.show_filters_options = (By.XPATH, "//a[.='Show Filter Options']")
        self.user_sort = (
        By.XPATH, "(//text()[contains(.,'User')]//preceding-sibling::i[@class='icon-white fa dt-sort-icon'])[1]")
        self.active_cases_column_list = (By.XPATH, "//table[@id='report_table_daily_form_stats']//tbody//td[7]")
        self.total_cases_shared_column_list = (By.XPATH, "//table[@id='report_table_daily_form_stats']//tbody//td[8]")
        self.column_name_headers = "//table[@id='report_table_daily_form_stats']//thead//th/div/div[contains(.,'{}')]"


        # Pagination
        self.page_list_dropdown = (By.XPATH, "//select[@name='report_table_daily_form_stats_length']")
        self.table_info = (By.XPATH, "//div[@id='report_table_daily_form_stats_info']")
        self.prev_page_button = (By.XPATH, "//ul[@class='pagination']/li[@class='prev']/a")
        self.next_page_button = (By.XPATH, "//ul[@class='pagination']/li[@class='next']/a")
        self.prev_page_button_disabled = (By.XPATH, "//ul[@class='pagination']/li[@class='prev disabled']/a")
        self.next_page_button_disabled = (By.XPATH, "//ul[@class='pagination']/li[@class='next disabled']/a")
        self.page_button = "//ul[@class='pagination']/li/a[.='{}']"
        self.pagination_list = (By.XPATH, "//ul[@class='pagination']/li/a")

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

        # Case Type Verify
        self.case_created_column = (By.XPATH, "//table[@id='report_table_daily_form_stats']//tbody//td[5]//a")
        self.case_created_title = (By.XPATH, "//table[@id='report_table_daily_form_stats']//tbody//td[5]//span")
        self.case_list_table = (By.XPATH, "//table[@id='report_table_case_list']/tbody/tr/td[1]")
        self.case_list_table_title = (By.XPATH, "//h2[@class='panel-title'][contains(.,'Case List')]")
        self.case_list_table_info = (By.XPATH, "//div[@id='report_table_case_list_info']")
        self.case_list_page_dropdown = (By.XPATH, "//select[@name='report_table_case_list_length']")

        # Email report
        self.email_report_btn = (By.XPATH, "//a[@id='email-report']")
        self.email_subject_field = (By.XPATH, "//input[@id='id_subject']")
        self.email_form_cancel_btn = (By.XPATH, "//input[@id='button-id-close']")
        self.send_email_btn = (By.XPATH, "//input[@id='submit-id-submit_btn']")
        self.email_success_message = (By.XPATH, "//*[.='Report successfully emailed']")

        # Submit History Verification
        self.total_form_counts = "//td[contains(.,'{}')]//following-sibling::td[last()]"
        self.filter_column_name = "(//thead//th[@aria-controls='report_table_submit_history'][3]/div[contains(.,'{}')])[1]"
        self.submit_history_table_info = (By.XPATH, "//div[@id='report_table_submit_history_info']")
        self.empty_table = (By.XPATH, "//tr/td[contains(.,'No data available to display.')]")
        self.submit_history_table_title = (By.XPATH, "//h2[@class='panel-title'][contains(.,'Submit History')]")


    def hide_filters(self):
        self.wait_to_click(self.daily_form_activity_rep)
        self.wait_for_element(self.hide_filters_options)
        self.click(self.hide_filters_options)
        time.sleep(2)
        assert not self.is_visible_and_displayed(self.users_field, 10), "User field is still present"
        assert not self.is_visible_and_displayed(self.date_input, 10), "Date Range field is still present"
        assert not self.is_visible_and_displayed(self.filter_dates_by, 10), "Filter Dates By field is still present"
        assert self.is_present(self.show_filters_options), "Show Filters Options is not present"
        print("All filters are hidden!")

    def show_filters(self):
        self.wait_for_element(self.show_filters_options)
        self.click(self.show_filters_options)
        time.sleep(2)
        assert self.is_present(self.users_field), "User field is not present"
        assert self.is_present(self.date_input), "Date Range field is not present"
        assert self.is_present(self.filter_dates_by), "Filter Dates By field is not present"
        assert self.is_present(self.hide_filters_options), "Show Filters Options is not present"
        print("All filters are shown!")

    def verify_daily_activity_page_fields(self):
        self.wait_to_click(self.daily_form_activity_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.DAILY_FORM_ACTIVITY_TITLE in self.driver.title, "This is not the Daily Form Activity page."
        assert self.is_present(self.users_field), "User field is not present"
        assert self.is_present(self.date_input), "Date Range field is not present"
        assert self.is_present(self.filter_dates_by), "Filter Dates By field is not present"
        assert self.is_present(self.hide_filters_options), "Show Filters Options is not present"
        print("All filters are shown!")

    def verify_table_columns(self):
        self.wait_to_click(self.daily_form_activity_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.DAILY_FORM_ACTIVITY_TITLE in self.driver.title, "This is not the Daily Form Activity page."
        self.verify_user_lookup_table()
        self.remove_default_users()
        self.send_keys(self.users_field, UserData.user_group)
        self.wait_to_click((By.XPATH, self.users_list_item.format(UserData.user_group)))
        time.sleep(1)
        self.select_by_text(self.filter_dates_by, UserData.filter_dates_by[0])
        self.wait_to_click(self.date_input)
        self.wait_to_click((By.XPATH, self.date_range_type.format(UserData.date_range[0])))
        text = self.get_attribute(self.date_input, "value")
        print(text)
        date_string, start_date, end_date = self.value_date_range_7_days()
        time.sleep(2)
        self.wait_to_click(self.apply_id)
        time.sleep(10)
        self.wait_for_element(self.result_table, 300)
        assert self.is_visible_and_displayed(self.report_content_id, 120), "Report not loaded"
        print("Report loaded successfully!")
        self.scroll_to_element(self.result_table)
        time.sleep(5)
        assert self.is_present(self.user_column), "Username Column not present"
        assert self.is_present(self.total_column), "Total Column not present"
        list_of_columns = self.date_generator(start_date, end_date)
        self.verify_date_column_name_headers(list_of_columns)

    def verify_user_lookup_table(self):
        self.wait_to_click(self.users_field)
        time.sleep(2)
        assert not self.is_visible_and_displayed(self.users_list_empty, 10), "Case Type List is not empty"
        list = self.find_elements(self.users_list)
        print(len(list))
        assert int(len(list)) >= 1
        print("A Look up for Case type is successfully loaded")

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
             time.sleep(2)
             if len(count) != 1:
                ActionChains(self.driver).send_keys(Keys.TAB).perform()
                time.sleep(2)
             count = self.find_elements(self.remove_buttons)

    def verify_date_column_name_headers(self, date_list):
        print(len(date_list))
        print(date_list)
        if len(date_list)>0:
            for item in date_list:
                assert self.is_present((By.XPATH, self.column_name_headers.format(item))), "Date "+ item +" not present"
                print("Column for date "+ item+ " is present in the table")


    def verify_users_in_the_group(self):
        list = self.find_elements(self.results_rows)
        if len(list) > 0:
            for item in UserData.automation_group_users:
                assert self.is_present((By.XPATH, self.result_rows_names.format(
                    item))), "Group user " + item + " is not present in results."
                print("Group User " + item + " is present in results.")


    def daily_form_activity_pagination_list(self):
        self.wait_to_click(self.daily_form_activity_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.DAILY_FORM_ACTIVITY_TITLE in self.driver.title, "This is not the Worker Activity page."
        self.select_by_text(self.filter_dates_by, UserData.filter_dates_by[0])
        self.wait_to_click(self.date_input)
        self.wait_to_click((By.XPATH, self.date_range_type.format(UserData.date_range[2])))
        text = self.get_attribute(self.date_input, "value")
        print(text)
        date_string, start_date, end_date = self.value_date_range_30_days()
        assert text == date_string
        time.sleep(2)
        self.wait_to_click(self.apply_id)
        time.sleep(10)
        self.wait_for_element(self.result_table, 300)
        assert self.is_visible_and_displayed(self.report_content_id, 120), "Report not loaded"
        print("Report loaded successfully!")
        self.scroll_to_element(self.result_table)
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
            time.sleep(5)
            print("Clicking on page " + first_page)
            self.wait_to_click((By.XPATH, self.page_button.format(first_page)))
            time.sleep(15)
            list1 = self.find_elements(self.user_names_column_list)
            list1_names = list()
            for item in list1:
                list1_names.append(item.text)
            self.wait_to_click(self.next_page_button)
            time.sleep(5)
            list2 = self.find_elements(self.user_names_column_list)
            list2_names = list()
            for item in list2:
                list2_names.append(item.text)
            print(list1_names, list2_names)
            assert list1_names != list2_names, "Both Pages have same values"
            print("Next button functioning correctly.")
            self.wait_to_click(self.prev_page_button)
            time.sleep(5)
            list3 = self.find_elements(self.user_names_column_list)
            list3_names = list()
            for item in list3:
                list3_names.append(item.text)
            print(list1_names, list2_names, list3_names)
            assert list1_names == list3_names and list2_names != list3_names, "Page contains same data as the previous"
            print("Prev button functioning correctly.")
        else:
            print("Not enough users are present.")
            assert self.is_present(self.prev_page_button_disabled)
            assert self.is_present(self.next_page_button_disabled)
            print("Both Previous and Next Page buttons are disabled correctly.")

    def verify_pagination_dropdown(self):
        info = self.get_text(self.table_info)
        info = str(info).split(" ")
        print("Total records: ", info[-2])

        for item in UserData.pagination:
            self.select_by_value(self.page_list_dropdown, item)
            time.sleep(10)
            list = self.find_elements(self.user_names_column_list)
            print(len(list))
            if int(info[-2]) < int(item):
                assert int(len(list)) == int(info[-2]), "List does not have all records."
                print("Records displayed correctly for " + item)
            elif int(info[-2]) >= int(item):
                assert int(len(list)) == int(item), "List does not have all records."
                print("Records displayed correctly for " + item)
            else:
                print("No records to display")

    def verify_sorted_list(self):
        list1 = self.find_elements(self.user_names_column_list)
        list1_names = list()
        for item in list1:
            list1_names.append(item.text)
        sorted_list = sorted(list1_names)
        assert list1_names == sorted_list, "List is not sorted"
        print("List is in ascending order")
        self.wait_to_click(self.user_sort)
        time.sleep(15)
        list2 = self.find_elements(self.user_names_column_list)
        list2_names = list()
        for item in list2:
            list2_names.append(item.text)
        rev_list = sorted(list1_names, reverse=True)
        assert list2_names == rev_list, "List is not sorted"
        print("List is in descending order")

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

    def daily_form_activity_search(self, date_range=UserData.date_range[0]):
        date_string = start_date = end_date = ''
        self.wait_to_click(self.daily_form_activity_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.DAILY_FORM_ACTIVITY_TITLE in self.driver.title, "This is not the Daily Form Activity page."
        self.select_by_text(self.filter_dates_by, UserData.filter_dates_by[0])
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
        time.sleep(2)
        self.wait_to_click(self.apply_id)
        time.sleep(10)
        self.wait_for_element(self.result_table, 300)
        assert self.is_visible_and_displayed(self.report_content_id, 120), "Report not loaded"
        print("Report loaded successfully!")
        self.scroll_to_element(self.result_table)
        time.sleep(5)
        list_of_columns = self.date_generator(start_date, end_date)
        self.verify_date_column_name_headers(list_of_columns)
        print("Dates are with in range for " + date_range)

    def date_validator(self, date_value, start_date, end_date):
        dt = parse(date_value)
        st = parse(start_date)
        et = parse(end_date)
        print(dt, st, et)
        if st <= dt <= et:
            assert True, "Date outside date range"
            print("within range")
        else:
            print("not within range")
            assert False

    def daily_form_activity_search_custom_date(self):
        self.wait_to_click(self.daily_form_activity_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.DAILY_FORM_ACTIVITY_TITLE in self.driver.title, "This is not the Daily Form Activity page."
        self.select_by_text(self.filter_dates_by, UserData.filter_dates_by[0])
        date_string, start_date, end_date = self.get_custom_dates_past(0, 0, 5)
        self.clear(self.date_input)
        self.send_keys(self.date_input,  date_string+Keys.TAB)
        text = self.get_attribute(self.date_input, "value")
        print(text)
        self.wait_to_click(self.apply_id)
        time.sleep(10)
        self.wait_for_element(self.result_table, 300)
        assert self.is_visible_and_displayed(self.report_content_id, 120), "Report not loaded"
        print("Report loaded successfully!")
        self.scroll_to_element(self.result_table)
        time.sleep(5)
        assert self.is_present_and_displayed(self.date_range_error), "Date Range Error not displayed"
        print("Date Range error correctly displayed")
        self.wait_to_click(self.daily_form_activity_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.DAILY_FORM_ACTIVITY_TITLE in self.driver.title, "This is not the Daily Form Activity page."
        self.wait_to_click(self.date_input)
        self.wait_to_click((By.XPATH, self.date_range_type.format(UserData.date_range[3])))
        date_string, start_date, end_date = self.get_custom_dates_past(20, 0, 0)
        self.select_date_from_picker(start_date, end_date)
        time.sleep(2)
        text = self.get_attribute(self.date_input, "value")
        print(text)
        assert text == date_string
        self.wait_to_click(self.apply_id)
        time.sleep(10)
        self.wait_for_element(self.result_table, 300)
        assert self.is_visible_and_displayed(self.report_content_id, 120), "Report not loaded"
        print("Report loaded successfully!")
        self.scroll_to_element(self.result_table)
        time.sleep(5)
        list_of_columns = self.date_generator(start_date, end_date)
        self.verify_date_column_name_headers(list_of_columns)
        print("Dates are with in range for " + UserData.date_range[3])


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
        time.sleep(2)
        self.select_by_value(self.from_month, start_month)
        time.sleep(2)
        self.wait_to_click((By.XPATH, self.from_date.format(start_day)))
        time.sleep(2)
        self.wait_for_element(self.to_month)
        self.select_by_value(self.to_year, end_year)
        time.sleep(2)
        self.select_by_value(self.to_month, end_month)
        time.sleep(2)
        self.wait_to_click((By.XPATH, self.to_date.format(end_day)))
        time.sleep(2)
        self.wait_to_click(self.apply_date)

    def daily_form_activity_save_report(self):
        self.wait_to_click(self.daily_form_activity_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.DAILY_FORM_ACTIVITY_TITLE in self.driver.title, "This is not the Worker Activity page."
        self.verify_user_lookup_table()
        self.remove_default_users()
        self.send_keys(self.users_field, UserData.user_group)
        self.wait_to_click((By.XPATH, self.users_list_item.format(UserData.user_group)))
        time.sleep(1)
        self.select_by_text(self.filter_dates_by, UserData.filter_dates_by[0])
        self.wait_to_click(self.date_input)
        self.wait_to_click((By.XPATH, self.date_range_type.format(UserData.date_range[0])))
        text = self.get_attribute(self.date_input, "value")
        print(text)
        date_string, start_date, end_date = self.value_date_range_7_days()
        time.sleep(2)
        self.wait_to_click(self.apply_id)
        time.sleep(10)
        self.wait_for_element(self.result_table, 300)
        assert self.is_visible_and_displayed(self.report_content_id, 120), "Report not loaded"
        print("Report loaded successfully!")
        self.verify_users_in_the_group()
        list_of_columns = self.date_generator(start_date, end_date)
        self.verify_date_column_name_headers(list_of_columns)
        print("Dates are with in range for " + UserData.date_range[0])
        time.sleep(10)
        report_name = "Saved Daily Form Activity Report " + fetch_random_string()
        self.verify_favorite_empty(report_name)
        self.save_report_donot_save(report_name)
        self.save_report(report_name)
        self.wait_to_click(self.daily_form_activity_rep)
        self.wait_for_element(self.apply_id, 100)
        self.verify_favorite_created(report_name)
        time.sleep(10)
        self.verify_users_in_the_group()
        list_of_columns = self.date_generator(start_date, end_date)
        self.verify_date_column_name_headers(list_of_columns)
        print("Dates are with in range for " + UserData.date_range[0])
        self.delete_saved_report(report_name)
        self.wait_to_click(self.daily_form_activity_rep)
        self.verify_favorite_empty(report_name)

    def verify_favorite_empty(self, report=None):
        self.wait_to_click(self.favorite_button)
        if report == None:
            assert self.is_visible_and_displayed(self.empty_fav_list), "Favorites Already Present"
        else:
            assert not self.is_visible_and_displayed((By.XPATH, self.saved_fav.format(report)),
                                                     30), "Favorite is already Present"
        print("No Favorites yet.")

    def verify_favorite_created(self, report):
        self.wait_to_click(self.favorite_button)
        assert not self.is_visible_and_displayed(self.empty_fav_list, 10), "Favorites Already Present"
        assert self.is_visible_and_displayed((By.XPATH, self.saved_fav.format(report))), "Favorite Not Present"
        print("Favorites added.")
        self.wait_to_click((By.XPATH, self.saved_fav.format(report)))

    def delete_saved_report(self, report):
        self.wait_to_click(self.saved_reports_menu_link)
        assert self.is_visible_and_displayed((By.XPATH, self.saved_report_created.format(report)), 120)
        print("Report Present!")
        self.click((By.XPATH, self.delete_saved.format(report)))
        print("Deleted Saved Report")
        time.sleep(5)
        self.driver.refresh()
        assert not self.is_visible_and_displayed((By.XPATH, self.saved_report_created.format(report)), 20)
        print("Deleted Report Successfully")

    def save_report_donot_save(self, report_name):
        self.wait_for_element(self.save_config_button)
        self.wait_to_click(self.save_config_button)
        self.wait_to_clear_and_send_keys(self.name_field, report_name)
        text = self.get_selected_text(self.date_range_field_select)
        print(text)
        assert UserData.date_range[0].casefold() == text.casefold(), "Date Range does not match"
        print("Date range is matching")
        self.wait_to_click(self.cancel_report_button)
        time.sleep(2)
        assert not self.is_visible_and_displayed(self.name_field, 10), "Save Report Form not closed"
        print("Save Report Form is closed")

    def save_report(self, report_name):
        self.wait_for_element(self.save_config_button)
        self.wait_to_click(self.save_config_button)
        self.clear(self.name_field)
        self.wait_to_click(self.save_report_button)
        time.sleep(3)
        assert self.is_present(self.report_save_error), "Error not displayed"
        print("Error is correctly displayed")
        self.wait_to_clear_and_send_keys(self.name_field, report_name)
        text = self.get_selected_text(self.date_range_field_select)
        print(text)
        assert UserData.date_range[0].casefold() == text.casefold(), "Date Range does not match"
        print("Date range is matching")
        self.wait_to_click(self.try_again_button)
        time.sleep(2)
        self.driver.refresh()
        self.wait_to_click(self.saved_reports_menu_link)
        assert self.is_visible_and_displayed((By.XPATH, self.saved_report_created.format(report_name)), 120)
        print("Report Saved successfully!")
        print("Report name: ", report_name)
        return report_name

    def verify_case_type_data(self):
        case_type_list = self.find_elements(self.case_created_column)
        if len(case_type_list) > 0:
            for item in case_type_list:
                text = item.text
                print("Cases created ", text)
                if text == '0':
                    print("No Cases were created withing the given range")
                else:
                    self.wait_to_click(item)
                    self.switch_to_next_tab()
                    time.sleep(10)
                    self.wait_for_element(self.case_list_table_title, 200)
                    self.scroll_to_bottom()
                    info = self.get_text(self.case_list_table_info)
                    info = str(info).split(" ")
                    print("Total records: ", info[-2])
                    assert info[-2] == text, "Case created count mismatch"
                    print("Cases created count matched")
                    self.select_by_value(self.case_list_page_dropdown, '100')
                    time.sleep(10)
                    cases = self.find_elements(self.case_list_table)
                    if len(cases) > 0:
                        for case in cases:
                            name = case.text
                            assert name == UserData.case_reassign, "Case Type mismatch"
                            print("Case Type matching")
                    time.sleep(2)
                    self.driver.close()
                    time.sleep(2)
                    self.switch_back_to_prev_tab()

    def export_daily_form_activity_to_excel(self):
        self.wait_to_click(self.daily_form_activity_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.DAILY_FORM_ACTIVITY_TITLE in self.driver.title, "This is not the Worker Activity page."
        self.verify_user_lookup_table()
        self.remove_default_users()
        self.send_keys(self.users_field, UserData.user_group)
        self.wait_to_click((By.XPATH, self.users_list_item.format(UserData.user_group)))
        time.sleep(1)
        self.select_by_text(self.filter_dates_by, UserData.filter_dates_by[0])
        self.wait_to_click(self.date_input)
        self.wait_to_click((By.XPATH, self.date_range_type.format(UserData.date_range[0])))
        time.sleep(2)
        self.wait_to_click(self.apply_id)
        time.sleep(10)
        self.wait_for_element(self.result_table, 300)
        assert self.is_visible_and_displayed(self.report_content_id, 120), "Report not loaded"
        print("Report loaded successfully!")
        self.verify_users_in_the_group()
        self.wait_for_element(self.form_activity_results)
        col = self.find_elements(self.form_activity_results_cells)
        list = []
        for c in col:
            list.append(c.text)
        print(list)
        self.wait_to_click(self.export_to_excel)
        self.wait_for_element(self.export_success)
        print("Export to excel successful")
        print("Sleeping for some time for the email to be sent")
        time.sleep(30)
        return list

    def compare_dfa_with_email(self, link, web_data):
        print(link)
        print(web_data)
        self.driver.get(link)
        time.sleep(10)
        newest_file = latest_download_file()
        path = os.path.join(PathSettings.DOWNLOAD_PATH, newest_file)
        print(path)
        new_data = pd.read_excel(path, sheet_name=0, index_col=None)
        print(new_data.values)
        ext_list = []
        ext_list.extend(new_data.values.tolist())
        list = []
        for i in range(len(ext_list) - 1)[:]:
            list += ext_list[i]
        print("List New: ", list)
        print("Old data rows: ", len(web_data), "New data rows: ", len(list))
        print("Old List: ", web_data)
        print("New list: ", list)
        assert len(web_data) == len(list), "Data in Both Excel and Searched results do not match"
        print("Both Excel and Searched results have same amount of data")
        for i in range(len(list)):
            print("Comparing ", html.unescape(str(list[i])), " with ", str(web_data[i]))
            assert html.unescape(str(list[i])) == str(web_data[i]), "Cpmparision failed for " + list[i] + " and " + \
                                                                        web_data[i]

    def export_daily_form_activity_email(self):
        self.wait_to_click(self.daily_form_activity_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.DAILY_FORM_ACTIVITY_TITLE in self.driver.title, "This is not the Daily Form Activity page."
        self.verify_user_lookup_table()
        self.remove_default_users()
        self.send_keys(self.users_field, UserData.user_group)
        self.wait_to_click((By.XPATH, self.users_list_item.format(UserData.user_group)))
        time.sleep(1)
        self.select_by_text(self.filter_dates_by, UserData.filter_dates_by[0])
        self.wait_to_click(self.date_input)
        self.wait_to_click((By.XPATH, self.date_range_type.format(UserData.date_range[0])))
        time.sleep(2)
        self.wait_to_click(self.apply_id)
        time.sleep(10)
        self.wait_for_element(self.result_table, 300)
        assert self.is_visible_and_displayed(self.report_content_id, 120), "Report not loaded"
        print("Report loaded successfully!")
        self.wait_for_element(self.form_activity_results)
        col = self.find_elements(self.form_activity_results_cells)
        list = []
        for c in col:
            list.append(c.text)
        print(list)
        subject = UserData.email_daily_form_report
        self.email_report_form_not_save(subject)
        self.email_report_form(subject)
        print("Export to excel successful")
        print("Sleeping for some time for the email to be sent")
        time.sleep(30)
        return list, subject

    def email_report_form_not_save(self, subject):
        self.wait_for_element(self.email_report_btn)
        self.wait_to_click(self.email_report_btn)
        self.wait_for_element(self.email_subject_field)
        self.wait_to_clear_and_send_keys(self.email_subject_field, subject)
        self.wait_to_click(self.email_form_cancel_btn)
        print("Email report form closed properly")

    def email_report_form(self, subject):
        self.wait_for_element(self.email_report_btn)
        self.wait_to_click(self.email_report_btn)
        self.wait_for_element(self.email_subject_field)
        self.wait_to_clear_and_send_keys(self.email_subject_field, subject)
        self.wait_to_click(self.send_email_btn)
        assert self.is_visible_and_displayed(self.email_success_message), "Email report not sent successfully"
        print("Email report sent successfully")

    def compare_dfa_with_html_table(self, table_data, web_data):
        list = table_data
        print("Old data rows: ", len(web_data), "New data rows: ", len(list))
        print("Old List: ", web_data)
        print("New list: ", list)
        assert len(web_data) == len(list), "Data in Both Email Body and Searched results do not match"
        print("Both Email Body and Searched results have same amount of data")
        for i in range(len(list)):
            print("Comparing ", html.unescape(str(list[i])), " with ", str(web_data[i]))
            assert html.unescape(str(list[i])) == str(web_data[i]), "Cpmparision failed for " + list[i] + " and " + \
                                                                    web_data[i]

    def daily_form_activity_users_active(self):
        self.wait_to_click(self.daily_form_activity_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.DAILY_FORM_ACTIVITY_TITLE in self.driver.title, "This is not the Worker Activity page."
        self.wait_to_click(self.remove_active_worker)
        assert not self.is_present(self.remove_active_worker), "Active Mobile Worker is still not removed"
        print("Active Mobile Worker is removed successfully")
        self.driver.refresh()
        self.wait_for_element(self.apply_id, 100)
        self.verify_user_lookup_table()
        self.remove_default_users()
        self.send_keys(self.users_field, UserData.daily_form_groups[0])
        self.wait_to_click((By.XPATH, self.users_list_item.format(UserData.daily_form_groups[0])))
        time.sleep(1)
        self.select_by_text(self.filter_dates_by, UserData.filter_dates_by[0])
        self.wait_to_click(self.date_input)
        self.wait_to_click((By.XPATH, self.date_range_type.format(UserData.date_range[0])))
        time.sleep(2)
        self.wait_to_click(self.apply_id)
        time.sleep(10)
        self.wait_for_element(self.result_table, 300)
        assert self.is_visible_and_displayed(self.report_content_id, 120), "Report not loaded"
        print("Report loaded successfully!")
        self.select_by_value(self.page_list_dropdown, UserData.pagination[3])
        time.sleep(10)
        assert not self.is_present((By.XPATH, self.result_rows_names.format(UserData.deactivated_user))), "Deactivated user " + UserData.deactivated_user + " is present in the active worker list."
        print("All Active users are present")



    def daily_form_activity_users_deactivated(self):
        self.wait_to_click(self.daily_form_activity_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.DAILY_FORM_ACTIVITY_TITLE in self.driver.title, "This is not the Worker Activity page."
        self.wait_to_click(self.remove_deactive_worker)
        assert not self.is_present(self.remove_deactive_worker), "Deactivated Mobile Worker is still not removed"
        print("Deactivated Mobile Worker is removed successfully")
        self.driver.refresh()
        self.wait_for_element(self.apply_id, 100)
        self.verify_user_lookup_table()
        self.remove_default_users()
        self.send_keys(self.users_field, UserData.daily_form_groups[1])
        self.wait_to_click((By.XPATH, self.users_list_item.format(UserData.daily_form_groups[1])))
        time.sleep(1)
        self.select_by_text(self.filter_dates_by, UserData.filter_dates_by[0])
        self.wait_to_click(self.date_input)
        self.wait_to_click((By.XPATH, self.date_range_type.format(UserData.date_range[0])))
        time.sleep(2)
        self.wait_to_click(self.apply_id)
        time.sleep(10)
        self.wait_for_element(self.result_table, 300)
        assert self.is_visible_and_displayed(self.report_content_id, 120), "Report not loaded"
        print("Report loaded successfully!")
        self.select_by_value(self.page_list_dropdown, UserData.pagination[3])
        time.sleep(10)
        assert self.is_present((By.XPATH, self.result_rows_names.format(UserData.deactivated_user))), "Deactivated user " + UserData.deactivated_user + " is not present in the Deactivated worker list."
        print("All Deactivated users are present")


    def verify_assigned_cases_count(self, actives, totals):
        print("Sleeping for some time for the cases to be assigned")
        time.sleep(60)
        self.wait_to_click(self.daily_form_activity_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.DAILY_FORM_ACTIVITY_TITLE in self.driver.title, "This is not the Worker Activity page."
        self.send_keys(self.users_field, UserData.user_group)
        self.wait_to_click((By.XPATH, self.user_from_list.format(UserData.user_group)))
        time.sleep(1)
        self.select_by_text(self.view_by_dropdown, UserData.view_by[0])
        self.wait_to_click(self.date_input)
        self.wait_to_click((By.XPATH, self.date_range_type.format(UserData.date_range[2])))
        self.wait_to_click(self.apply_id)
        time.sleep(10)
        self.wait_for_element(self.result_table, 300)
        assert self.is_visible_and_displayed(self.report_content_id, 120), "Report not loaded"
        print("Report loaded successfully!")
        self.scroll_to_bottom()
        self.verify_users_in_the_group()
        active_cases = self.find_elements(self.active_cases_column_list)
        actives_new = []
        for items in active_cases:
            actives_new.append(items.text)
        total_cases = self.find_elements(self.total_cases_shared_column_list)
        totals_new = []
        for items in total_cases:
            totals_new.append(items.text)
        print("Active Case: ", actives_new)
        print("Total shared case: ", totals_new)
        for i in range(len(actives_new)):
            assert int(actives[i])-10 == actives_new[i], "Active Cases not reduced"
            print("Active cases reduced")
        for i in range(len(totals_new)):
            assert int(totals[i])-10 == totals_new[i], "Active Cases not reduced"
            print("Active cases reduced")
        print("Cases successfully assigned")

    def filter_dates_and_verify(self, filter):
        self.wait_to_click(self.daily_form_activity_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.DAILY_FORM_ACTIVITY_TITLE in self.driver.title, "This is not the Worker Activity page."
        self.verify_user_lookup_table()
        self.remove_default_users()
        self.send_keys(self.users_field, UserData.user_group)
        self.wait_to_click((By.XPATH, self.users_list_item.format(UserData.user_group)))
        time.sleep(1)
        self.select_by_text(self.filter_dates_by, filter)
        self.wait_to_click(self.date_input)
        self.wait_to_click((By.XPATH, self.date_range_type.format(UserData.date_range[0])))
        date_string = self.get_attribute(self.date_input, "value")
        time.sleep(2)
        self.wait_to_click(self.apply_id)
        time.sleep(10)
        self.wait_for_element(self.result_table, 300)
        assert self.is_visible_and_displayed(self.report_content_id, 120), "Report not loaded"
        print("Report loaded successfully!")
        self.scroll_to_bottom()
        self.verify_users_in_the_group()
        for items in UserData.automation_group_users:
            count = self.get_text((By.XPATH, self.total_form_counts.format(items)))
            print(count)
            self.wait_to_click((By.PARTIAL_LINK_TEXT, items))
            time.sleep(15)
            self.wait_for_element(self.submit_history_table_title)
            self.wait_for_element(self.result_table, 300)
            assert self.is_visible_and_displayed(self.report_content_id, 120), "Report not loaded"
            print("Report loaded successfully!")
            assert filter == self.get_selected_text(self.filter_dates_by), "Date Filter mismatched"
            print("Date Filter matched")
            assert date_string == self.get_attribute(self.date_input, "value"), "Date Range mismatched"
            print("Date Range matched")
            assert self.is_present((By.XPATH, self.filter_column_name.format(filter))), "Incorrect column present"
            print("Correct Column present")
            self.scroll_to_bottom()
            time.sleep(2)
            self.wait_for_element(self.submit_history_table_info, 120)
            info = self.get_text(self.submit_history_table_info)
            print(info)
            info = str(info).split(" ")
            print("Total records: ", info[-2])
            assert count == info[-2], "Form counts not matching"
            print("Form Count matching")
            if count == '0':
                assert self.is_present(self.empty_table)
                print("Correct value displayed")
            time.sleep(5)
            self.driver.back()



