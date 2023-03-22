import time
from datetime import datetime

from selenium.webdriver.support.select import Select

from common_utilities.selenium.base_page import BasePage
from common_utilities.generate_random_string import fetch_random_string
from HQSmokeTests.userInputs.user_inputs import UserData

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

""""Contains test page elements and functions related to the Reports module"""


class ReportPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

        self.report_name_form = "report form " + fetch_random_string()
        self.report_name_case = "report case " + fetch_random_string()
        self.report_name_saved = "saved form " + fetch_random_string()

        # Mobile Worker Reports
        self.worker_activity_rep = (By.LINK_TEXT, "Worker Activity")
        self.daily_form_activity_rep = (By.LINK_TEXT, "Daily Form Activity")
        self.submissions_by_form_rep = (By.LINK_TEXT, "Submissions By Form")
        self.form_completion_rep = (By.LINK_TEXT, "Form Completion Time")
        self.case_activity_rep = (By.LINK_TEXT, "Case Activity")
        self.completion_vs_submission_rep = (By.LINK_TEXT, "Form Completion vs. Submission Trends")
        self.worker_activity_times_rep = (By.LINK_TEXT, "Worker Activity Times")
        self.project_performance_rep = (By.LINK_TEXT, "Project Performance")

        # Inspect Data Reports
        self.submit_history_rep = (By.LINK_TEXT, "Submit History")
        self.case_list_rep = (By.LINK_TEXT, "Case List")

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
        self.select_source_id_form_value = "Case List / Registration Form"
        self.select_source_id_case_value = "commcare-user"

        # Saved Reports
        self.new_saved_report_name = (By.ID, "name")
        self.save_confirm = (By.XPATH, '//div[@class = "btn btn-primary"]')
        self.saved_reports_menu_link = (By.LINK_TEXT, 'My Saved Reports')
        self.saved_report_created = (By.XPATH, "//a[text()='" + self.report_name_saved + "']")
        self.delete_saved = (By.XPATH,
                             "(//a[text()='" + self.report_name_saved + "']//following::button[@class='btn btn-danger add-spinner-on-click'])[1]")

        # Scheduled Reports
        self.scheduled_reports_menu_xpath = (By.XPATH, "//a[@href='#scheduled-reports']")
        self.create_scheduled_report = (By.XPATH, "//a[@class='btn btn-primary track-usage-link']")
        self.available_reports = (By.XPATH, "//li[@class='ms-elem-selectable']")
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
        self.app_user_select =  "(//li[contains(text(),'{}')])[1]"
        self.application_select = (By.XPATH, "//select[@id='report_filter_form_app_id']")
        self.module_select = (By.XPATH, "//select[@id='report_filter_form_module']")
        self.form_select = (By.XPATH, "//select[@id='report_filter_form_xmlns']")
        self.case_type_select = (By.XPATH, "//select[@id='report_filter_case_type']")
        self.date_input = (By.XPATH, "//input[@id='filter_range']")
        self.view_form_link = (By.XPATH, "//tbody/tr[1]/td[1]/a[.='View Form']")
        self.case_name = (By.XPATH, "//td[div[contains(text(),'abc')]]")
        self.submit_history_table = (By.XPATH, "//table[@id='report_table_submit_history']/tbody/tr")

        # Case List
        self.search_input = (By.XPATH, "//input[@id='report_filter_search_query']")
        self.case_list_table = (By.XPATH, "//table[@id='report_table_case_list']/tbody/tr")
        self.case_id_block = (By.XPATH, "//th[@title='_id']/following-sibling::td")

        # Messaging History
        self.communication_type_select = (By.XPATH, "//label[.='Communication Type']/following-sibling::div/select")

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
        self.check_if_report_loaded()

    def case_list_report(self):
        self.wait_to_click(self.case_list_rep)
        self.check_if_report_loaded()

    def sms_usage_report(self):
        self.wait_to_click(self.sms_usage_rep)
        self.check_if_report_loaded()

    def messaging_history_report(self):
        self.wait_to_click(self.messaging_history_rep)
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
        self.click(self.select_app)
        self.select_by_text(self.select_source_id, self.select_source_id_case_value)
        self.wait_to_click(self.next_button_id)
        self.wait_to_click(self.save_and_view_button_id)
        self.check_if_report_loaded()
        self.delete_report()

    def create_report_builder_form_report(self):
        self.wait_to_click(self.create_new_rep_id)
        self.send_keys(self.report_name_textbox_id, self.report_name_form)
        self.select_by_value(self.form_or_cases, self.select_form_type_value)
        self.select_by_text(self.application, UserData.village_application)
        self.select_by_text(self.select_source_id, self.select_source_id_form_value)
        self.wait_to_click(self.next_button_id)
        self.wait_to_click(self.save_and_view_button_id)
        self.check_if_report_loaded()
        self.delete_report()

    def saved_report(self):
        self.wait_to_click(self.case_activity_rep)
        self.wait_to_click(self.save_xpath)
        self.send_keys(self.new_saved_report_name, self.report_name_saved)
        self.wait_to_click(self.save_confirm)
        time.sleep(2)
        self.js_click(self.saved_reports_menu_link)
        assert self.is_visible_and_displayed(self.saved_report_created)
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
        self.wait_to_click(self.submit_id)
        assert self.is_visible_and_displayed(self.success_alert)
        print("Scheduled Report Created Successfully")

    def delete_scheduled_and_saved_reports(self):
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

    def get_yesterday_tomorrow_dates(self):
        # Get today's date
        presentday = datetime.now()  # or presentday = datetime.today()
        # Get Yesterday
        # yesterday = presentday - timedelta(1)
        # Get Tomorrow
        # tomorrow = presentday + timedelta(1)

        return presentday.strftime('%Y-%m-%d') + " to " + presentday.strftime('%Y-%m-%d')

    def verify_table_not_empty(self, locator):
        clickable = ec.presence_of_all_elements_located(locator)
        element = WebDriverWait(self.driver, 30).until(clickable, message="Couldn't find locator: "
                                                                          + str(locator))
        count = len(element)
        if count > 0:
            print(count, " rows are present in the web table")
            return True
        else:
            print("No rows are present in the web table")
            return False

    def verify_form_data_submit_history(self, case_name, username):
        print("Sleeping for sometime for the case to get registered.")
        time.sleep(40)
        self.wait_to_click(self.submit_history_rep)
        self.wait_to_click(self.users_box)
        self.send_keys(self.search_user, username)
        self.wait_to_click((By.XPATH, self.app_user_select.format(username)))
        self.select_by_text(self.application_select, UserData.reassign_cases_application)
        self.select_by_text(self.module_select, UserData.case_list_name)
        self.select_by_text(self.form_select, UserData.form_name)
        date_range = self.get_yesterday_tomorrow_dates()
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
        time.sleep(40)
        self.wait_to_click(self.submit_history_rep)
        self.wait_to_click(self.users_box)
        self.send_keys(self.search_user, UserData.app_login)
        self.wait_to_click((By.XPATH, self.app_user_select.format(UserData.app_login)))
        self.select_by_text(self.application_select, UserData.reassign_cases_application)
        self.select_by_text(self.module_select, UserData.case_list_name)
        self.select_by_text(self.form_select, UserData.new_form_name)
        date_range = self.get_yesterday_tomorrow_dates()
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

    def verify_updated_data_in_case_list(self, case_name, value):
        self.page_source_contains(case_name)
        self.wait_and_sleep_to_click((By.LINK_TEXT, str(case_name)))
        time.sleep(3)
        self.page_source_contains(case_name)
        assert self.is_present_and_displayed(
            (By.XPATH, "//div[@id='properties']//td[contains(text(),'" + value + "')]")), "Case property not updated."
        print("Case is updated successfully")
        case_id = self.get_text(self.case_id_block)
        return case_id

    def validate_messaging_history_for_cond_alert(self, cond_alert):
        self.wait_to_click(self.messaging_history_rep)
        date_range = self.get_yesterday_tomorrow_dates()
        self.clear(self.date_input)
        self.send_keys(self.date_input, date_range + Keys.TAB)
        time.sleep(2)
        self.deselect_all(self.communication_type_select)
        time.sleep(2)
        self.select_by_text(self.communication_type_select, UserData.communication_type)
        self.check_if_report_loaded()
        self.scroll_to_bottom()
        print(cond_alert)
        list_alerts = self.driver.find_elements(By.XPATH, "//td[.='"+cond_alert+"']/following-sibling::td[3]")
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
