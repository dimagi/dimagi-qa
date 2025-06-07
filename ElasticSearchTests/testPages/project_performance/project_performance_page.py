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


class ProjectPerformancePage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

        # Mobile Worker Reports
        self.reports_menu_id = (By.ID, "ProjectReportsTab")
        self.proj_perf_rep = (By.LINK_TEXT, "Project Performance")
        self.proj_perf_TITLE = "Project Performance - CommCare HQ"

        # Report Elements
        self.apply_id = (By.ID, "apply-filters")
        self.report_content_id = (By.ID, "report-content")

        self.low_perf_results = (By.XPATH, "(//table[contains(@id,'DataTables_Table')]/tbody/tr)[1]")
        self.low_perf_results_cells = (By.XPATH, "(//table[contains(@id,'DataTables_Table')])[1]/tbody/tr/td")
        self.low_perf_user_edit = (
            By.XPATH, "(//table[contains(@id,'DataTables_Table')]/tbody/tr/td[1]/a/div//a[.='Edit User Information'])[1]")
        self.low_perf_user_column = (
            By.XPATH, "(//table[contains(@id,'DataTables_Table')]/thead//th[.='Username'])[1]")
        self.low_perf_forms_submitted_column = (
            By.XPATH, "(//table[contains(@id,'DataTables_Table')]/thead//th[.='Change in Forms Submitted'])[1]")
        self.low_perf_last_month_column = (
            By.XPATH, "(//table[contains(@id,'DataTables_Table')]/thead//th[.='Last Month'])[1]")
        self.low_perf_this_month_column = (
            By.XPATH, "(//table[contains(@id,'DataTables_Table')]/thead//th[.='This Month'])[1]")
        self.low_perf_arrow_values = (
            By.XPATH, "(//table[contains(@id,'DataTables_Table')]/thead//th[.='This Month'])[1]")

        self.inactive_results = (By.XPATH, "(//table[contains(@id,'DataTables_Table')]/tbody/tr)[2]")
        self.inactive_results_cells = (By.XPATH, "(//table[contains(@id,'DataTables_Table')])[2]/tbody/tr/td")
        self.inactive_user_edit = (
            By.XPATH, "(//table[contains(@id,'DataTables_Table')]/tbody/tr/td[1]/a/div//a[.='Edit User Information'])[2]")
        self.inactive_user_column = (
            By.XPATH, "(//table[contains(@id,'DataTables_Table')]/thead//th[.='Username'])[2]")
        self.inactive_forms_submitted_column = (
            By.XPATH, "(//table[contains(@id,'DataTables_Table')]/thead//th[.='Change in Forms Submitted'])[2]")
        self.inactive_last_month_column = (
            By.XPATH, "(//table[contains(@id,'DataTables_Table')]/thead//th[.='Last Month'])[2]")
        self.inactive_this_month_column = (
            By.XPATH, "(//table[contains(@id,'DataTables_Table')]/thead//th[.='This Month'])[2]")

        self.high_perf_results = (By.XPATH, "(//table[contains(@id,'DataTables_Table')]/tbody/tr)[3]")
        self.high_perf_results_cells = (By.XPATH, "(//table[contains(@id,'DataTables_Table')])[3]/tbody/tr/td")
        self.high_perf_user_edit = (
            By.XPATH, "(//table[contains(@id,'DataTables_Table')]/tbody/tr/td[1]/a/div//a[.='Edit User Information'])[3]")
        self.high_perf_user_column = (
            By.XPATH, "(//table[contains(@id,'DataTables_Table')]/thead//th[.='Username'])[3]")
        self.high_perf_forms_submitted_column = (
            By.XPATH, "(//table[contains(@id,'DataTables_Table')]/thead//th[.='Change in Forms Submitted'])[3]")
        self.high_perf_last_month_column = (
            By.XPATH, "(//table[contains(@id,'DataTables_Table')]/thead//th[.='Last Month'])[3]")
        self.high_perf_this_month_column = (
            By.XPATH, "(//table[contains(@id,'DataTables_Table')]/thead//th[.='This Month'])[3]")

        self.down_arrows = (By.XPATH, "(//table[contains(@id,'DataTables_Table')]/tbody//td/span[@class='fa fa-chevron-down'])")
        self.up_arrows = (
        By.XPATH, "//table[contains(@id,'DataTables_Table')]/tbody//td/span[@class='fa fa-chevron-up']")

        self.up_arrows_iterables = "(//table[contains(@id,'DataTables_Table')]/tbody//td/span[@class='fa fa-chevron-up'])[{}]"
        self.down_arrows_iterables = "(//table[contains(@id,'DataTables_Table')]/tbody//td/span[@class='fa fa-chevron-down'])[{}]"

        self.group_field = (By.XPATH, "(//textarea[@class='select2-search__field'])[1]")
        self.remove_buttons = (By.XPATH, "//ul//button")
        self.user_remove_btn = (By.XPATH, "(//button[@class='select2-selection__choice__remove'])[last()]")
        self.custome_remove_btn = "//li/span[contains(.,'{}')]//preceding-sibling::button[@class='select2-selection__choice__remove']"
        self.user_from_list = "//li[contains(.,'{}')]"
        self.export_to_excel = (By.XPATH, "//a[@id='export-report-excel']")
        self.export_success = (By.XPATH,
                               "//span[.='Your requested Excel report will be sent to the email address defined in your account settings.']")
        self.user_column = (
        By.XPATH, "(//table[contains(@id,'DataTables_Table')]/tbody/tr/td[1]/a/div//a[.='Edit User Information']")
        self.active_cases_column = (
            By.XPATH, "(//thead/tr/th[@aria-controls='report_table_case_activity']/div[contains(.,'# Active Cases')])[1]")
        self.inactive_cases_column = (
            By.XPATH,
            "(//thead/tr/th[@aria-controls='report_table_case_activity']/div[contains(.,'# Inactive Cases')])[1]")

        self.users_list_item = "//ul[@role='listbox']/li[contains(.,'{}')]"
        self.users_list = (By.XPATH, "//ul[contains(@class,'select2-results__options')]/li")
        self.users_list_empty = (
        By.XPATH, "//ul[contains(@id,'select2-emw-bi-results')]/li[.='The results could not be loaded.']")

        self.column_names = "(//thead/tr/th[@aria-controls='report_table_case_activity']/div[@data-title='{}'])[{}]"
        self.column_group_names = "(//thead/tr/th//strong[.='{}'])[1]"
        self.user_names_column_list = "(//table[contains(@id,'DataTables_Table')]//tbody//td[1])[{}]"
        self.last_submission_column_list = (By.XPATH, "//table[@id='report_table_case_activity']//tbody//td[4]")
        self.result_table = (By.XPATH, "(//div[@id='report-content']//table//tbody//td[1])[1]")
        self.results_rows = (By.XPATH, "//tbody//td[not(contains(.,'No data'))]//parent::tr")
        self.result_rows_names = "//tbody/tr/td[1][contains(.,'{}')]"
        self.all_users_row_names = (By.XPATH, "//tfoot/td[contains(.,'All Users')]")
        self.hide_filters_options = (By.XPATH, "//a[.='Hide Filter Options']")
        self.show_filters_options = (By.XPATH, "//a[.='Show Filter Options']")
        self.user_sort = (
        By.XPATH, "(//text()[contains(.,'User')]//preceding-sibling::i[@class='icon-white fa dt-sort-icon'])[1]")
        self.active_cases_column_list = (By.XPATH, "//table[@id='report_table_case_activity']//tbody//td[7]")
        self.total_cases_shared_column_list = (By.XPATH, "//table[@id='report_table_case_activity']//tbody//td[8]")
        self.column_name_headers = "//table[@id='report_table_case_activity']//thead//th/div/div[contains(.,'{}')]"


        # Pagination
        self.page_list_dropdown =  "(//table[contains(@id,'DataTables_Table')])[{}]//following-sibling::div//select"
        self.table_info = "(//table[contains(@id,'DataTables_Table')])[{}]//following-sibling::div//div[@class='dataTables_info']"
        self.prev_page_button =  "(//table[contains(@id,'DataTables_Table')])[{}]//following-sibling::div//ul[@class='pagination']/li[@class='prev']/a"
        self.next_page_button =  "(//table[contains(@id,'DataTables_Table')])[{}]//following-sibling::div//ul[@class='pagination']/li[@class='next']/a"
        self.prev_page_button_disabled = "(//table[contains(@id,'DataTables_Table')])[{}]//following-sibling::div//ul[@class='pagination']/li[@class='prev disabled']/a"
        self.next_page_button_disabled = "(//table[contains(@id,'DataTables_Table')])[{}]//following-sibling::div//ul[@class='pagination']/li[@class='next disabled']/a"
        self.page_button = "(//table[contains(@id,'DataTables_Table')])[{}]//following-sibling::div//ul[@class='pagination']/li/a[.='{}']"
        self.pagination_list =  "(//table[contains(@id,'DataTables_Table')])[{}]//following-sibling::div//ul[@class='pagination']/li/a"

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
        self.case_created_column = (By.XPATH, "//table[@id='report_table_case_activity']//tbody//td[5]//a")
        self.case_created_title = (By.XPATH, "//table[@id='report_table_case_activity']//tbody//td[5]//span")
        self.case_list_table = (By.XPATH, "//table[@id='report_table_case_list']/tbody/tr/td[1]")
        self.case_list_table_title = (By.XPATH, "//h2[@class='panel-title'][contains(.,'Case List')]")
        self.case_list_table_info = (By.XPATH, "//div[@id='report_table_case_list_info']")
        self.case_list_page_dropdown = (By.XPATH, "//select[@name='report_table_case_list_length']")
        self.owner_column_list = (By.XPATH, "//tbody//td[3]")
        self.empty_table = (By.XPATH, "//tr/td[contains(.,'No data available to display.')]")

        # Email report
        self.email_report_btn = (By.XPATH, "//a[@id='email-report']")
        self.email_subject_field = (By.XPATH, "//input[@id='id_subject']")
        self.email_form_cancel_btn = (By.XPATH, "//input[@id='button-id-close']")
        self.send_email_btn = (By.XPATH, "//input[@id='submit-id-submit_btn']")
        self.email_success_message = (By.XPATH, "//*[.='Report successfully emailed']")
        self.additional_recipients = (By.XPATH, "//textarea[contains(@aria-describedby,'id_recipient_emails')]")
        self.reports_notes_field = (By.XPATH, "//textarea[@data-bind='value: notes']")



    def hide_filters(self):
        self.wait_to_click(self.proj_perf_rep)
        self.wait_for_element(self.hide_filters_options)
        self.click(self.hide_filters_options)
        
        assert not self.is_visible_and_displayed(self.group_field, 10), "Group or Locations field is still present"
        assert not self.is_visible_and_displayed(self.apply_id, 10), "Apply button is still present"
        assert not self.is_visible_and_displayed(self.favorite_button, 10), "Favorites button is still present"
        assert not self.is_visible_and_displayed(self.save_config_button, 10), "Save button is still present"
        assert self.is_present(self.show_filters_options), "Show Filters Options is not present"
        print("All filters are hidden!")

    def show_filters(self):
        self.wait_for_element(self.show_filters_options)
        self.click(self.show_filters_options)
        
        self.wait_for_element(self.group_field)
        self.wait_for_element(self.apply_id)
        self.wait_for_element(self.favorite_button)
        self.wait_for_element(self.save_config_button)
        assert self.is_present(self.hide_filters_options), "Show Filters Options is not present"
        print("All filters are shown!")

    def verify_proj_perf_page_fields(self):
        self.wait_to_click(self.proj_perf_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.proj_perf_TITLE in self.driver.title, "This is not the Project Performance page."
        self.wait_for_element(self.group_field)
        self.wait_for_element(self.apply_id)
        self.wait_for_element(self.favorite_button)
        self.wait_for_element(self.save_config_button)
        assert self.is_present(self.hide_filters_options), "Show Filters Options is not present"
        print("All filters are shown!")

    def verify_tables_columns(self):
        self.wait_to_click(self.proj_perf_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.proj_perf_TITLE in self.driver.title, "This is not the Project Performance page."
        self.wait_to_click(self.apply_id)
        time.sleep(2)
        self.wait_for_element(self.result_table, 300)
        self.wait_for_element(self.report_content_id, 120)
        print("Report loaded successfully!")
        self.scroll_to_element(self.result_table)
        time.sleep(2)
        assert self.is_present(self.low_perf_user_column), "User Column not present for Low Performance Table"
        assert self.is_present(self.low_perf_last_month_column), "Last Month Column not present for Low Performance Table"
        assert self.is_present(self.low_perf_this_month_column), "This Month Column not present for Low Performance Table"

        assert self.is_present(self.inactive_user_column), "User Column not present for Inactive Table"
        assert self.is_present(
            self.inactive_last_month_column), "Last Month Column not present for Inactive Table"
        assert self.is_present(
            self.inactive_this_month_column), "This Month Column not present for Inactive Table"

        assert self.is_present(self.high_perf_user_column), "User Column not present for High Performance Table"
        assert self.is_present(
            self.high_perf_last_month_column), "Last Month Column not present for High Performance Table"
        assert self.is_present(
            self.high_perf_this_month_column), "This Month Column not present for High Performance Table"
        down_arrow_lists = self.find_elements(self.down_arrows)
        print(len(down_arrow_lists))
        if len(down_arrow_lists)>0:
            for i in range(len(down_arrow_lists)):
                style = self.get_attribute((By.XPATH,self.down_arrows_iterables.format(i+1)), "style")
                print(style)
                assert UserData.arrows_code[0] in style or UserData.arrows_code[1] in style, "Arrow is not Red for Down arrow"
                print("Arrow is Red for Down arrow")

        up_arrow_lists = self.find_elements(self.up_arrows)
        len(up_arrow_lists)
        if len(up_arrow_lists) > 0:
            for i in range(len(up_arrow_lists)):
                style = self.get_attribute((By.XPATH,self.up_arrows_iterables.format(i+1)), "style")
                print(style)
                assert UserData.arrows_code[2] in style or UserData.arrows_code[3] in style, "Arrow is not Green for Up arrow"
                print("Arrow is Green for Up arrow")


    def verify_user_lookup_table(self):
        self.wait_to_click(self.group_field)
        
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


    def verify_users_in_the_group(self, cond="yes"):
        list = self.find_elements(self.results_rows)
        if len(list) > 0:
            if cond == "yes":
                for item in UserData.automation_group_users:
                    if self.is_present((By.XPATH, self.result_rows_names.format(
                        item))) == False:
                        print("No results for user: ", item)
                    else:
                        assert self.is_present((By.XPATH, self.result_rows_names.format(
                            item))), "Group user " + item + " is not present in results."
                        print("Group User " + item + " is present in results.")
            elif cond == "no":
                for item in UserData.automation_group_users:
                    assert not self.is_present((By.XPATH, self.result_rows_names.format(
                        item))), "Group user " + item + " is present in results."
                    print("Group User " + item + " is not present in results.")

    def proj_perf_pagination_list(self):
        self.wait_to_click(self.proj_perf_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.proj_perf_TITLE in self.driver.title, "This is not the Project Performance page."
        self.wait_to_click(self.apply_id)
        time.sleep(2)
        self.wait_for_element(self.result_table, 300)
        self.wait_for_element(self.report_content_id, 120)
        print("Report loaded successfully!")
        self.scroll_to_element(self.result_table)
        # For Low Performance table
        for i in range(0,3):
            pages = self.find_elements((By.XPATH,self.pagination_list.format(i+1)))
            pages_count = len(pages) - 2
            print("Total Pages: ", pages_count)
            first_page = pages[1].text
            last_page = pages[-2].text
            if pages_count > 1:
                assert self.is_present((By.XPATH, self.prev_page_button_disabled.format(i+1))), "Previous button is not disabled."
                print("Previous button disabled correctly")
                print("Clicking on page " + last_page)
                self.wait_to_click((By.XPATH, self.page_button.format(i+1, last_page)))
                time.sleep(15)
                assert self.is_present((By.XPATH, self.next_page_button_disabled.format(i+1))), "Next button is not disabled."
                print("Next button disabled correctly")
                time.sleep(2)
                print("Clicking on page " + first_page)
                self.wait_to_click((By.XPATH, self.page_button.format(i+1,first_page)))
                time.sleep(15)
                list1 = self.find_elements((By.XPATH, self.user_names_column_list.format(i+1)))
                list1_names = list()
                for item in list1:
                    list1_names.append(item.text)
                self.wait_to_click(self.next_page_button)
                time.sleep(2)
                list2 = self.find_elements((By.XPATH, self.user_names_column_list.format(i+1)))
                list2_names = list()
                for item in list2:
                    list2_names.append(item.text)
                print(list1_names, list2_names)
                assert list1_names != list2_names, "Both Pages have same values"
                print("Next button functioning correctly.")
                self.wait_to_click(self.prev_page_button)
                time.sleep(2)
                list3 = self.find_elements((By.XPATH, self.user_names_column_list.format(i+1)))
                list3_names = list()
                for item in list3:
                    list3_names.append(item.text)
                print(list1_names, list2_names, list3_names)
                assert list1_names == list3_names and list2_names != list3_names, "Page contains same data as the previous"
                print("Prev button functioning correctly.")
            else:
                print("Not enough users are present.")
                assert self.is_present((By.XPATH, self.prev_page_button_disabled.format(i+1)))
                assert self.is_present((By.XPATH, self.next_page_button_disabled.format(i+1)))
                print("Both Previous and Next Page buttons are disabled correctly.")

    def verify_pagination_dropdown(self):
        for i in range(0, 3):
            info = self.get_text((By.XPATH, self.table_info.format(i+1)))
            info = str(info).split(" ")
            print("Total records: ", info[-2])
            if int(info[-2]) > 10:
                for item in UserData.pagination:
                    self.select_by_value((By.XPATH,self.page_list_dropdown.format(i+1)), item)
                    time.sleep(2)
                    list = self.find_elements((By.XPATH, self.user_names_column_list.format(i+1)))
                    print(len(list))
                    if int(info[-2]) < int(item):
                        assert int(len(list)) == int(info[-2]), "List does not have all records."
                        print("Records displayed correctly for " + item)
                    elif int(info[-2]) >= int(item):
                        assert int(len(list)) == int(item), "List does not have all records."
                        print("Records displayed correctly for " + item)
                    else:
                        print("No records to display")
            else:
                print("Not enough Record to be displayed with Pagination List")


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

    def case_activity_search(self, date_range=UserData.date_range[0]):
        date_string = start_date = end_date = ''
        self.wait_to_click(self.case_activity_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.case_activity_TITLE in self.driver.title, "This is not theProject Performance page."
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

    def case_activity_search_custom_date(self):
        self.wait_to_click(self.case_activity_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.case_activity_TITLE in self.driver.title, "This is not theProject Performance page."
        self.select_by_text(self.filter_dates_by, UserData.filter_dates_by[0])
        date_string, start_date, end_date = self.get_custom_dates_past(0, 0, 5)
        self.clear(self.date_input)
        self.send_keys(self.date_input,  date_string+Keys.TAB)
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
        self.wait_to_click(self.case_activity_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.case_activity_TITLE in self.driver.title, "This is not theProject Performance page."
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

    def proj_perf_save_report(self):
        self.wait_to_click(self.proj_perf_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.proj_perf_TITLE in self.driver.title, "This is not the Worker Activity page."
        self.send_keys(self.group_field, UserData.user_group)
        self.wait_to_click((By.XPATH, self.users_list_item.format(UserData.user_group)))
        
        self.wait_to_click(self.apply_id)
        time.sleep(2)
        self.wait_for_element(self.result_table, 300)
        self.wait_for_element(self.report_content_id, 120)
        print("Report loaded successfully!")
        self.verify_users_in_the_group()
        time.sleep(2)
        report_name = "Saved Project Performance Report " + fetch_random_string()
        self.verify_favorite_empty(report_name)
        self.save_report_donot_save(report_name)
        self.save_report(report_name)
        self.wait_to_click(self.proj_perf_rep)
        self.wait_for_element(self.apply_id, 100)
        self.verify_favorite_created(report_name)
        time.sleep(2)
        self.verify_users_in_the_group()
        self.delete_saved_report(report_name)
        self.wait_to_click(self.proj_perf_rep)
        self.verify_favorite_empty(report_name)

    def verify_favorite_empty(self, report=None):
        self.wait_to_click(self.favorite_button)
        if report==None:
            self.wait_for_element(self.empty_fav_list)
        else:
            assert not self.is_visible_and_displayed((By.XPATH, self.saved_fav.format(report)),30), "Favorite is already Present"
        print("No Favorites yet.")

    def verify_favorite_created(self, report):
        self.wait_to_click(self.favorite_button)
        assert not self.is_visible_and_displayed(self.empty_fav_list, 10)
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
        time.sleep(2)
        assert self.is_present(self.name_field), "Name Field is not present"
        assert self.is_present(self.description_field), "Description field is not present"
        assert self.is_present(self.cancel_report_button), "Cancel button is not present"
        assert self.is_present(self.save_report_button)
        self.wait_to_clear_and_send_keys(self.name_field, report_name)
        self.wait_to_click(self.cancel_report_button)
        
        assert not self.is_visible_and_displayed(self.name_field, 10), "Save Report Form not closed"
        print("Save Report Form is closed")

    def save_report(self, report_name):
        self.wait_for_element(self.save_config_button)
        self.wait_to_click(self.save_config_button)
        assert self.is_present(self.name_field), "Name Field is not present"
        assert self.is_present(self.description_field), "Description field is not present"
        assert self.is_present(self.cancel_report_button), "Cancel button is not present"
        assert self.is_present(self.save_report_button)
        self.clear(self.name_field)
        self.wait_to_click(self.save_report_button)
        time.sleep(3)
        assert self.is_present(self.report_save_error), "Error not displayed"
        print("Error is correctly displayed")
        self.wait_to_clear_and_send_keys(self.name_field, report_name)
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

    def export_proj_perf_to_excel(self):
        self.wait_to_click(self.proj_perf_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.proj_perf_TITLE in self.driver.title, "This is not the Worker Activity page."
        self.send_keys(self.group_field, UserData.user_group)
        self.wait_to_click((By.XPATH, self.users_list_item.format(UserData.user_group)))
        
        self.wait_to_click(self.apply_id)
        time.sleep(2)
        self.wait_for_element(self.result_table, 300)
        self.wait_for_element(self.report_content_id, 120)
        print("Report loaded successfully!")
        self.verify_users_in_the_group()
        self.wait_for_element(self.low_perf_results)
        col_low = self.find_elements(self.low_perf_results_cells)
        list_low = []
        for c in col_low:
            list_low.append(c.text)
        print(list_low)
        col_inactive = self.find_elements(self.inactive_results_cells)
        list_inactive = []
        for c in col_inactive:
            list_inactive.append(c.text)
        print(list_inactive)
        col_high = self.find_elements(self.high_perf_results_cells)
        list_high = []
        for c in col_high:
            list_high.append(c.text)
        print(list_high)
        self.wait_to_click(self.export_to_excel)
        time.sleep(2)
        print("Export to excel successful")
        return list_low, list_inactive, list_high

    def compare_pp_with_excel(self, low, inactive, high):
        low = list(map(lambda x: x.replace('    ', '--'), low))
        inactive = list(map(lambda x: x.replace('    ', '--'), inactive))
        high = list(map(lambda x: x.replace('    ', '--'), high))
        web_data = [inactive, low, high]
        print("Low Performance: ",low)
        print("Inactive: ", inactive)
        print("High Performance: ", high)
        newest_file = latest_download_file()
        path = os.path.join(PathSettings.DOWNLOAD_PATH, newest_file)
        print(path)
        df_sheet_all = pd.read_excel(path, sheet_name=None, index_col=None)
        for i in range(len(UserData.proj_perf_excel_tabs))[1:]:
            data = df_sheet_all[UserData.proj_perf_excel_tabs[i]]
            print(UserData.proj_perf_excel_tabs[i], data)
            data['last_month'] = data['delta_last_month'].astype(str) +"--"+ data['last_month_forms'].astype(str)
            data['this_month'] = data['delta_this_month'].astype(str) +"--"+ data['this_month_forms'].astype(str)
            data = (data.loc[:, ~data.columns.isin(['user_id', 'last_month_forms','delta_last_month','this_month_forms','delta_this_month','is_performing'])])
            # Create an empty list
            row_list = []
            # Iterate over each row
            for index, rows in data.iterrows():
                # Create list for the current row
                my_list = [rows.username, rows.last_month, rows.this_month]
                # append the list to the final list
                row_list.extend(my_list)
                # Print the list
            print("Final list: ",row_list)
            if "No data available in table" in web_data[i-1]:
                assert len(row_list) == 0, "Data mismatch"
                print("Data is matching")
            else:
                assert row_list[0] == web_data[i-1] or row_list == web_data[i-1], "Data mismatch"
                print("Data is matching")


    def export_proj_perf_email(self):
        self.wait_to_click(self.proj_perf_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.proj_perf_TITLE in self.driver.title, "This is not the Worker Activity page."
        self.send_keys(self.group_field, UserData.user_group)
        self.wait_to_click((By.XPATH, self.users_list_item.format(UserData.user_group)))
        
        self.wait_to_click(self.apply_id)
        time.sleep(2)
        self.wait_for_element(self.result_table, 300)
        self.wait_for_element(self.report_content_id, 120)
        print("Report loaded successfully!")
        self.verify_users_in_the_group()
        self.wait_for_element(self.low_perf_results)
        col_low = self.find_elements(self.low_perf_results_cells)
        list_low = []
        for c in col_low:
            list_low.append(c.text)
        print(list_low)
        col_inactive = self.find_elements(self.inactive_results_cells)
        list_inactive = []
        for c in col_inactive:
            list_inactive.append(c.text)
        print(list_inactive)
        col_high = self.find_elements(self.high_perf_results_cells)
        list_high = []
        for c in col_high:
            list_high.append(c.text)
        print(list_high)
        subject = UserData.email_proj_perf_report
        self.email_report_form(subject)
        print("Export to excel successful")
        list_low = list(map(lambda x: x.replace('    ', '--'), list_low))
        list_inactive = list(map(lambda x: x.replace('    ', '--'), list_inactive))
        list_high = list(map(lambda x: x.replace('    ', '--'), list_high))
        web_data=[list_low+ list_inactive+ list_high]
        print("Sleeping for some time for the email to be sent")
        time.sleep(30)
        return web_data, subject

    def email_report_form_not_save(self, subject):
        self.wait_for_element(self.email_report_btn)
        self.wait_to_click(self.email_report_btn)
        self.wait_for_element(self.email_subject_field)
        assert self.is_present(self.additional_recipients), "Additional recipients field is not present"
        print("Additional recipients field is present")
        assert self.is_present(self.reports_notes_field), "Report notes field is not present"
        print("Report notes field is present")
        self.wait_to_clear_and_send_keys(self.email_subject_field, subject)
        self.wait_to_click(self.email_form_cancel_btn)
        print("Email report form closed properly")

    def email_report_form(self, subject):
        self.wait_for_element(self.email_report_btn)
        self.wait_to_click(self.email_report_btn)
        self.wait_for_element(self.email_subject_field)
        assert self.is_present(self.additional_recipients), "Additional recipients field is not present"
        print("Additional recipients field is present")
        assert self.is_present(self.reports_notes_field), "Report notes field is not present"
        print("Report notes field is present")
        self.wait_to_clear_and_send_keys(self.email_subject_field, subject)
        self.wait_to_click(self.send_email_btn)
        self.wait_for_element(self.email_success_message)
        print("Email report sent successfully")

    def compare_proj_perf_with_html_table(self, table_data, web_data):
        print("table data: ",table_data)
        print("Web data: ", web_data)
        assert len(web_data) == len(table_data), "Data in Both Email Body and Searched results do not match"
        print("Both Email Body and Searched results have same amount of data")
        for i in range(len(table_data)):
            print("Comparing ", html.unescape(str(table_data[i])), " with ", str(web_data[i]))
            assert html.unescape(str(table_data[i])) == str(web_data[i]), "Cpmparision failed for " + table_data[i] + " and " + \
                                                                    web_data[i]

    def proj_perf_group_selection(self):
        self.wait_to_click(self.proj_perf_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.proj_perf_TITLE in self.driver.title, "This is not the Worker Activity page."
        self.send_keys(self.group_field, UserData.user_group)
        self.wait_to_click((By.XPATH, self.users_list_item.format(UserData.user_group)))
        
        self.wait_to_click(self.apply_id)
        self.wait_for_element(self.report_content_id, 120)
        print("Report loaded successfully!")
        self.scroll_to_bottom()
        self.verify_users_in_the_group()
        self.wait_to_click((By.XPATH, self.custome_remove_btn.format(UserData.user_group)))
        
        assert not self.is_present((By.XPATH, self.custome_remove_btn.format(UserData.user_group))), "Group still present"
        print("Group removed successfully")
        self.send_keys(self.group_field, UserData.location)
        self.wait_to_click((By.XPATH, self.users_list_item.format(UserData.location)))
        
        self.wait_to_click(self.apply_id)
        self.wait_for_element(self.report_content_id, 120)
        print("Report loaded successfully!")
        self.scroll_to_bottom()
        self.verify_users_in_the_group("no")
        self.wait_to_click((By.XPATH, self.custome_remove_btn.format(UserData.location)))
        
        assert not self.is_present(
            (By.XPATH, self.custome_remove_btn.format(UserData.location))), "Location still present"
        print("Location removed successfully")
        self.send_keys(self.group_field, UserData.user_group)
        self.wait_to_click((By.XPATH, self.users_list_item.format(UserData.user_group)))
        
        self.send_keys(self.group_field, UserData.location)
        self.wait_to_click((By.XPATH, self.users_list_item.format(UserData.location)))
        self.wait_to_click(self.apply_id)
        self.wait_for_element(self.report_content_id, 120)
        print("Report loaded successfully!")
        assert self.is_present((By.XPATH, self.custome_remove_btn.format(UserData.user_group))), "Group not present"
        assert self.is_present((By.XPATH, self.custome_remove_btn.format(UserData.location))), "Location not present"
        print("Multiple options selected successfully")


    def case_activity_users_deactivated(self):
        self.wait_to_click(self.case_activity_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.case_activity_TITLE in self.driver.title, "This is not the Worker Activity page."
        self.wait_to_click(self.remove_deactive_worker)
        assert not self.is_present(self.remove_deactive_worker), "Deactivated Mobile Worker is still not removed"
        print("Deactivated Mobile Worker is removed successfully")
        self.reload_page()
        self.wait_for_element(self.apply_id, 100)
        self.verify_user_lookup_table()
        self.remove_default_users()
        self.send_keys(self.users_field, UserData.daily_form_groups[1])
        self.wait_to_click((By.XPATH, self.users_list_item.format(UserData.daily_form_groups[1])))
        
        self.select_by_text(self.case_type_dropdown, UserData.case_reassign)
        
        self.wait_to_click(self.apply_id)
        time.sleep(2)
        self.wait_for_element(self.result_table, 300)
        self.wait_for_element(self.report_content_id, 120)
        print("Report loaded successfully!")
        self.select_by_value(self.page_list_dropdown, UserData.pagination[3])
        time.sleep(2)
        assert self.is_present((By.XPATH, self.result_rows_names.format(UserData.deactivated_user))), "Deactivated user " + UserData.deactivated_user + " is not present in the Deactivated worker list."
        print("All Deactivated users are present")

    def user_data_verify(self):
        self.wait_to_click(self.case_activity_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.case_activity_TITLE in self.driver.title, "This is not the Worker Activity page."
        self.verify_user_lookup_table()
        self.remove_default_users()
        self.send_keys(self.users_field, UserData.user_group)
        self.wait_to_click((By.XPATH, self.users_list_item.format(UserData.user_group)))
        
        self.select_by_text(self.case_type_dropdown, UserData.case_reassign)
        
        self.wait_to_click(self.apply_id)
        time.sleep(2)
        self.wait_for_element(self.result_table, 300)
        self.wait_for_element(self.report_content_id, 120)
        print("Report loaded successfully!")
        self.scroll_to_bottom()
        self.verify_users_in_the_group()
        for items in UserData.automation_group_users:
            self.wait_to_click((By.PARTIAL_LINK_TEXT, items))
            time.sleep(15)
            self.wait_for_element(self.case_list_table_title)
            self.wait_for_element(self.result_table, 300)
            self.wait_for_element(self.report_content_id, 120)
            print("Report loaded successfully!")
            self.scroll_to_bottom()
            
            owner_list = self.find_elements(self.owner_column_list)
            print(len(owner_list))
            if len(owner_list)>1:
                for owner in owner_list:
                    text = owner.text
                    assert items in text or text in UserData.user_group, "Owner does not match"
                    print("Owner matching")
            time.sleep(2)
            self.driver.back()
            
            self.driver.back()



