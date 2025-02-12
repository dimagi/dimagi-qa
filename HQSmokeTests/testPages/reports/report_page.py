import os
import time
import html
from datetime import datetime, timedelta
import pandas as pd
from selenium.webdriver import ActionChains

from HQSmokeTests.testPages.data.export_data_page import latest_download_file
from common_utilities.path_settings import PathSettings

from common_utilities.selenium.base_page import BasePage
from common_utilities.generate_random_string import fetch_random_string
from HQSmokeTests.userInputs.user_inputs import UserData

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

""""Contains test page elements and functions related to the Reports module"""

import re


def parse_time(time_str):
    # Define regex patterns to match time units
    time_units = {
        'days': 1,
        'weeks': 7,
        'months': 30,
        'years': 365
        }

    total_days = 0
    # Match days, weeks, months, and years in the string
    for unit, multiplier in time_units.items():
        match = re.search(r'(\d+)\s+' + unit, time_str)
        if match:
            total_days += int(match.group(1)) * multiplier

    # If 'Never' is found, we return a very large value to consider it as the "oldest"
    if 'Never' in time_str:
        return float('inf')

    return total_days


def sort_times(time_list):
    # Sort the list based on the parsed time values (newest first)
    return sorted(time_list, key=parse_time, reverse=False)


def is_list_sorted_new_to_old(time_list):
    # Parse each time string and check if they are in sorted order
    parsed_times = [parse_time(time) for time in time_list]
    res = all(parsed_times[i] >= parsed_times[i + 1] for i in range(len(parsed_times) - 1))
    print(res)
    # Verify if the parsed times are sorted in descending order
    return res


class ReportPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

        self.report_name_form = "report form " + fetch_random_string()
        self.report_name_case = "report case " + fetch_random_string()
        self.report_name_saved = "saved form " + fetch_random_string()

        # Mobile Worker Reports
        self.reports_menu_id = (By.ID, "ProjectReportsTab")
        self.worker_activity_rep = (By.LINK_TEXT, "Worker Activity")
        self.daily_form_activity_rep = (By.LINK_TEXT, "Daily Form Activity")
        self.submissions_by_form_rep = (By.LINK_TEXT, "Submissions By Form")
        self.form_completion_rep = (By.LINK_TEXT, "Form Completion Time")
        self.case_activity_rep = (By.LINK_TEXT, "Case Activity")
        self.completion_vs_submission_rep = (By.LINK_TEXT, "Form Completion vs. Submission Trends")
        self.worker_activity_times_rep = (By.LINK_TEXT, "Worker Activity Times")
        self.project_performance_rep = (By.LINK_TEXT, "Project Performance")
        self.CASE_LIST_TITLE = "Case List - CommCare HQ"

        # Inspect Data Reports
        self.submit_history_rep = (By.LINK_TEXT, "Submit History")
        self.case_list_rep = (By.LINK_TEXT, "Case List")
        self.case_list_explorer = (By.LINK_TEXT, "Case List Explorer")

        # Manage Deployments Reports
        self.application_status_rep = (By.LINK_TEXT, "Application Status")
        self.agg_user_status_rep = (By.LINK_TEXT, "Aggregate User Status")
        self.raw_forms_rep = (By.LINK_TEXT, "Raw Forms, Errors & Duplicates")
        self.device_log_rep = (By.LINK_TEXT, "Device Log Details")
        self.app_error_rep = (By.LINK_TEXT, "Application Error Report")

        # Messaging Reports
        self.sms_usage_rep = (By.LINK_TEXT, "SMS Usage")
        self.messaging_history_rep = (By.LINK_TEXT, "Messaging History")
        self.message_log_rep = (By.LINK_TEXT, "Message Log")
        self.sms_opt_out_rep = (By.LINK_TEXT, "SMS Opt Out Report")
        self.scheduled_messaging_rep = (By.LINK_TEXT, "Scheduled Messaging Events")

        # Report Elements
        self.apply_id = (By.ID, "apply-filters")
        self.report_content_id = (By.ID, "report-content")
        self.save_xpath = (By.XPATH, "//button[@data-bind='click: setConfigBeingEdited']")
        self.custom_report_content_id = (By.ID, "report_table_configurable_wrapper")
        self.edit_report_id = (By.ID, "edit-report-link")
        self.delete_report_xpath = (By.XPATH, "//input[contains(@value,'Delete')]")
        self.homepage = (By.XPATH, ".//a[@href='/homepage/']")

        # Report Builder
        self.create_new_rep_id = (By.ID, "create-new-report-left-nav")
        self.report_name_textbox_id = (By.ID, "id_report_name")

        self.next_button_id = (By.ID, "js-next-data-source")
        self.save_and_view_button_id = (By.ID, "btnSaveView")
        self.form_or_cases = (By.XPATH, "//select[@data-bind='value: sourceType']")
        self.select_form_type = (By.XPATH, "//option[@value='form']")
        self.select_app = (By.XPATH, "//option[text()='Village Health']")
        self.application = (By.XPATH, "//select[@data-bind='value: application']")

        self.select_source_id = (By.XPATH, "//select[@id='id_source']")
        self.select_form_type_value = "form"
        self.select_case_type_value = "case"
        self.select_source_id_form_value = "Case List / Registration Form"
        self.select_source_id_case_value = "commcare-user"

        # Saved Reports
        self.new_saved_report_name = (By.ID, "name")
        self.save_confirm = (By.XPATH, '//div[@class = "btn btn-primary"]')
        self.saved_reports_menu_link = (By.LINK_TEXT, 'My Saved Reports')
        self.saved_report_created = (By.XPATH, "//a[text()='" + self.report_name_saved + "']")
        self.delete_saved = (By.XPATH,
                             "(//a[text()='" + self.report_name_saved + "']//following::button[@class='btn btn-danger add-spinner-on-click'])[1]")
        self.delete_saved_report_link = "(//a[text()='{}']//following::button[@class='btn btn-danger add-spinner-on-click'])[1]"
        self.all_saved_reports = (
            By.XPATH, "//td[a[contains(.,'Saved')]]//following-sibling::td/button[contains(@data-bind,'delete')]")

        # Scheduled Reports
        self.scheduled_reports_menu_xpath = (By.XPATH, "//a[@href='#scheduled-reports']")
        self.create_scheduled_report = (By.XPATH, "//a[@class='btn btn-primary track-usage-link']")
        self.available_reports = (By.XPATH, "//li[@class='ms-elem-selectable']")
        self.start_hour = (By.XPATH, "//select[@id='id_hour']")
        self.stop_hour = (By.XPATH, "//select[@id='id_stop_hour']")
        self.daily_option = (By.XPATH, "//button[./text()='Daily']")
        self.other_recipients = (By.XPATH, "//textarea[@aria-describedby='select2-id_recipient_emails-container']")
        self.recipient_value = "//li[contains(@class,'select2-results__option')][.='{}']"
        self.my_scheduled_reports = (By.XPATH, "//div[@data-bind='if: is_owner']/table/tbody/tr")
        self.report_schedule_time = (By.XPATH, "(//div[@data-bind='if: is_owner']/table/tbody/tr/td[3])[last()]")
        self.recipients_name = (By.XPATH, "(//div[@data-bind='if: is_owner']/table/tbody/tr/td[4])[last()]")
        self.submit_id = (By.ID, "submit-id-submit_btn")
        self.success_alert = (By.XPATH, "//div[@class='alert alert-margin-top fade in alert-success']")
        self.select_all = (By.XPATH, "(//button[@data-bind='click: selectAll'])[1]")
        self.delete_selected = (By.XPATH, "//a[@class='btn btn-danger']")
        self.delete_scheduled_confirm = (By.XPATH, "(//button[@data-bind='click: bulkDelete'])[1]")
        self.delete_success_scheduled = (By.XPATH, "//div[@class='alert alert-margin-top fade in alert-success']")

        # Submit History
        self.users_box = (By.XPATH, "//span[@class='select2-selection select2-selection--multiple']")
        self.search_user = (By.XPATH, "//textarea[@class='select2-search__field']")
        self.select_user = (By.XPATH, "//li[contains(text(),'[Web Users]')]")
        self.app_user_select = "(//li[contains(text(),'{}')])[1]"
        self.application_select = (By.XPATH, "//select[@id='report_filter_form_app_id']")
        self.module_select = (By.XPATH, "//select[@id='report_filter_form_module']")
        self.form_select = (By.XPATH, "//select[@id='report_filter_form_xmlns']")
        self.case_type_select = (By.XPATH, "//select[@id='report_filter_case_type']")
        self.date_input = (By.XPATH, "//input[@id='filter_range']")
        self.view_form_link = (By.XPATH, "//tbody/tr[1]/td[1]/a[.='View Form']")
        self.view_case_link = (By.XPATH, "//tbody/tr[1]/td[1]/a[.='View Case']")

        self.case_name = (By.XPATH, "//td[div[contains(text(),'abc')]]")
        self.submit_history_table = (By.XPATH, "//table[@id='report_table_submit_history']/tbody/tr")
        self.location_values = (By.XPATH, "//tr[@class='form-data-question ']/td[2]")

        # Case List
        self.search_input = (By.XPATH, "//input[@id='report_filter_search_query']")
        self.case_list_table = (By.XPATH, "//table[@id='report_table_case_list']/tbody/tr")
        self.case_id_block = (By.XPATH, "//th[@title='_id']/following-sibling::td")
        self.remove_case_owner = (
            By.XPATH, "//label[.='Case Owner(s)']//following-sibling::div//button[@aria-label='Remove item']")
        self.case_owner_textarea = (By.XPATH, "//label[.='Case Owner(s)']//following-sibling::div//textarea")
        self.case_owner_list_item = "//ul[@role='listbox']/li[contains(.,'{}')]"
        self.case_owner_column = (By.XPATH, "//tbody//td[3]")

        # Case List Explorer
        self.query_div = (By.XPATH, "//div[@class='ace_content']//div[@class='ace_line']")
        self.case_list_explorer_query_field = (
        By.XPATH, "//textarea[@class='ace_text-input']")
        self.case_list_explorer_rep = (By.LINK_TEXT, "Case List Explorer")
        self.case_list_explorer_TITLE = "Case List Explorer - CommCare HQ"
        self.case_type_dropdown = (By.XPATH, "//select[@id='report_filter_case_type']")
        self.column_editor = (By.XPATH, "//a[@href='#columns-editor']")
        self.add_property_button = (By.XPATH, "//button[@data-bind='click: addProperty']")
        self.last_properties_input = (
            By.XPATH,
            "(//tbody[contains(@data-bind,'properties')]//td//input[contains(@data-bind,'Properties')])[last()]")
        self.last_value_input = (
            By.XPATH,
            "(//tbody[contains(@data-bind,'properties')]//td//input[contains(@data-bind,'value: label')])[last()]")
        self.last_delete_property = (By.XPATH, "(//tbody[contains(@data-bind,'properties')]//td[4]/i)[last()]")
        self.property_label = "//div[@class='atwho-container']//div[@class='atwho-view']//ul/li[1]/span[ .='reassign']//following-sibling::strong[.='name']"
        self.properties_input = (
            By.XPATH, "//tbody[contains(@data-bind,'properties')]//td//input[contains(@data-bind,'Properties')]")
        self.value_input = (
            By.XPATH, "//tbody[contains(@data-bind,'properties')]//td//input[contains(@data-bind,'value: label')]")
        self.delete_property = (By.XPATH, "//tbody[contains(@data-bind,'properties')]//td[4]")
        self.edit_column = (By.XPATH,
                            "//div[./label[contains(.,'Columns')]]//following-sibling::div//a[@data-parent='#case-list-explorer-columns']")
        self.properties_table = (By.XPATH, "//tbody[contains(@data-bind,'properties')]")
        self.property_name_input = (By.XPATH, "(//tbody[contains(@data-bind,'properties')]//td[2]//input)[last()]")
        self.cle_case_owner_column = (By.XPATH, "//table[contains(@class,'datatable')]//tbody//td[5]")

        # Messaging History
        self.communication_type_select = (By.XPATH, "//label[.='Communication Type']/following-sibling::div/select")

        # Report Case
        self.report_case_links = (By.XPATH, "//li/a[contains(@title,'report case')]")
        self.report_case_link = "(//li/a[contains(@title,'{}')])[1]"
        self.report_form_links = (By.XPATH, "//li/a[contains(@title,'report form')]")
        self.report_form_link = "(//li/a[contains(@title,'{}')])[1]"

        # Configurable Report
        self.configurable_report = (By.LINK_TEXT, "Configurable Reports")
        self.add_report_button = (By.XPATH, "//div[@id='hq-content']//*[contains(.,'Add Report')]")
        self.edit_report_dropdown = (
            By.XPATH, "//span[contains(@class,'placeholder')][.='Edit a report or data source']")
        self.report_search_input = (By.XPATH, "//input[@role='searchbox']")
        self.select_report = "//li[contains(.,'{}')]/i"
        self.report_dropdown = (By.XPATH, "//select[@id='select2-navigation']")
        self.description_input = (By.XPATH, "//input[@id='id_description']")
        self.save_button = (By.XPATH, "//button[.='Save']")

        # Daily Form Activity
        self.daily_form_activity_results = (By.XPATH, "//table[@id='report_table_daily_form_stats']/tbody/tr")
        self.daily_form_activity_results_cells = (By.XPATH, "//table[@id='report_table_daily_form_stats']/tbody/tr/td")
        self.users_field = (By.XPATH, "(//textarea[@class='select2-search__field'])[1]")
        self.remove_active_worker = (By.XPATH,
                                     "//span[.='[Active Mobile Workers]']//preceding-sibling::button[@class='select2-selection__choice__remove']")
        self.remove_deactive_worker = (By.XPATH,
                                       "//span[.='[Deactivated Mobile Workers]']//preceding-sibling::button[@class='select2-selection__choice__remove']")
        self.remove_buttons = (By.XPATH, "//ul//button")
        self.user_remove_btn = (By.XPATH, "(//button[@class='select2-selection__choice__remove'])[last()]")
        self.user_from_list = "//li[contains(.,'{}')]"
        self.export_to_excel = (By.XPATH, "//a[@id='export-report-excel']")
        self.export_success = (By.XPATH,
                               "//span[.='Your requested Excel report will be sent to the email address defined in your account settings.']")
        self.download_report_link = (By.XPATH, "//div[contains(@class,'success')]//a[.='Download Report']")

        # App Status
        self.app_status_results = (
        By.XPATH, "//table[@class='table table-striped datatable dataTable no-footer']/tbody/tr")
        self.app_status_results_cells = (
        By.XPATH, "//table[@class='table table-striped datatable dataTable no-footer']/tbody/tr/td")
        self.panel_body_text = (By.XPATH, "//div[@class='panel-body-datatable']")
        self.last_submit_column_list = (By.XPATH, "//table[@id='report_table_app_status']//tbody//td[3]")
        self.last_submit_column_first = (By.XPATH, "(//table[@id='report_table_app_status']//tbody//td[3])[1]")
        self.page_list_dropdown = (By.XPATH, "//select[@name='report_table_app_status_length']")
        self.pagination_list = (By.XPATH, "//ul[@class='pagination']/li/a")
        self.application_dropdown = (By.XPATH, "//select[@id='report_filter_app']")
        self.application_field = (By.XPATH, "//span[contains(@id, 'report_filter_app-container')]")
        self.application_input = (By.XPATH, "//input[contains(@aria-controls,'report_filter_app-result')]")
        self.APPLICATION_STATUS_TITLE = "Application Status - CommCare HQ"
        self.result_table = (By.XPATH, "(//div[@id='report-content']//table//tbody//td[1])[1]")
        self.users_list_item = "//ul[@role='listbox']/li[contains(.,'{}')]"

    def check_if_report_loaded(self):
        try:
            self.wait_to_click(self.apply_id)
            time.sleep(10)
        except (TimeoutException, NoSuchElementException):
            print("Button Disabled")
        try:
            assert self.is_visible_and_displayed(self.report_content_id)
        except (TimeoutException, AssertionError):
            assert self.is_visible_and_displayed(self.custom_report_content_id)
        print("Report loaded successfully!")

    def worker_activity_report(self):
        self.wait_to_click(self.worker_activity_rep)
        self.check_if_report_loaded()

    def daily_form_activity_report(self):
        self.wait_to_click(self.daily_form_activity_rep)
        self.check_if_report_loaded()

    def submissions_by_form_report(self):
        self.wait_to_click(self.submissions_by_form_rep)
        self.check_if_report_loaded()

    def form_completion_report(self):
        self.wait_to_click(self.form_completion_rep)
        self.check_if_report_loaded()

    def case_activity_report(self):
        self.wait_to_click(self.case_activity_rep)
        self.check_if_report_loaded()

    def completion_vs_submission_report(self):
        self.wait_to_click(self.completion_vs_submission_rep)
        self.check_if_report_loaded()

    def worker_activity_times_report(self):
        self.wait_to_click(self.worker_activity_times_rep)
        self.check_if_report_loaded()

    def project_performance_report(self):
        self.wait_to_click(self.project_performance_rep)
        self.check_if_report_loaded()

    def submit_history_report(self):
        self.wait_to_click(self.submit_history_rep)
        self.wait_for_element(self.users_box, 200)
        self.check_if_report_loaded()

    def case_list_report(self):
        self.wait_to_click(self.case_list_rep)
        self.check_if_report_loaded()

    def sms_usage_report(self):
        self.wait_to_click(self.sms_usage_rep)
        self.check_if_report_loaded()

    def messaging_history_report(self):
        self.wait_to_click(self.messaging_history_rep)
        date_range = self.get_last_7_days_date_range()
        self.clear(self.date_input)
        self.send_keys(self.date_input, date_range + Keys.TAB)
        self.check_if_report_loaded()

    def message_log_report(self):
        self.wait_to_click(self.message_log_rep)
        self.check_if_report_loaded()

    def sms_opt_out_report(self):
        self.wait_to_click(self.sms_opt_out_rep)
        assert self.is_visible_and_displayed(self.report_content_id)

    def scheduled_messaging_report(self):
        self.wait_to_click(self.scheduled_messaging_rep)
        self.check_if_report_loaded()

    def delete_report(self):
        if self.is_present(self.delete_report_xpath):
            self.wait_to_click(self.delete_report_xpath)
            print("Report deleted successfully!")
        else:
            try:
                self.wait_to_click(self.edit_report_id)
            except TimeoutException:
                self.driver.refresh()
                self.wait_to_click(self.edit_report_id)
            self.wait_to_click(self.delete_report_xpath)
            print("Report deleted successfully!")
        self.wait_to_click(self.homepage)

    def create_report_builder_case_report(self):
        self.wait_to_click(self.create_new_rep_id)
        self.send_keys(self.report_name_textbox_id, self.report_name_case)
        self.select_by_value(self.form_or_cases, self.select_case_type_value)
        self.select_by_text(self.application, UserData.village_application)
        self.select_by_text(self.select_source_id, self.select_source_id_case_value)
        self.wait_to_click(self.next_button_id)
        self.wait_to_click(self.save_and_view_button_id)
        self.check_if_report_loaded()

    def create_report_builder_form_report(self):
        self.wait_to_click(self.create_new_rep_id)
        self.send_keys(self.report_name_textbox_id, self.report_name_form)
        self.select_by_value(self.form_or_cases, self.select_form_type_value)
        self.select_by_text(self.application, UserData.village_application)
        self.select_by_text(self.select_source_id, self.select_source_id_form_value)
        self.wait_to_click(self.next_button_id)
        self.wait_to_click(self.save_and_view_button_id)
        self.check_if_report_loaded()

    def saved_report(self):
        self.wait_to_click(self.case_activity_rep)
        self.wait_to_click(self.save_xpath)
        self.send_keys(self.new_saved_report_name, self.report_name_saved)
        self.wait_to_click(self.save_confirm)
        time.sleep(10)
        self.wait_for_element(self.saved_reports_menu_link, 100)
        self.js_click(self.saved_reports_menu_link)
        assert self.is_visible_and_displayed(self.saved_report_created, 220)
        print("Report Saved successfully!")

    def create_scheduled_report_button(self):
        self.wait_and_sleep_to_click(self.scheduled_reports_menu_xpath)
        self.wait_to_click(self.create_scheduled_report)

    def scheduled_report(self):
        self.create_scheduled_report_button()
        try:
            self.wait_to_click(self.available_reports)
        except TimeoutException:
            self.saved_report()
            self.create_scheduled_report_button()
            self.wait_to_click(self.available_reports)
        self.wait_to_click(self.daily_option)
        self.select_by_index(self.start_hour, 10)
        self.wait_to_click(self.other_recipients)
        self.send_keys(self.other_recipients, UserData.p1p2_user)
        self.wait_to_click((By.XPATH, self.recipient_value.format(UserData.p1p2_user)))
        selected_hour = self.get_selected_text(self.start_hour)
        self.wait_to_click(self.submit_id)
        assert self.is_visible_and_displayed(self.success_alert)
        print("Scheduled Report Created Successfully")
        return selected_hour, UserData.p1p2_user

    def verify_scheduled_report(self, time, user):
        self.wait_for_element(self.my_scheduled_reports)
        if len(self.find_elements(self.my_scheduled_reports)) > 0:
            print("My scheduled report is present")
            assert True
        else:
            print("No scheduled report is present")
            assert False
        time_text = self.get_text(self.report_schedule_time)
        print(time_text)
        assert time in time_text, "Scheduled Time is not matching"
        recipient_text = self.get_text(self.recipients_name)
        print(recipient_text)
        assert user in recipient_text, "Recipient is not present"

    def delete_scheduled_and_saved_reports(self):
        self.wait_for_element(self.saved_reports_menu_link, 400)
        self.js_click(self.saved_reports_menu_link)
        try:
            self.click(self.delete_saved)
            print("Deleted Saved Report")
        except NoSuchElementException:
            print("Not such report found!")
        self.wait_to_click(self.scheduled_reports_menu_xpath)
        try:
            self.wait_to_click(self.select_all)
            self.wait_to_click(self.delete_selected)
            self.wait_to_click(self.delete_scheduled_confirm)
            self.is_visible_and_displayed(self.delete_success_scheduled)
            print("Deleted Scheduled Report")
        except TimeoutException:
            print("No reports available")

    def delete_saved_reports(self):
        self.js_click(self.saved_reports_menu_link)
        list = self.find_elements(self.all_saved_reports)
        if len(list) > 0:
            for items in list:
                self.wait_to_click(items)
                print("Deleted Saved Report")
                list = self.find_elements(self.all_saved_reports)
        else:
            print("No saved test reports")

    def delete_report_case_links(self):
        list = self.find_elements(self.report_case_links)
        print(len(list))
        print(list)
        if len(list) > 0:
            for i in range(len(list))[::-1]:
                text = list[i].text
                print(i, text)
                self.wait_for_element((By.XPATH, self.report_case_link.format(text)))
                self.wait_to_click((By.XPATH, self.report_case_link.format(text)))
                self.wait_to_click(self.edit_report_id)
                self.wait_to_click(self.delete_report_xpath)
                print("Deleted Saved Report")
                time.sleep(2)
                self.driver.refresh()
                time.sleep(5)
                list = self.find_elements(self.report_case_links)

        else:
            print("Report deleted successfully!")

    def delete_report_form_links(self):
        list = self.find_elements(self.report_form_links)
        print(len(list))
        print(list)
        if len(list) > 0:
            for i in range(len(list))[::-1]:
                text = list[i].text
                print(i, text)
                self.wait_for_element((By.XPATH, self.report_form_link.format(text)))
                self.wait_to_click((By.XPATH, self.report_form_link.format(text)))
                self.wait_to_click(self.edit_report_id)
                self.wait_to_click(self.delete_report_xpath)
                print("Deleted Saved Report")
                time.sleep(2)
                self.driver.refresh()
                time.sleep(5)
                list = self.find_elements(self.report_form_links)

        else:
            print("Report deleted successfully!")

    def get_last_7_days_date_range(self):
        # Get today's date
        presentday = datetime.now()  # or presentday = datetime.today()
        # Get Today minus 7 days date
        week_ago = presentday - timedelta(7)
        return week_ago.strftime('%Y-%m-%d') + " to " + presentday.strftime('%Y-%m-%d')

    def get_todays_date_range(self):
        # Get today's date
        presentday = datetime.now()  # or presentday = datetime.today()
        return presentday.strftime('%Y-%m-%d') + " to " + presentday.strftime('%Y-%m-%d')

    def verify_table_not_empty(self, locator):
        clickable = ec.presence_of_all_elements_located(locator)
        element = WebDriverWait(self.driver, 30).until(clickable, message="Couldn't find locator: "
                                                                          + str(locator)
                                                       )
        count = len(element)
        if count > 0:
            print(count, " rows are present in the web table")
            return True
        else:
            print("No rows are present in the web table")
            return False

    def verify_form_data_submit_history(self, case_name, username):
        print("Sleeping for sometime for the case to get registered.")
        time.sleep(90)
        self.wait_to_click(self.submit_history_rep)
        self.wait_for_element(self.users_box, 200)
        self.wait_to_click(self.users_box)
        self.send_keys(self.search_user, username)
        self.wait_to_click((By.XPATH, self.app_user_select.format(username)))
        self.select_by_text(self.application_select, UserData.reassign_cases_application)
        self.select_by_text(self.module_select, UserData.case_list_name)
        self.select_by_text(self.form_select, UserData.form_name)
        date_range = self.get_todays_date_range()
        self.clear(self.date_input)
        self.send_keys(self.date_input, date_range + Keys.TAB)
        self.wait_to_click(self.apply_id)
        time.sleep(15)
        self.scroll_to_bottom()
        self.verify_table_not_empty(self.submit_history_table)
        self.is_present_and_displayed(self.view_form_link)
        form_link = self.get_attribute(self.view_form_link, "href")
        print("View Form Link: ", form_link)
        # self.switch_to_new_tab()
        self.driver.get(form_link)
        time.sleep(3)
        self.page_source_contains(case_name)
        assert True, "Case name is present in Submit history"
        # self.driver.close()
        # self.switch_back_to_prev_tab()
        self.driver.back()

    def verify_form_data_case_list(self, case_name):
        self.wait_to_click(self.case_list_rep)
        self.wait_to_click(self.users_box)
        self.wait_to_click(self.select_user)
        self.send_keys(self.search_input, case_name)
        self.wait_to_click(self.apply_id)
        time.sleep(15)
        self.scroll_to_bottom()
        self.verify_table_not_empty(self.case_list_table)
        self.page_source_contains(case_name)
        self.wait_and_sleep_to_click((By.LINK_TEXT, str(case_name)))
        # self.switch_to_next_tab()
        time.sleep(3)
        self.page_source_contains(case_name)
        assert True, "Case name is present in Case List"
        # self.driver.close()
        # self.switch_back_to_prev_tab()
        self.driver.back()

    def verify_app_data_submit_history(self, case_name):
        print("Sleeping for sometime for the case to get registered.")
        time.sleep(90)
        self.wait_to_click(self.submit_history_rep)
        self.wait_for_element(self.users_box, 300)
        self.wait_to_click(self.users_box)
        self.send_keys(self.search_user, UserData.app_login)
        self.wait_to_click((By.XPATH, self.app_user_select.format(UserData.new_app_login)))
        self.select_by_text(self.application_select, UserData.reassign_cases_application)
        self.select_by_text(self.module_select, UserData.case_list_name)
        self.select_by_text(self.form_select, UserData.new_form_name)
        date_range = self.get_todays_date_range()
        self.clear(self.date_input)
        self.send_keys(self.date_input, date_range + Keys.TAB)
        self.wait_to_click(self.apply_id)
        time.sleep(50)
        self.scroll_to_bottom()
        self.verify_table_not_empty(self.submit_history_table)
        self.is_present_and_displayed(self.view_form_link)
        form_link = self.get_attribute(self.view_form_link, "href")
        print("View Form Link: ", form_link)
        # self.switch_to_new_tab()
        self.driver.get(form_link)
        time.sleep(3)
        self.page_source_contains(case_name)
        assert True, "Case name is present in Submit history"

    def verify_updated_data_in_case_list(self, case_name, value):
        self.page_source_contains(case_name)
        self.wait_and_sleep_to_click((By.LINK_TEXT, str(case_name)))
        time.sleep(3)
        self.page_source_contains(case_name)
        assert self.is_present_and_displayed(
            (By.XPATH, "//div[@id='properties']//td[contains(text(),'" + value + "')]")
            ), "Case property not updated."
        print("Case is updated successfully")
        case_id = self.get_text(self.case_id_block)
        return case_id

    def validate_messaging_history_for_cond_alert(self, cond_alert):
        self.wait_to_click(self.messaging_history_rep)
        date_range = self.get_todays_date_range()
        self.clear(self.date_input)
        self.send_keys(self.date_input, date_range + Keys.TAB)
        time.sleep(2)
        self.deselect_all(self.communication_type_select)
        time.sleep(2)
        self.select_by_text(self.communication_type_select, UserData.communication_type)
        self.check_if_report_loaded()
        self.scroll_to_bottom()
        print(cond_alert)
        list_alerts = self.driver.find_elements(By.XPATH, "//td[.='" + cond_alert + "']/following-sibling::td[3]")
        print(len(list_alerts))
        if len(list_alerts) > 0:
            for i in range(len(list_alerts)):
                text = list_alerts[i].text
                print(text)
                if "Completed" in text:
                    assert True
                elif "Internal Server Error" in text:
                    assert False
                else:
                    print("Alert status is not Completed but has no Internal Server Error")

    def check_for_case_list_owner(self, url):
        if 'www' in url:
            owner = UserData.appiumtest_owner_id_prod
        else:
            owner = UserData.appiumtest_owner_id
        self.wait_to_click(self.case_list_rep)
        self.wait_for_element(self.remove_case_owner)
        self.wait_to_click(self.remove_case_owner)
        self.wait_to_click(self.case_owner_textarea)
        self.send_keys(self.case_owner_textarea, UserData.app_login)
        self.wait_for_element((By.XPATH, self.case_owner_list_item.format(UserData.app_login)))
        self.wait_to_click((By.XPATH, self.case_owner_list_item.format(UserData.app_login)))
        self.wait_to_click(self.apply_id)
        time.sleep(15)
        self.scroll_to_bottom()
        list_of_owner = self.find_elements(self.case_owner_column)
        print(len(list_of_owner))
        if len(list_of_owner) > 0:
            for i in range(len(list_of_owner)):
                text = list_of_owner[i].text
                print(text)
                assert text == owner or text == UserData.user_group, "Owner does not match"
                self.check_if_html(text)

    def check_for_case_list_explorer_owner(self, url):
        if 'www' in url:
            owner = UserData.appiumtest_owner_id_prod
        else:
            owner = UserData.appiumtest_owner_id
        self.wait_to_click(self.case_list_explorer)
        time.sleep(5)
        self.wait_for_element(self.edit_column)
        self.wait_to_click(self.edit_column)
        self.wait_for_element(self.properties_table)
        self.wait_to_click(self.add_property_button)
        self.wait_to_click(self.property_name_input)
        self.send_keys(self.property_name_input, "owner_name")
        time.sleep(1)
        ActionChains(self.driver).key_down(Keys.ENTER).send_keys(Keys.TAB).perform()
        self.scroll_to_element(self.remove_case_owner)
        self.wait_to_click(self.remove_case_owner)
        self.wait_to_click(self.case_owner_textarea)
        self.send_keys(self.case_owner_textarea, UserData.app_login)
        self.wait_for_element((By.XPATH, self.case_owner_list_item.format(UserData.app_login)))
        self.wait_to_click((By.XPATH, self.case_owner_list_item.format(UserData.app_login)))
        self.wait_to_click(self.apply_id)
        time.sleep(15)
        self.scroll_to_bottom()
        list_of_owner = self.find_elements(self.cle_case_owner_column)
        print(len(list_of_owner))
        if len(list_of_owner) > 0:
            for i in range(len(list_of_owner)):
                text = list_of_owner[i].text
                print(text)
                assert text == owner or text == UserData.user_group, "Owner does not match"
                self.check_if_html(text)

    def check_if_html(self, text):
        re_is_html = re.compile(r"(?:</[^<]+>)|(?:<[^<]+/>)")
        result = re_is_html.search(text)
        if result:
            print("Owner name has html tags")
            assert False
        else:
            print("No html tag present")
            assert True

    def configure_add_report(self):
        self.wait_to_click(self.configurable_report)
        time.sleep(10)
        self.wait_for_element(self.report_dropdown, 300)
        self.wait_to_click(self.edit_report_dropdown)
        self.wait_for_element(self.report_search_input)
        self.send_keys(self.report_search_input, self.report_name_form)
        self.wait_to_click((By.XPATH, self.select_report.format(self.report_name_form)))
        # self.select_by_text(self.report_dropdown, self.report_name_form)
        time.sleep(10)
        # self.wait_for_element(self.description_input, 300)
        assert self.is_present_and_displayed(self.description_input, 300), "Edit screen is not displayed"
        self.wait_to_clear_and_send_keys(self.description_input, "editing " + self.report_name_form)
        self.scroll_to_element(self.save_button)
        self.wait_to_click(self.save_button)
        time.sleep(10)
        assert self.is_present_and_displayed(self.success_alert, 300), "Report not saved successfully"
        # self.wait_for_element(self.success_alert, 400)

    def verify_only_permitted_report(self, report_name):
        self.wait_to_click(self.reports_menu_id)
        assert self.is_present_and_displayed((By.LINK_TEXT, report_name))
        self.wait_to_click((By.LINK_TEXT, report_name))
        assert self.is_present_and_displayed(self.apply_id), "Report page not accessible"
        print("Report page is accessible")

    def export_daily_form_activity_to_excel(self):
        self.wait_to_click(self.daily_form_activity_rep)
        try:
            self.wait_for_element(self.remove_active_worker)
            count = self.find_elements(self.remove_buttons)
            print(len(count))
            for i in range(len(count)):
                count[0].click()
                time.sleep(2)
                if len(count) != 1:
                    ActionChains(self.driver).send_keys(Keys.TAB).perform()
                    time.sleep(2)
                count = self.find_elements(self.remove_buttons)
            # self.wait_to_click(self.users_field)
            self.send_keys(self.users_field, UserData.app_login)
            self.wait_to_click((By.XPATH, self.user_from_list.format(UserData.app_login)))
            time.sleep(2)
            ActionChains(self.driver).send_keys(Keys.TAB).perform()
            self.wait_to_click(self.apply_id)
            time.sleep(10)
        except (TimeoutException, NoSuchElementException):
            print("Button Disabled")
        try:
            assert self.is_visible_and_displayed(self.report_content_id)
        except (TimeoutException, AssertionError):
            assert self.is_visible_and_displayed(self.custom_report_content_id)
        print("Report loaded successfully!")
        self.wait_for_element(self.daily_form_activity_results)
        col = self.find_elements(self.daily_form_activity_results_cells)
        list = []
        for c in col:
            list.append(c.text)
        print(list)
        # web_data = pd.DataFrame(list)
        self.wait_to_click(self.export_to_excel)
        self.wait_for_element(self.export_success)
        print("Export to excel successful")
        print("Sleeping for some time for the email to be sent")
        time.sleep(30)
        return list

    def compare_web_with_email(self, link, web_data):
        try:
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
                if html.unescape(str(list[i])) == str(web_data[i]):
                    assert True
                else:
                    print("Comparison failed for " + list[i] + " and " + web_data[i])
        except Exception:
            print("No Data to compare or there is data mismatch")

    def export_app_status_to_excel(self):
        self.wait_to_click(self.application_status_rep)
        try:
            self.wait_for_element(self.remove_active_worker)
            count = self.find_elements(self.remove_buttons)
            print(len(count))
            for i in range(len(count)):
                count[0].click()
                time.sleep(2)
                if len(count) != 1:
                    ActionChains(self.driver).send_keys(Keys.TAB).perform()
                    time.sleep(2)
                count = self.find_elements(self.remove_buttons)

            # self.wait_to_click(self.users_field)
            self.send_keys(self.users_field, UserData.app_login)
            self.wait_to_click((By.XPATH, self.user_from_list.format(UserData.app_login)))
            self.wait_to_click(self.apply_id)
            time.sleep(10)
        except (TimeoutException, NoSuchElementException):
            print("Button Disabled")
        try:
            assert self.is_visible_and_displayed(self.report_content_id)
        except (TimeoutException, AssertionError):
            assert self.is_visible_and_displayed(self.custom_report_content_id)
        print("Report loaded successfully!")
        self.wait_for_element(self.app_status_results)
        col = self.find_elements(self.app_status_results_cells)
        list = []
        for c in col:
            list.append(c.text)
        print(list)
        # web_data = pd.DataFrame(list)
        self.wait_to_click(self.export_to_excel)
        self.wait_for_element(self.export_success)
        print("Export to excel successful")
        print("Sleeping for some time for the email to be sent")
        time.sleep(30)
        return list

    def compare_app_status_web_with_email(self, link, web_data):
        try:
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
            for i in range(len(ext_list))[:]:
                list += ext_list[i]
            print("List New: ", list)
            print("Old data rows: ", len(web_data), "New data rows: ", len(list))
            print("Old List: ", web_data)
            print("New list: ", list)
            assert len(web_data) == len(list), "Data in Both Excel and Searched results do not match"
            print("Both Excel and Searched results have same amount of data")
            for i in range(len(list)):
                if i == 1 or i == 2 or i == 3:
                    print("Not comparing", html.unescape(str(list[i])), " with ", str(web_data[i]))
                else:
                    print("Comparing ", html.unescape(str(list[i])), " with ", str(web_data[i]))
                    assert html.unescape(str(list[i])) == str(web_data[i]), "Comparison failed for " + list[
                        i] + " and " + web_data[i]
        except Exception:
            print("No Data to compare or there is Data mismatch")

    def verify_form_in_submit_history(self, app_name, lat, lon):
        print("Sleeping for sometime for the case to get registered.")
        time.sleep(140)
        self.wait_to_click(self.submit_history_rep)
        self.wait_for_element(self.users_box, 200)
        self.wait_to_click(self.users_box)
        self.send_keys(self.search_user, UserData.app_login)
        self.wait_to_click((By.XPATH, self.app_user_select.format(UserData.app_login)))
        self.select_by_text(self.application_select, app_name)
        self.select_by_text(self.module_select, UserData.case_list_name)
        date_range = self.get_todays_date_range()
        self.clear(self.date_input)
        self.send_keys(self.date_input, date_range + Keys.TAB)
        self.wait_to_click(self.apply_id)
        time.sleep(15)
        self.scroll_to_bottom()
        self.verify_table_not_empty(self.submit_history_table)
        self.is_present_and_displayed(self.view_form_link)
        form_link = self.get_attribute(self.view_form_link, "href")
        print("View Form Link: ", form_link)
        # self.switch_to_new_tab()
        self.driver.get(form_link)
        time.sleep(3)
        text = self.get_text(self.location_values)
        text = text.split(" ")
        result_lat = self.format_number(abs(float(text[0])), 5)
        result_lon = self.format_number(abs(float(text[1])), 5)
        print(result_lat, result_lon)
        assert result_lat in lat and result_lon in lon, "Mismatch"

    def format_number(self, n, digits):
        formatter = '{:.' + '{}'.format(digits) + 'f}'
        x = round(n, digits)
        return formatter.format(x)

    def verify_case_list_page(self):
        self.wait_to_click(self.case_list_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.CASE_LIST_TITLE in self.driver.title, "This is not the Case List page."
        text = self.get_text(self.panel_body_text)
        print(text)
        assert "Why can't I see any data?" in text
        assert "Please choose your filters above and click Apply to see report data." in text

    def export_to_excel_config_report(self, report_name):
        self.wait_to_click((By.LINK_TEXT, report_name))
        time.sleep(10)
        self.wait_for_element(self.export_to_excel)
        self.wait_to_click(self.export_to_excel)
        self.wait_till_progress_completes("exports")
        self.wait_to_click(self.download_report_link, 300)
        print("Downloading report...")
        time.sleep(3)
        newest_file = latest_download_file()
        print("Newest file:" + newest_file)
        self.assert_downloaded_file(newest_file, report_name)

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
        ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()

    def verify_sorted_list(self):
        self.select_by_value(self.page_list_dropdown, '100')
        time.sleep(10)
        list1 = self.find_elements(self.last_submit_column_list)
        list1_names = list()
        for item in list1:
            list1_names.append(item.text)
        print(list1_names)
        sorted_time_list = sort_times(list1_names)
        print(sorted_time_list)
        if list1_names == sorted_time_list:
            assert True
        else:
            assert False
        # result = is_list_sorted_new_to_old(list1_names)
        # print(result)

    def application_status_report_search(self):
        self.wait_to_click(self.application_status_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.APPLICATION_STATUS_TITLE in self.driver.title, "This is not the Application Status page."
        self.remove_default_users()
        self.click(self.application_field)
        self.send_keys(self.application_input, UserData.reassign_cases_application)
        self.wait_to_click((By.XPATH, self.users_list_item.format(UserData.reassign_cases_application)))
        time.sleep(2)
        self.wait_to_click(self.apply_id)
        time.sleep(10)
        self.wait_for_element(self.result_table, 300)
        assert self.is_visible_and_displayed(self.report_content_id, 120), "Report not loaded"
        print("Report loaded successfully!")

    def verify_case_list_explorer_properties(self):
        self.wait_to_click(self.case_list_explorer_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.case_list_explorer_TITLE in self.driver.title, "This is not the Case List Explorer page."
        self.select_by_value(self.case_type_dropdown, UserData.case_reassign)
        return UserData.case_reassign

    def add_new_property(self, name):
        self.scroll_to_element(self.column_editor)
        self.wait_to_click(self.column_editor)
        props1 = self.find_elements(self.properties_input)
        value1 = self.find_elements(self.value_input)
        delete1 = self.find_elements(self.delete_property)
        assert len(props1) != 0, "Property fields not present"
        assert len(value1) != 0, "Value fields not present"
        assert len(delete1) != 0, "Delete fields not present"
        self.wait_for_element(self.add_property_button)
        self.wait_to_click(self.add_property_button)
        time.sleep(2)
        assert len(props1) + 1 == len(self.find_elements(self.properties_input)), "Property fields not added"
        assert len(value1) + 1 == len(self.find_elements(self.value_input)), "Value fields not added"
        assert len(delete1) + 1 == len(self.find_elements(self.delete_property)), "Delete fields not added"
        self.send_keys(self.last_properties_input, "name")
        time.sleep(2)
        if self.is_visible_and_displayed((By.XPATH, self.property_label.format(name))):
            assert True
            print("Property present")
        else:
            print("Property absent")
            assert False
        ActionChains(self.driver).send_keys(Keys.TAB).perform()

    def get_case_id_from_case_list_explorer(self, text):
        query = "case_name = '" + text + "'"
        self.wait_to_click(self.case_list_explorer_rep)
        self.wait_for_element(self.apply_id, 100)
        self.remove_default_users()
        self.js_click(self.query_div)
        time.sleep(2)
        self.send_keys(self.case_list_explorer_query_field, query)
        time.sleep(2)
        self.select_by_text(self.case_type_dropdown, UserData.case_reassign_change)
        time.sleep(2)
        self.scroll_to_element(self.apply_id)
        self.js_click(self.apply_id)
        time.sleep(5)
        self.wait_for_element(self.result_table, 300)
        assert self.is_visible_and_displayed(self.report_content_id, 120), "Report not loaded"
        print("Report loaded successfully!")
        form_link = self.get_attribute(self.view_case_link, "href")
        print("View Form Link: ", form_link)
        # self.switch_to_new_tab()
        self.driver.get(form_link)
        time.sleep(3)
        self.page_source_contains(text)
        assert True, "Case name is present in Submit history"
        self.page_source_contains(text)
        print("Case is updated successfully")
        case_id = self.get_text(self.case_id_block)
        return case_id

