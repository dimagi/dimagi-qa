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


class SubmissionsByFormPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

        # Mobile Worker Reports
        self.reports_menu_id = (By.ID, "ProjectReportsTab")
        self.sub_by_form_rep = (By.LINK_TEXT, "Submissions By Form")
        self.sub_by_form_TITLE = "Submissions By Form - CommCare HQ"

        # Report Elements
        self.apply_id = (By.ID, "apply-filters")
        self.report_content_id = (By.ID, "report-content")
        self.homepage = (By.XPATH, ".//a[@href='/homepage/']")
        self.date_range_error = (By.XPATH, "//td[contains(.,'You are limited to a span of 90 days,')]")

        self.form_activity_results = (By.XPATH, "//table[@id='report_table_submissions_by_form']/tbody/tr")
        self.form_activity_results_cells = (
            By.XPATH, "//table[@id='report_table_submissions_by_form']/tbody/tr[not(contains(.,'All Users'))]/td")
        self.all_users_results_cells = (
            By.XPATH, "(//tfoot)[2]/tr/td")
        self.users_field = (By.XPATH, "(//textarea[@class='select2-search__field'])[1]")
        self.filter_dates_by = (By.XPATH, "//select[@id='report_filter_sub_time']")
        self.remove_buttons = (By.XPATH, "//ul//button")
        self.user_remove_btn = (By.XPATH, "(//button[@class='select2-selection__choice__remove'])[last()]")
        self.user_from_list = "//li[contains(.,'{}')]"
        self.export_to_excel = (By.XPATH, "//a[@id='export-report-excel']")
        self.export_success = (By.XPATH,
                               "//span[.='Your requested Excel report will be sent to the email address defined in your account settings.']")
        self.user_column = (
            By.XPATH, "(//thead/tr/th[@aria-controls='report_table_submissions_by_form']/div[contains(.,'User')])[1]")
        self.all_forms_column = (
            By.XPATH,
            "(//thead/tr/th[@aria-controls='report_table_submissions_by_form']/div[contains(.,'All Forms')])[1]")
        self.app_mod_form_column = "(//thead/tr/th[@aria-controls='report_table_submissions_by_form']/div[contains(.,'{}')])[1]"
        self.users_list_item = "//ul[@role='listbox']/li[contains(.,'{}')]"
        self.users_list = (By.XPATH, "//ul[contains(@class,'select2-results__options')]/li")
        self.users_list_empty = (
            By.XPATH, "//ul[contains(@id,'select2-emw-bi-results')]/li[.='The results could not be loaded.']")

        self.date_input = (By.XPATH, "//input[@id='filter_range']")
        self.date_range_type = "//li[@data-range-key='{}']"
        self.column_names = "(//thead/tr/th[@aria-controls='report_table_submissions_by_form']/div[@data-title='{}'])[1]"
        self.column_group_names = "(//thead/tr/th//strong[.='{}'])[1]"
        self.user_names_column_list = (By.XPATH, "//table[@id='report_table_submissions_by_form']//tbody//td[1]")
        self.last_submission_column_list = (By.XPATH, "//table[@id='report_table_submissions_by_form']//tbody//td[4]")
        self.result_table = (By.XPATH, "(//div[@id='report-content']//table//tbody//td[1])[1]")
        self.results_rows = (By.XPATH, "//tbody/tr")
        self.result_rows_names = "//table[@id='report_table_submissions_by_form']//tbody/tr/td[1]//a[contains(.,'{}')]"
        self.hide_filters_options = (By.XPATH, "//a[.='Hide Filter Options']")
        self.show_filters_options = (By.XPATH, "//a[.='Show Filter Options']")
        self.user_sort = (
            By.XPATH,
            "//div[@class='DTFC_LeftWrapper']//text()[contains(.,'User')]//preceding-sibling::i[@class='icon-white fa dt-sort-icon']")
        self.active_cases_column_list = (By.XPATH, "//table[@id='report_table_submissions_by_form']//tbody//td[7]")
        self.total_cases_shared_column_list = (
            By.XPATH, "//table[@id='report_table_submissions_by_form']//tbody//td[8]")
        self.column_name_headers = "//table[@id='report_table_submissions_by_form']//thead//th/div/div[contains(.,'{}')]"

        # Pagination
        self.page_list_dropdown = (By.XPATH, "//select[@name='report_table_submissions_by_form_length']")
        self.table_info = (By.XPATH, "//div[@id='report_table_submissions_by_form_info']")
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
        self.report_save_error = (
            By.XPATH, "//div[.='Some required fields are missing. Please complete them before saving.']")
        self.cancel_report_button = (By.XPATH, "//div/a[.='Cancel']")
        self.saved_reports_menu_link = (By.LINK_TEXT, 'My Saved Reports')
        self.saved_report_created = "//a[text()='{}']"
        self.delete_saved = "(//a[text()='{}']//following::button[@class='btn btn-danger add-spinner-on-click'])[1]"

        # Case Type Verify
        self.case_created_column = (By.XPATH, "//table[@id='report_table_submissions_by_form']//tbody//td[5]//a")
        self.case_created_title = (By.XPATH, "//table[@id='report_table_submissions_by_form']//tbody//td[5]//span")
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

        # Application form section
        self.application_dropdown = (By.XPATH, "//select[@id='report_filter_form_app_id']")
        self.module_dropdown = (By.XPATH, "//select[@id='report_filter_form_module']")
        self.form_dropdown = (By.XPATH, "//select[@id='report_filter_form_xmlns']")
        self.show_adv_options = (By.XPATH, "//input[@name='show_advanced']")
        self.known_forms = (By.XPATH, "//input[@id='report_filter_form_unknown_hide']")
        self.unknown_forms = (By.XPATH, "//input[@id='report_filter_form_unknown_show']")
        self.unknown_form_dropdown = (By.XPATH, "//select[@id='report_filter_form-unknown_xmlns']")
        self.application_type_dropdown = (By.XPATH, "//select[@id='report_filter_form_status']")

        # Submit History Verification
        self.total_form_counts = "//td[contains(.,'{}')]//following-sibling::td[last()]"
        self.filter_column_name = "(//thead//th[@aria-controls='report_table_submit_history'][3]/div[contains(.,'{}')])[1]"
        self.submit_history_table_info = (By.XPATH, "//div[@id='report_table_submit_history_info']")
        self.empty_table = (By.XPATH, "//tr/td[contains(.,'No data available to display.')]")
        self.submit_history_table_title = (By.XPATH, "//h2[@class='panel-title'][contains(.,'Submit History')]")

    def hide_filters(self):
        self.wait_to_click(self.sub_by_form_rep)
        self.wait_for_element(self.hide_filters_options)
        self.click(self.hide_filters_options)
        
        assert not self.is_visible_and_displayed(self.users_field, 10), "User field is still present"
        assert not self.is_visible_and_displayed(self.application_dropdown, 10), "Application dropdown is still present"
        assert not self.is_visible_and_displayed(self.show_adv_options,
                                                 10), "Show Advance Options checkbox is still present"
        assert not self.is_visible_and_displayed(self.date_input, 10), "Date Range field is still present"
        assert not self.is_visible_and_displayed(self.filter_dates_by, 10), "Filter Dates By field is still present"
        assert self.is_present(self.show_filters_options), "Show Filters Options is not present"
        print("All filters are hidden!")

    def show_filters(self):
        self.wait_for_element(self.show_filters_options)
        self.click(self.show_filters_options)
        
        assert self.is_present(self.users_field), "User field is not present"
        assert self.is_present(self.date_input), "Date Range field is not present"
        assert self.is_present(self.application_dropdown), "Application dropdown is not present"
        assert self.is_present(self.show_adv_options), "Show Advance Options checkbox is not present"
        assert self.is_present(self.filter_dates_by), "Filter Dates By field is not present"
        assert self.is_present(self.hide_filters_options), "Show Filters Options is not present"
        print("All filters are shown!")

    def verify_sub_by_form_page_fields(self):
        self.wait_to_click(self.sub_by_form_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.sub_by_form_TITLE in self.driver.title, "This is not the Submissions By Form page."
        assert self.is_present(self.users_field), "User field is not present"
        assert self.is_present(self.application_dropdown), "Application dropdown is not present"
        assert self.is_present(self.show_adv_options), "Show Advance Options checkbox is not present"
        assert self.is_present(self.date_input), "Date Range field is not present"
        assert self.is_present(self.filter_dates_by), "Filter Dates By field is not present"
        assert self.is_present(self.hide_filters_options), "Show Filters Options is not present"
        print("All filters are shown!")

    def verify_table_columns(self):
        self.wait_to_click(self.sub_by_form_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.sub_by_form_TITLE in self.driver.title, "This is not the Submissions By Form page."
        self.verify_user_lookup_table()
        self.remove_default_users()
        self.send_keys(self.users_field, UserData.user_group)
        self.wait_to_click((By.XPATH, self.users_list_item.format(UserData.user_group)))
        
        self.select_application_and_forms(UserData.reassign_cases_application,
                                          list(UserData.reasign_modules_forms.keys())[1],
                                          UserData.reasign_modules_forms[
                                              list(UserData.reasign_modules_forms.keys())[1]][0])
        column_name = UserData.reassign_cases_application + " > " + list(UserData.reasign_modules_forms.keys())[
            1] + " > " + UserData.reasign_modules_forms[list(UserData.reasign_modules_forms.keys())[1]][0]
        self.select_by_text(self.filter_dates_by, UserData.filter_dates_by[0])
        self.wait_to_click(self.date_input)
        self.wait_to_click((By.XPATH, self.date_range_type.format(UserData.date_range[0])))
        text = self.get_attribute(self.date_input, "value")
        print(text)
        
        self.wait_to_click(self.apply_id)
        time.sleep(2)
        self.wait_for_element(self.result_table, 300)
        self.wait_for_element(self.report_content_id, 120)
        print("Report loaded successfully!")
        self.scroll_to_element(self.result_table)
        time.sleep(2)
        assert self.is_present(self.user_column), "Username Column not present"
        assert self.is_present(self.all_forms_column), "All Forms Column not present"
        assert self.is_present(
            (By.XPATH, self.app_mod_form_column.format(column_name))), "Form Name Column not present: " + column_name

    def select_application_and_forms(self, app, module, form):
        self.wait_for_element(self.application_dropdown)
        text = self.get_selected_text(self.application_dropdown)
        print(text)
        assert UserData.default_app_mod_form[0] in text, "Values mismatch: " + text + " and " + \
                                                         UserData.default_app_mod_form[0]
        print(UserData.default_app_mod_form[0] + " is present as default value")
        self.select_by_text(self.application_dropdown, app)
        self.wait_for_element(self.module_dropdown)
        text = self.get_selected_text(self.module_dropdown)
        print(text)
        assert UserData.default_app_mod_form[1] in text, "Values mismatch: " + text + " and " + \
                                                         UserData.default_app_mod_form[1]
        print(UserData.default_app_mod_form[1] + " is present as default value")
        mod_list = [UserData.default_app_mod_form[1]] + list(UserData.reasign_modules_forms.keys())
        self.verify_dropdown_options(self.module_dropdown, mod_list)
        self.select_by_text(self.module_dropdown, module)
        self.wait_for_element(self.form_dropdown)
        text = self.get_selected_text(self.form_dropdown)
        print(text)
        assert UserData.default_app_mod_form[2] in text, "Values mismatch: " + text + " and " + \
                                                         UserData.default_app_mod_form[2]
        print(UserData.default_app_mod_form[2] + " is present as default value")
        form_list = [UserData.default_app_mod_form[2]] + UserData.reasign_modules_forms[module]
        self.verify_dropdown_options(self.form_dropdown, form_list)
        self.select_by_text(self.form_dropdown, form)

    def verify_dropdown_options(self, locator, list_to_compare):
        print("List to compare: ", list_to_compare)
        assert list_to_compare == self.get_all_dropdown_options(locator), "Dropdown does not have all the options"
        print("All module/form options are present in the dropdown")

    def verify_user_lookup_table(self):
        self.wait_to_click(self.users_field)
        
        assert not self.is_visible_and_displayed(self.users_list_empty, 10), "User List is not empty"
        list = self.find_elements(self.users_list)
        print(len(list))
        assert int(len(list)) >= 1
        print("A Look up for users is successfully loaded")

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

    def verify_users_in_the_group(self):
        list = self.find_elements(self.results_rows)
        if len(list) > 0:
            for item in UserData.automation_group_users:
                assert self.is_present((By.XPATH, self.result_rows_names.format(
                    item))), "Group user " + item + " is not present in results."
                print("Group User " + item + " is present in results.")

    def sub_by_form_pagination_list(self):
        self.wait_to_click(self.sub_by_form_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.sub_by_form_TITLE in self.driver.title, "This is not the Worker Activity page."
        self.select_application_and_forms(UserData.reassign_cases_application,
                                          list(UserData.reasign_modules_forms.keys())[1],
                                          UserData.reasign_modules_forms[
                                              list(UserData.reasign_modules_forms.keys())[1]][0])
        self.select_by_text(self.filter_dates_by, UserData.filter_dates_by[0])
        self.wait_to_click(self.date_input)
        self.wait_to_click((By.XPATH, self.date_range_type.format(UserData.date_range[2])))
        text = self.get_attribute(self.date_input, "value")
        print(text)
        date_string, start_date, end_date = self.value_date_range_30_days()
        assert text == date_string
        
        self.wait_to_click(self.apply_id)
        time.sleep(2)
        self.wait_for_element(self.result_table, 300)
        self.wait_for_element(self.report_content_id, 120)
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
            assert list1_names != list2_names, "Both Pages have same values"
            print("Next button functioning correctly.")
            self.wait_to_click(self.prev_page_button)
            time.sleep(2)
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
            time.sleep(2)
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
        rev_list = list(reversed(sorted_list))
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

    def sub_by_form_search(self, date_range=UserData.date_range[0]):
        date_string = start_date = end_date = ''
        self.wait_to_click(self.sub_by_form_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.sub_by_form_TITLE in self.driver.title, "This is not the Submissions By Form page."
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
        
        self.wait_to_click(self.apply_id)
        time.sleep(2)
        self.wait_for_element(self.result_table, 300)
        self.wait_for_element(self.report_content_id, 120)
        print("Report loaded successfully!")
        self.scroll_to_element(self.result_table)
        time.sleep(2)
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

    def sub_by_form_search_custom_date(self):
        self.wait_to_click(self.sub_by_form_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.sub_by_form_TITLE in self.driver.title, "This is not the Submissions By Form page."
        self.select_by_text(self.filter_dates_by, UserData.filter_dates_by[0])
        date_string, start_date, end_date = self.get_custom_dates_past(0, 0, 5)
        self.clear(self.date_input)
        self.send_keys(self.date_input, date_string + Keys.TAB)
        text = self.get_attribute(self.date_input, "value")
        print(text)
        self.wait_to_click(self.apply_id)
        time.sleep(2)
        self.wait_for_element(self.result_table, 300)
        self.wait_for_element(self.report_content_id, 120)
        print("Report loaded successfully!")
        self.scroll_to_element(self.result_table)
        time.sleep(2)
        assert self.is_present_and_displayed(self.date_range_error), "Date Range Error not displayed"
        print("Date Range error correctly displayed")
        self.wait_to_click(self.sub_by_form_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.sub_by_form_TITLE in self.driver.title, "This is not the Submissions By Form page."
        self.wait_to_click(self.date_input)
        self.wait_to_click((By.XPATH, self.date_range_type.format(UserData.date_range[3])))
        date_string, start_date, end_date = self.get_custom_dates_past(20, 0, 0)
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
        time.sleep(2)
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
        
        self.select_by_value(self.from_month, start_month)
        
        self.wait_to_click((By.XPATH, self.from_date.format(start_day)))
        
        self.wait_for_element(self.to_month)
        self.select_by_value(self.to_year, end_year)
        
        self.select_by_value(self.to_month, end_month)
        
        self.wait_to_click((By.XPATH, self.to_date.format(end_day)))
        
        self.wait_to_click(self.apply_date)

    def sub_by_form_save_report(self):
        self.wait_to_click(self.sub_by_form_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.sub_by_form_TITLE in self.driver.title, "This is not the Worker Activity page."
        self.verify_user_lookup_table()
        self.remove_default_users()
        self.send_keys(self.users_field, UserData.user_group)
        self.wait_to_click((By.XPATH, self.users_list_item.format(UserData.user_group)))
        
        self.select_application_and_forms(UserData.reassign_cases_application,
                                          list(UserData.reasign_modules_forms.keys())[1],
                                          UserData.reasign_modules_forms[
                                              list(UserData.reasign_modules_forms.keys())[1]][0])
        self.select_by_text(self.filter_dates_by, UserData.filter_dates_by[0])
        self.wait_to_click(self.date_input)
        self.wait_to_click((By.XPATH, self.date_range_type.format(UserData.date_range[0])))
        text = self.get_attribute(self.date_input, "value")
        print(text)
        date_string, start_date, end_date = self.value_date_range_7_days()
        
        self.wait_to_click(self.apply_id)
        time.sleep(2)
        self.wait_for_element(self.result_table, 300)
        self.wait_for_element(self.report_content_id, 120)
        print("Report loaded successfully!")
        self.verify_users_in_the_group()
        time.sleep(2)
        report_name = "Saved Submissions By Form Report " + fetch_random_string()
        self.verify_favorite_empty(report_name)
        self.save_report_donot_save(report_name)
        report = self.save_report(report_name)
        self.wait_to_click(self.sub_by_form_rep)
        self.wait_for_element(self.apply_id, 100)
        self.verify_favorite_created(report)
        time.sleep(2)
        self.verify_users_in_the_group()
        self.delete_saved_report(report)
        self.wait_to_click(self.sub_by_form_rep)
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
        text = self.get_selected_text(self.date_range_field_select)
        print(text)
        assert UserData.date_range[0].casefold() == text.casefold(), "Date Range does not match"
        print("Date range is matching")
        self.wait_to_click(self.cancel_report_button)
        
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
        
        self.reload_page()
        self.wait_to_click(self.saved_reports_menu_link)
        self.wait_for_element((By.XPATH, self.saved_report_created.format(report_name)), 120)
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
                    time.sleep(2)
                    self.wait_for_element(self.case_list_table_title, 200)
                    self.scroll_to_bottom()
                    info = self.get_text(self.case_list_table_info)
                    info = str(info).split(" ")
                    print("Total records: ", info[-2])
                    assert info[-2] == text, "Case created count mismatch"
                    print("Cases created count matched")
                    self.select_by_value(self.case_list_page_dropdown, '100')
                    time.sleep(2)
                    cases = self.find_elements(self.case_list_table)
                    if len(cases) > 0:
                        for case in cases:
                            name = case.text
                            assert name == UserData.case_reassign, "Case Type mismatch"
                            print("Case Type matching")
                    
                    self.driver.close()
                    
                    self.switch_back_to_prev_tab()

    def export_sub_by_form_to_excel(self):
        self.wait_to_click(self.sub_by_form_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.sub_by_form_TITLE in self.driver.title, "This is not the Worker Activity page."
        self.verify_user_lookup_table()
        self.remove_default_users()
        self.send_keys(self.users_field, UserData.user_group)
        self.wait_to_click((By.XPATH, self.users_list_item.format(UserData.user_group)))
        
        self.select_application_and_forms(UserData.reassign_cases_application,
                                          list(UserData.reasign_modules_forms.keys())[1],
                                          UserData.reasign_modules_forms[
                                              list(UserData.reasign_modules_forms.keys())[1]][0])
        self.select_by_text(self.filter_dates_by, UserData.filter_dates_by[0])
        self.wait_to_click(self.date_input)
        self.wait_to_click((By.XPATH, self.date_range_type.format(UserData.date_range[0])))
        
        self.wait_to_click(self.apply_id)
        time.sleep(2)
        self.wait_for_element(self.result_table, 300)
        self.wait_for_element(self.report_content_id, 120)
        print("Report loaded successfully!")
        self.verify_users_in_the_group()
        self.wait_for_element(self.form_activity_results)
        col = self.find_elements(self.form_activity_results_cells)
        list_col = []
        for c in col:
            list_col.append(c.text)
        print(list_col)
        self.wait_to_click(self.export_to_excel)
        print("Export to excel successful")
        print("sleeping for sometime for the download to complete")
        time.sleep(15)
        return list_col

    def compare_sbf_with_email(self, web_data):
        print(web_data)
        newest_file = latest_download_file()
        path = os.path.join(PathSettings.DOWNLOAD_PATH, newest_file)
        print(path)
        new_data = pd.read_excel(path, sheet_name=0, index_col=None)
        print(new_data.values)
        ext_list = []
        ext_list.extend(new_data.values.tolist())
        list = []
        for i in range(len(ext_list))[:-1]:
            list += ext_list[i]
        print("List New: ", list)
        print("Old data rows: ", len(web_data), "New data rows: ", len(list))
        print("Old List: ", web_data)
        print("New list: ", list)
        assert len(web_data) == len(list), "Data in Both Excel and Searched results do not match"
        print("Both Excel and Searched results have same amount of data")
        for i in range(len(list)):
            print("Comparing ", html.unescape(str(list[i])), " with ", str(web_data[i]))
            assert html.unescape(str(list[i])) == str(web_data[i]) or html.unescape(str(list[i])) in str(web_data[i]), \
                "Comparison failed for " + list[i] + " and " + web_data[i]

    def export_sub_by_form_email(self):
        self.wait_to_click(self.sub_by_form_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.sub_by_form_TITLE in self.driver.title, "This is not the Submissions By Form page."
        self.verify_user_lookup_table()
        self.remove_default_users()
        self.send_keys(self.users_field, UserData.user_group)
        self.wait_to_click((By.XPATH, self.users_list_item.format(UserData.user_group)))
        
        self.select_application_and_forms(UserData.reassign_cases_application,
                                          list(UserData.reasign_modules_forms.keys())[1],
                                          UserData.reasign_modules_forms[
                                              list(UserData.reasign_modules_forms.keys())[1]][0])
        self.select_by_text(self.filter_dates_by, UserData.filter_dates_by[0])
        self.wait_to_click(self.date_input)
        self.wait_to_click((By.XPATH, self.date_range_type.format(UserData.date_range[0])))
        
        self.wait_to_click(self.apply_id)
        time.sleep(2)
        self.wait_for_element(self.result_table, 300)
        self.wait_for_element(self.report_content_id, 120)
        print("Report loaded successfully!")
        self.wait_for_element(self.form_activity_results)
        col = self.find_elements(self.form_activity_results_cells)
        list_col = []
        for c in col:
            list_col.append(c.text)
        print(list_col)
        footer = self.find_elements(self.all_users_results_cells)
        list_ft = []
        for f in footer:
            list_ft.append(f.text)
        print(list_ft)
        list_col.extend(list_ft)
        subject = UserData.email_sub_by_form_report
        self.email_report_form_not_save(subject)
        self.email_report_form(subject)
        print("Export to excel successful")

        return list_col, subject

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
        self.wait_for_element(self.email_success_message)
        print("Email report sent successfully")

    def compare_sbf_with_html_table(self, table_data, web_data):
        list = table_data
        print("Table data rows: ", len(web_data), "Web data rows: ", len(list))
        print("Table List: ", web_data)
        print("Web list: ", list)
        assert len(web_data) == len(list), "Data in Both Email Body and Searched results do not match"
        print("Both Email Body and Searched results have same amount of data")
        for i in range(len(list)):
            print("Comparing ", html.unescape(str(list[i])), " with ", str(web_data[i]))
            assert html.unescape(str(list[i])) == str(web_data[i]), "Cpmparision failed for " + list[i] + " and " + \
                                                                    web_data[i]

    def sub_by_form_users_active(self):
        self.wait_to_click(self.sub_by_form_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.sub_by_form_TITLE in self.driver.title, "This is not the Worker Activity page."
        self.wait_to_click(self.remove_active_worker)
        assert not self.is_present(self.remove_active_worker), "Active Mobile Worker is still not removed"
        print("Active Mobile Worker is removed successfully")
        self.reload_page()
        self.wait_for_element(self.apply_id, 100)
        self.verify_user_lookup_table()
        self.remove_default_users()
        self.send_keys(self.users_field, UserData.daily_form_groups[0])
        self.wait_to_click((By.XPATH, self.users_list_item.format(UserData.daily_form_groups[0])))
        
        self.select_application_and_forms(UserData.reassign_cases_application,
                                          list(UserData.reasign_modules_forms.keys())[1],
                                          UserData.reasign_modules_forms[
                                              list(UserData.reasign_modules_forms.keys())[1]][0])

        self.select_by_text(self.filter_dates_by, UserData.filter_dates_by[0])
        self.wait_to_click(self.date_input)
        self.wait_to_click((By.XPATH, self.date_range_type.format(UserData.date_range[0])))
        
        self.wait_to_click(self.apply_id)
        time.sleep(2)
        self.wait_for_element(self.result_table, 300)
        self.wait_for_element(self.report_content_id, 120)
        print("Report loaded successfully!")
        self.select_by_value(self.page_list_dropdown, UserData.pagination[3])
        time.sleep(2)
        assert not self.is_present((By.XPATH, self.result_rows_names.format(
            UserData.deactivated_user))), "Deactivated user " + UserData.deactivated_user + " is present in the active worker list."
        print("All Active users are present")

    def sub_by_form_users_deactivated(self):
        self.wait_to_click(self.sub_by_form_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.sub_by_form_TITLE in self.driver.title, "This is not the Worker Activity page."
        self.wait_to_click(self.remove_deactive_worker)
        assert not self.is_present(self.remove_deactive_worker), "Deactivated Mobile Worker is still not removed"
        print("Deactivated Mobile Worker is removed successfully")
        self.reload_page()
        self.wait_for_element(self.apply_id, 100)
        self.verify_user_lookup_table()
        self.remove_default_users()
        self.send_keys(self.users_field, UserData.daily_form_groups[1])
        self.wait_to_click((By.XPATH, self.users_list_item.format(UserData.daily_form_groups[1])))
        
        self.select_application_and_forms(UserData.reassign_cases_application,
                                          list(UserData.reasign_modules_forms.keys())[1],
                                          UserData.reasign_modules_forms[
                                              list(UserData.reasign_modules_forms.keys())[1]][0])

        self.select_by_text(self.filter_dates_by, UserData.filter_dates_by[0])
        self.wait_to_click(self.date_input)
        self.wait_to_click((By.XPATH, self.date_range_type.format(UserData.date_range[0])))
        
        self.wait_to_click(self.apply_id)
        time.sleep(2)
        self.wait_for_element(self.result_table, 300)
        self.wait_for_element(self.report_content_id, 120)
        print("Report loaded successfully!")
        self.select_by_value(self.page_list_dropdown, UserData.pagination[3])
        time.sleep(2)
        assert self.is_present((By.XPATH, self.result_rows_names.format(
            UserData.deactivated_user))), "Deactivated user " + UserData.deactivated_user + " is not present in the Deactivated worker list."
        print("All Deactivated users are present")

    def verify_assigned_cases_count(self, actives, totals):
        print("Sleeping for some time for the cases to be assigned")
        time.sleep(60)
        self.wait_to_click(self.sub_by_form_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.sub_by_form_TITLE in self.driver.title, "This is not the Worker Activity page."
        self.send_keys(self.users_field, UserData.user_group)
        self.wait_to_click((By.XPATH, self.user_from_list.format(UserData.user_group)))
        
        self.select_by_text(self.view_by_dropdown, UserData.view_by[0])
        self.wait_to_click(self.date_input)
        self.wait_to_click((By.XPATH, self.date_range_type.format(UserData.date_range[2])))
        self.wait_to_click(self.apply_id)
        time.sleep(2)
        self.wait_for_element(self.result_table, 300)
        self.wait_for_element(self.report_content_id, 120)
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
            assert int(actives[i]) - 10 == actives_new[i], "Active Cases not reduced"
            print("Active cases reduced")
        for i in range(len(totals_new)):
            assert int(totals[i]) - 10 == totals_new[i], "Active Cases not reduced"
            print("Active cases reduced")
        print("Cases successfully assigned")

    def filter_dates_and_verify(self, filter):
        self.wait_to_click(self.sub_by_form_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.sub_by_form_TITLE in self.driver.title, "This is not the Worker Activity page."
        self.verify_user_lookup_table()
        self.remove_default_users()
        self.send_keys(self.users_field, UserData.user_group)
        self.wait_to_click((By.XPATH, self.users_list_item.format(UserData.user_group)))
        
        self.select_application_and_forms(UserData.reassign_cases_application,
                                          list(UserData.reasign_modules_forms.keys())[1],
                                          UserData.reasign_modules_forms[
                                              list(UserData.reasign_modules_forms.keys())[1]][0])

        self.select_by_text(self.filter_dates_by, filter)
        date_string, start_date, end_date = self.get_custom_dates_past(20, 0, 0)
        self.clear(self.date_input)
        self.send_keys(self.date_input, date_string + Keys.TAB)
        text = self.get_attribute(self.date_input, "value")
        print(text)
        
        self.wait_to_click(self.apply_id)
        time.sleep(2)
        self.wait_for_element(self.result_table, 300)
        self.wait_for_element(self.report_content_id, 120)
        print("Report loaded successfully!")
        self.scroll_to_bottom()
        self.verify_users_in_the_group()
        for items in UserData.automation_group_users:
            count = self.get_text((By.XPATH, self.total_form_counts.format(items)))
            print(count)
            
            self.wait_to_click((By.XPATH, self.result_rows_names.format(items)))
            time.sleep(15)
            self.wait_for_element(self.submit_history_table_title)
            self.wait_for_element(self.result_table, 300)
            self.wait_for_element(self.report_content_id, 120)
            print("Report loaded successfully!")
            assert filter == self.get_selected_text(self.filter_dates_by), "Date Filter mismatched"
            print("Date Filter matched")
            assert UserData.reassign_cases_application == self.get_selected_text(
                self.application_dropdown), "Application mismatched"
            print("Application matched")
            assert list(UserData.reasign_modules_forms.keys())[1] == self.get_selected_text(
                self.module_dropdown), "Application mismatched"
            print("Application matched")
            assert UserData.reasign_modules_forms[list(UserData.reasign_modules_forms.keys())[1]][
                       0] == self.get_selected_text(
                self.form_dropdown), "Application mismatched"
            print("Application matched")
            assert date_string == self.get_attribute(self.date_input, "value"), "Date Range mismatched"
            print("Date Range matched")
            assert self.is_present((By.XPATH, self.filter_column_name.format(filter))), "Incorrect column present"
            print("Correct Column present")
            self.scroll_to_bottom()
            
            # info = self.get_text(self.submit_history_table_info)
            # print(info)
            # info = str(info).split(" ")
            # print("Total records: ", info[-2])
            # assert count == info[-2], "Form counts not matching"
            # print("Form Count matching")
            # if count == '0':
            #     assert self.is_present(self.empty_table)
            #     print("Correct value displayed")
            time.sleep(2)
            self.driver.back()

    def advanced_options(self):
        self.wait_to_click(self.sub_by_form_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.sub_by_form_TITLE in self.driver.title, "This is not the Worker Activity page."
        self.wait_for_element(self.apply_id, 100)
        self.verify_user_lookup_table()
        self.remove_default_users()
        self.send_keys(self.users_field, UserData.daily_form_groups[0])
        self.wait_to_click((By.XPATH, self.users_list_item.format(UserData.daily_form_groups[0])))
        
        self.wait_to_click(self.show_adv_options)
        assert self.is_selected(self.show_adv_options), "Show Advanced Options is not selected"
        print("Show Advanced Option is successfully selected")
        
        assert self.is_present(self.known_forms), "Known Forms option not present"
        assert self.is_present(self.unknown_forms), "Unknown Forms option not present"
        assert self.is_present(self.application_type_dropdown), "Application Type dropdown not present"
        active_apps, deleted_apps = self.known_forms_options()
        self.unknown_forms_options(active_apps, deleted_apps)
        self.wait_to_click(self.show_adv_options)
        assert not self.is_selected(self.show_adv_options), "Show Advanced Options is still selected"
        
        assert not self.is_visible_and_displayed(self.known_forms, 10), "Known Forms option still present"
        assert not self.is_visible_and_displayed(self.unknown_forms, 10), "Unknown Forms option still present"
        print("All Show Advanced Options are working correctly")

    def known_forms_options(self):
        if not self.is_selected(self.known_forms):
            self.wait_to_click(self.known_forms)
            assert self.is_selected(self.known_forms), "Known Forms radio button is not selected"
        else:
            assert self.is_selected(self.known_forms), "Known Forms radio button is not selected"

        self.verify_dropdown_options(self.application_type_dropdown, UserData.app_type_list)
        self.select_by_text(self.application_type_dropdown, UserData.app_type_list[0])
        
        assert not self.is_visible_and_displayed(self.application_dropdown, 10), "Application dropdown is still present"
        print("Application dropdown successfully disappeared after selecting option ", UserData.app_type_list[0])
        self.select_by_text(self.application_type_dropdown, UserData.app_type_list[2])
        
        assert self.is_present(self.application_dropdown), "Application dropdown is not present"
        list_app_active = self.get_all_dropdown_options(self.application_dropdown)
        for items in list_app_active[1:]:
            assert "[Deleted Application]" in items, "Not a Deleted Application option"
        print("All Deleted Application present")
        self.select_by_text(self.application_type_dropdown, UserData.app_type_list[1])
        
        assert self.is_present(self.application_dropdown), "Application dropdown is not present"
        list_app_deleted = self.get_all_dropdown_options(self.application_dropdown)
        for items in list_app_deleted[1:]:
            assert "[Deleted Application]" not in items, "Deleted Application is present in the dropdown"
        print("No Deleted Application present")
        self.select_application_and_forms(UserData.reassign_cases_application,
                                          list(UserData.reasign_modules_forms.keys())[1],
                                          UserData.reasign_modules_forms[
                                              list(UserData.reasign_modules_forms.keys())[1]][0])
        print("Correct Modules and Forms are present")
        return list_app_active, list_app_deleted

    def unknown_forms_options(self, active, deleted):
        if not self.is_selected(self.unknown_forms):
            self.wait_to_click(self.unknown_forms)
            assert self.is_selected(self.unknown_forms), "Unknown Forms radio button is not selected"
        else:
            assert self.is_selected(self.unknown_forms), "Unknown Forms radio button is not selected"

        self.wait_for_element(self.unknown_form_dropdown)
        print("Application dropdown successfully disappeared after selecting option ", UserData.app_type_list[0])
        list_app = self.get_all_dropdown_options(self.application_dropdown)
        for items in list_app[1:]:
            assert items not in active or items not in deleted, "Not an Unknown Application option"
        print("All Applications present are unknown")

    def generate_form_column_names(self, app, mod=None, forms=None):
        column_list = []
        if mod == None and forms == None:
            mod = list(UserData.reasign_modules_forms.keys())
            for m in mod:
                for f in list(UserData.reasign_modules_forms[m]):
                    string = app+" > "+m+" > "+f
                    column_list.append(string)
        elif mod !=None and forms == None:
            for f in list(UserData.reasign_modules_forms[mod]):
                string = app+" > "+mod+" > "+f
                column_list.append(string)
        else:
            string = app + " > " + mod + " > " + forms
            column_list.append(string)
        print(column_list)
        return column_list

    def form_column_verification(self, app, mod=None, form=None):
        self.wait_to_click(self.sub_by_form_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.sub_by_form_TITLE in self.driver.title, "This is not the Worker Activity page."
        self.verify_user_lookup_table()
        self.remove_default_users()
        self.send_keys(self.users_field, UserData.user_group)
        self.wait_to_click((By.XPATH, self.users_list_item.format(UserData.user_group)))
        
        self.select_by_text(self.application_dropdown, app)
        if mod == None and form == None:
            column_list = self.generate_form_column_names(app)
            self.select_by_text(self.application_dropdown, app)
        elif mod != None and form == None:
            column_list = self.generate_form_column_names(app, mod)
            self.select_by_text(self.application_dropdown, app)
            self.select_by_text(self.module_dropdown, mod)
        else:
            column_list = self.generate_form_column_names(app, mod, form)
            self.select_by_text(self.application_dropdown, app)
            self.select_by_text(self.module_dropdown, mod)
            self.select_by_text(self.form_dropdown, form)

        self.select_by_text(self.filter_dates_by, UserData.filter_dates_by[0])
        self.wait_to_click(self.date_input)
        self.wait_to_click((By.XPATH, self.date_range_type.format(UserData.date_range[0])))
        text = self.get_attribute(self.date_input, "value")
        print(text)
        
        self.wait_to_click(self.apply_id)
        time.sleep(2)
        self.wait_for_element(self.result_table, 300)
        self.wait_for_element(self.report_content_id, 120)
        print("Report loaded successfully!")
        self.scroll_to_bottom()
        self.verify_users_in_the_group()
        for items in column_list:
            assert self.is_present((By.XPATH, self.app_mod_form_column.format(items))), "Form Name Column not present: " + column_name

