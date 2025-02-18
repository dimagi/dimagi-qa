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


class RawFormsErrorsDuplicatesPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

        # Mobile Worker Reports
        self.reports_menu_id = (By.ID, "ProjectReportsTab")
        self.red_rep = (By.LINK_TEXT, "Raw Forms, Errors & Duplicates")
        self.RED_TITLE = "Raw Forms, Errors & Duplicates - CommCare HQ"

        # Report Elements
        self.apply_id = (By.ID, "apply-filters")
        self.report_content_id = (By.ID, "report-content")
        self.homepage = (By.XPATH, ".//a[@href='/homepage/']")
        self.date_range_error = (By.XPATH, "//td[contains(.,'You are limited to a span of 90 days,')]")

        self.form_activity_results = (By.XPATH, "//table[@id='report_table_submit_errors']/tbody/tr")
        self.form_activity_results_cells = (
            By.XPATH, "//table[@id='report_table_submit_errors']/tbody/tr[not(contains(.,'All Users'))]/td")
        self.all_users_results_cells = (
            By.XPATH, "(//tfoot)[2]/tr/td")
        self.users_field = (By.XPATH, "(//textarea[@class='select2-search__field'])[1]")
        self.filter_dates_by = (By.XPATH, "//select[@id='report_filter_sub_time']")
        self.remove_buttons = (By.XPATH, "//ul//button")
        self.submit_form_type = "//div[@id='report_filter_submitfilter']//button[.='{}']"
        self.form_type_selected = "//div[@id='report_filter_submitfilter']//button[.='{}'][@aria-pressed='true']"
        self.form_type_selected_after = "//div[@id='report_filter_submitfilter']//button[.='{}'][contains(@class,'active')]"
        self.export_to_excel = (By.XPATH, "//a[@id='export-report-excel']")
        self.export_success = (By.XPATH,
                               "//span[.='Your requested Excel report will be sent to the email address defined in your account settings.']")
        self.user_column = (
            By.XPATH, "(//thead/tr/th[@aria-controls='report_table_submit_errors']/div[contains(.,'User')])[1]")
        self.all_forms_column = (
            By.XPATH,
            "(//thead/tr/th[@aria-controls='report_table_submit_errors']/div[contains(.,'All Forms')])[1]")
        self.app_mod_form_column = "(//thead/tr/th[@aria-controls='report_table_submit_errors']/div[contains(.,'{}')])[1]"
        self.column_names = "(//thead/tr/th[@aria-controls='report_table_submit_errors']/div[@data-title='{}'])[1]"
        self.column_group_names = (By.XPATH, "(//thead)[1]/tr/th/div")
        self.user_names_column_list = (By.XPATH, "//table[@id='report_table_submit_errors']//tbody//td[2]")
        self.submit_time_column_list = (By.XPATH, "//table[@id='report_table_submit_errors']//tbody//td[3]")
        self.result_table = (By.XPATH, "(//div[@id='report-content']//table//tbody//td[1])[1]")
        self.results_rows = (By.XPATH, "//tbody/tr")
        self.result_rows_names = "//table[@id='report_table_submit_errors']//tbody/tr/td[1]//a[contains(.,'{}')]"
        self.hide_filters_options = (By.XPATH, "//a[.='Hide Filter Options']")
        self.show_filters_options = (By.XPATH, "//a[.='Show Filter Options']")
        self.user_sort = "(//text()[contains(.,'{}')][not(contains(.,'View Form'))]//preceding-sibling::i[@class='icon-white fa dt-sort-icon'])[1]"
        self.error_type_column_list = (By.XPATH, "//table[@id='report_table_submit_errors']//tbody//td[5]")
        self.error_msg_column_list = (By.XPATH, "//table[@id='report_table_submit_errors']//tbody//td[6]")
        self.form_type_column_list = (By.XPATH, "//table[@id='report_table_submit_errors']//tbody//td[4]")
        self.total_cases_shared_column_list = (
            By.XPATH, "//table[@id='report_table_submit_errors']//tbody//td[8]")
        self.column_name_headers = "//table[@id='report_table_submit_errors']//thead//th/div/div[contains(.,'{}')]"

        # Pagination
        self.page_list_dropdown = (By.XPATH, "//select[@name='report_table_submit_errors_length']")
        self.table_info = (By.XPATH, "//div[@id='report_table_submit_errors_info']")
        self.prev_page_button = (By.XPATH, "//ul[@class='pagination']/li[@class='prev']/a")
        self.next_page_button = (By.XPATH, "//ul[@class='pagination']/li[@class='next']/a")
        self.prev_page_button_disabled = (By.XPATH, "//ul[@class='pagination']/li[@class='prev disabled']/a")
        self.next_page_button_disabled = (By.XPATH, "//ul[@class='pagination']/li[@class='next disabled']/a")
        self.page_button = "//ul[@class='pagination']/li/a[.='{}']"
        self.pagination_list = (By.XPATH, "//ul[@class='pagination']/li/a")
        self.pagination_page_numbers = (
            By.XPATH, "//ul[@class='pagination']/li[not(contains(@class,'next'))][not(contains(@class,'prev'))]")

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
        self.saved_report_title = (By.XPATH, "//h4[@data-bind='text: modalTitle']")
        self.cancel_report_button = (By.XPATH, "//div/a[.='Cancel']")
        self.saved_reports_menu_link = (By.LINK_TEXT, 'My Saved Reports')
        self.saved_report_created = "//a[text()='{}']"
        self.delete_saved = "(//a[text()='{}']//following::button[@class='btn btn-danger add-spinner-on-click'])[1]"

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
        self.filter_column_name = "(//thead//th[@aria-controls='report_table_submit_errors'][3]/div[contains(.,'{}')])[1]"
        self.submit_history_table_info = (By.XPATH, "//div[@id='report_table_submit_errors_info']")
        self.empty_table = (By.XPATH, "//tr/td[contains(.,'No data available to display.')]")
        self.submit_history_table_title = (By.XPATH, "//h2[@class='panel-title'][contains(.,'Submit History')]")

        # View Form Page
        self.view_form_tabs = "//li/a[contains(.,'{}')]"
        self.form_data_table = (By.XPATH, "//table[contains(@class,'form-data-table')]")
        self.archive_this_form = (By.XPATH, "//button[contains(.,'Archive this form')]")
        self.clean_form_submission = (By.XPATH, "//button[contains(.,'Clean Form Submission')]")
        self.form_table_case_name = (By.XPATH, "//td[.//span[contains(.,'Case name')]]//following-sibling::td/div")
        self.restore_this_form = (By.XPATH, "//button[contains(.,'Restore this form')]")
        self.delete_this_form = (By.XPATH, "//button[contains(.,'Delete this form')]")
        self.delete_confirm_button = (By.XPATH, "//div[@class='modal-footer']/*[contains(@class,'btn btn-danger')]")
        self.delete_case_confirm = (By.XPATH, "//*[@data-target='#delete_case_confirmation']")
        self.case_text = (By.XPATH, "//p[contains(.,'delete this form, type')]/strong")
        self.textarea_delete_popup = (
            By.XPATH, "//p[contains(.,'delete this form, type')][./strong]//following-sibling::textarea")
        self.archive_success_msg = (
            By.XPATH, "//div[contains(@class,'alert-margin-top')][contains(.,'Form was successfully archived')]")
        self.undo_archive = (By.XPATH, "//div[contains(@class,'alert-margin-top')]//a[contains(.,'Undo')]")
        self.restore_success_msg = (
            By.XPATH, "//div[contains(@class,'alert-margin-top')][contains(.,'Form was successfully restored')]")
        self.clean_form_submission_title = (By.XPATH, "//h4[contains(.,'Clean Form Submission')]")
        self.clean_form_save = (By.XPATH, "//button[@class='btn btn-primary']//span[contains(.,'Save')]")
        self.clean_form_cancel = (By.XPATH, "//button[@class='btn btn-default'][contains(.,'Cancel')]")
        self.clean_form_input_field = (By.XPATH, "//label[.//span[contains(.,'Case name')]]//following-sibling::div//input")

        self.view_form_column_list = (By.XPATH, "//table[@id='report_table_submit_errors']//tbody//td[1]/a")
        self.view_form_column_first = (By.XPATH, "(//table[@id='report_table_submit_errors']//tbody//td[1]/a)[1]")
        self.panel_body_text = (By.XPATH, "//div[@class='panel-body-datatable']")
        self.submit_form_section = (By.XPATH, "//div[@id='report_filter_submitfilter']")
        self.manage_deployments_list = (By.XPATH, "//h2[.='Manage Deployments']//following-sibling::ul[1]/li/a")
        self.manage_deployments_section = (By.XPATH, "//div[@id='hq-sidebar'][.//h2[.='Manage Deployments']]")

    def verify_page(self):
        self.wait_to_click(self.red_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.RED_TITLE in self.driver.title, "This is not the Raw Forms Errors & Duplicates page."
        text = self.get_text(self.panel_body_text)
        self.verify_manage_deployment_section()
        print(text)
        assert "Why can't I see any data?" in text
        assert "Please choose your filters above and click Apply to see report data." in text

    def verify_manage_deployment_section(self):
        assert self.is_visible_and_displayed(
            self.manage_deployments_section), "Manage Deployments section is not present in the left panel"
        print("Manage Deployments section is present in the left panel")
        elements = self.find_elements(self.manage_deployments_list)
        link_list = []
        for items in elements:
            link_list.append(items.text)
        print(link_list)
        assert "Raw Forms, Errors & Duplicates" in link_list, "Raw Forms, Errors & Duplicates is not present in the Manage Deployments section"
        print("Raw Forms, Errors & Duplicates is present in the Manage Deployments section")
        assert sorted(link_list) == sorted(
            UserData.manage_deployments_list), "Manage Deployments section list mismatched"
        print("Manage Deployments section has the list: ", link_list)

    def hide_filters(self):
        self.wait_to_click(self.red_rep)
        self.wait_for_element(self.hide_filters_options)
        self.click(self.hide_filters_options)
        time.sleep(2)
        assert not self.is_visible_and_displayed(self.submit_form_section,
                                                 10), "Submit Form Filter section is still present"
        assert not self.is_visible_and_displayed(self.application_dropdown, 10), "Application dropdown is still present"
        assert not self.is_visible_and_displayed(self.show_adv_options,
                                                 10), "Show Advance Options checkbox is still present"
        assert not self.is_visible_and_displayed(self.apply_id,
                                                 10), "Apply button is still present"
        assert not self.is_visible_and_displayed(self.favorite_button,
                                                 10), "Favorite button is still present"
        assert not self.is_visible_and_displayed(self.save_config_button,
                                                 10), "Save button is still present"
        assert self.is_present(self.show_filters_options), "Show Filters Options is not present"
        print("All filters are hidden!")

    def show_filters(self):
        self.wait_for_element(self.show_filters_options)
        self.click(self.show_filters_options)
        time.sleep(2)
        assert self.is_present(self.submit_form_section), "Submit Form Filter section is not present"
        assert self.is_present(self.application_dropdown), "Application dropdown is not present"
        assert self.is_present(self.show_adv_options), "Show Advance Options checkbox is not present"
        assert self.is_present(self.apply_id), "Apply button is not present"
        assert self.is_present(self.favorite_button), "Favorite button is not present"
        assert self.is_present(self.save_config_button), "Save button is not present"
        assert self.is_present(self.hide_filters_options), "Show Filters Options is not present"
        print("All filters are shown!")

    def verify_red_page_fields_columns(self):
        self.wait_to_click(self.red_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.RED_TITLE in self.driver.title, "This is not the Raw Forms, Errors & Duplicates page."
        assert self.is_present(self.submit_form_section), "Submit Form Filter section is still present"
        for items in UserData.submit_form_type:
            assert self.is_present((By.XPATH, self.submit_form_type.format(items))), "Not present item: " + items
        print("All types are present: ", UserData.submit_form_type)
        assert self.is_present(self.application_dropdown), "Application dropdown is not present"
        assert self.is_present(self.show_adv_options), "Show Advance Options checkbox is not present"
        assert self.is_present(self.hide_filters_options), "Show Filters Options is not present"
        print("All filters are shown!")

        self.wait_to_click((By.XPATH, self.submit_form_type.format(UserData.submit_form_type[0])))
        assert self.is_visible_and_displayed((By.XPATH, self.form_type_selected.format(UserData.submit_form_type[0])))
        time.sleep(1)
        self.select_application_and_forms(UserData.reassign_cases_application,
                                          list(UserData.reasign_modules_forms.keys())[1],
                                          UserData.reasign_modules_forms[
                                              list(UserData.reasign_modules_forms.keys())[1]][0])
        column_name = UserData.reassign_cases_application + " > " + list(UserData.reasign_modules_forms.keys())[
            1] + " > " + UserData.reasign_modules_forms[list(UserData.reasign_modules_forms.keys())[1]][0]
        time.sleep(2)
        self.wait_to_click(self.apply_id)
        time.sleep(10)
        self.wait_for_element(self.result_table, 300)
        assert self.is_visible_and_displayed(self.report_content_id, 120), "Report not loaded"
        print("Report loaded successfully!")
        self.scroll_to_element(self.result_table)
        time.sleep(5)
        assert self.is_present(self.page_list_dropdown), "Page list dropdown not present"
        assert self.is_present(self.next_page_button), "Next page button not present"
        pages = self.find_elements(self.pagination_page_numbers)
        assert len(pages) > 0, "Number of pages not present"
        list_col = self.find_elements(self.column_group_names)
        for item in list_col:
            text = item.text
            print(text)
            assert text in UserData.red_column_names, "Column not present"
            print(text, " is present!")
        users = self.find_elements(self.user_names_column_list)
        links = self.find_elements(self.view_form_column_list)
        form_type = self.find_elements(self.form_type_column_list)
        error_type = self.find_elements(self.error_type_column_list)
        for items in links:
            assert "View Form" == items.text, "View Form link is not present"
        print(len(users), len(links))
        assert len(users) == len(links), "All View Form cells does not have hyperlinks"
        for items in error_type:
            assert UserData.submit_form_type[0] == items.text, "Incorrect Error type is present"
        print("Correct Error type present for: ", UserData.submit_form_type[0])
        for items in form_type:
            assert column_name in items.text, "Incorrect Form type is present"
        print("Correct Form type present for: ", column_name)

    def verify_red_page_no_filter(self):
        self.wait_to_click(self.red_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.RED_TITLE in self.driver.title, "This is not the Raw Forms, Errors & Duplicates page."
        assert self.is_present(self.submit_form_section), "Submit Form Filter section is still present"
        for items in UserData.submit_form_type:
            assert self.is_present((By.XPATH, self.submit_form_type.format(items))), "Not present item: " + items
        print("All types are present: ", UserData.submit_form_type)
        assert self.is_present(self.application_dropdown), "Application dropdown is not present"
        assert self.is_present(self.show_adv_options), "Show Advance Options checkbox is not present"
        assert self.is_present(self.hide_filters_options), "Show Filters Options is not present"
        time.sleep(2)
        self.wait_to_click(self.apply_id)
        time.sleep(10)
        self.wait_for_element(self.result_table, 300)
        assert self.is_visible_and_displayed(self.report_content_id, 120), "Report not loaded"
        print("Report loaded successfully!")
        self.scroll_to_element(self.result_table)
        time.sleep(5)
        for items in UserData.submit_form_type:
            assert not self.is_visible_and_displayed((By.XPATH, self.form_type_selected.format(items)),
                                                     10), "Not present item: " + items
        assert self.is_present(self.empty_table), "Results should not be displayed"
        print("no data present in the result table")

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
        time.sleep(2)
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
            time.sleep(2)
            if len(count) != 1:
                ActionChains(self.driver).send_keys(Keys.TAB).perform()
                time.sleep(2)
            count = self.find_elements(self.remove_buttons)

    def verify_users_in_the_group(self):
        list = self.find_elements(self.results_rows)
        if len(list) > 0:
            for item in UserData.automation_group_users:
                assert self.is_present((By.XPATH, self.result_rows_names.format(
                    item))), "Group user " + item + " is not present in results."
                print("Group User " + item + " is present in results.")

    def red_pagination_list(self):
        self.wait_to_click(self.red_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.RED_TITLE in self.driver.title, "This is not the Worker Activity page."
        self.wait_to_click((By.XPATH, self.submit_form_type.format(UserData.submit_form_type[2])))
        assert self.is_visible_and_displayed((By.XPATH, self.form_type_selected.format(UserData.submit_form_type[2])))
        time.sleep(1)
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
        self.wait_for_element(self.table_info, 200)
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

    def verify_sorted_list(self, col_name):
        self.select_by_value(self.page_list_dropdown, UserData.pagination[3])
        time.sleep(10)
        self.wait_to_click((By.XPATH, self.user_sort.format(col_name)))
        time.sleep(15)
        if "User" in col_name:
            list1 = self.find_elements(self.user_names_column_list)
        elif "Time" in col_name:
            list1 = self.find_elements(self.submit_time_column_list)
        else:
            print("Invalid Column Name")
        list1_names = list()
        for item in list1:
            list1_names.append(item.text)
        if "Completion" in col_name:
            sorted_list = sorted(list1_names,
                                 key=lambda list1_names: datetime.strptime(list1_names, "%Y-%m-%d %H:%M:%S"))
        else:
            sorted_list = sorted(list1_names)
        print(list1_names)
        print(sorted_list)
        assert list1_names == sorted_list, "List is not sorted"
        print("List is in ascending order")
        self.wait_to_click((By.XPATH, self.user_sort.format(col_name)))
        time.sleep(15)
        if "User" in col_name:
            list2 = self.find_elements(self.user_names_column_list)
        elif "Time" in col_name:
            list2 = self.find_elements(self.submit_time_column_list)
        else:
            print("Invalid Column Name")
        list2_names = list()
        for item in list2:
            list2_names.append(item.text)
        if "Time" in col_name:
            rev_list = sorted(list1_names, reverse=True,
                              key=lambda list1_names: datetime.strptime(list1_names, "%Y-%m-%d %H:%M:%S"))
        else:
            rev_list = sorted(list1_names, reverse=True)
        print(list2_names)
        print(rev_list)
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

    def red_search(self, date_range=UserData.date_range[0]):
        date_string = start_date = end_date = ''
        self.wait_to_click(self.red_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.RED_TITLE in self.driver.title, "This is not the Raw Forms, Errors & Duplicates page."
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

    def red_search_custom_date(self):
        self.wait_to_click(self.red_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.RED_TITLE in self.driver.title, "This is not the Raw Forms, Errors & Duplicates page."
        self.select_by_text(self.filter_dates_by, UserData.filter_dates_by[0])
        date_string, start_date, end_date = self.get_custom_dates_past(0, 0, 5)
        self.clear(self.date_input)
        self.send_keys(self.date_input, date_string + Keys.TAB)
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
        self.wait_to_click(self.red_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.RED_TITLE in self.driver.title, "This is not the Raw Forms, Errors & Duplicates page."
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

    def red_save_report(self):
        self.wait_to_click(self.red_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.RED_TITLE in self.driver.title, "This is not the Worker Activity page."
        self.wait_to_click((By.XPATH, self.submit_form_type.format(UserData.submit_form_type[2])))
        assert self.is_visible_and_displayed((By.XPATH, self.form_type_selected.format(UserData.submit_form_type[2])))
        time.sleep(1)
        self.wait_to_click(self.apply_id)
        time.sleep(10)
        self.wait_for_element(self.result_table, 300)
        assert self.is_visible_and_displayed(self.report_content_id, 120), "Report not loaded"
        print("Report loaded successfully!")
        error_type = self.find_elements(self.error_type_column_list)
        for items in error_type:
            assert UserData.submit_form_type[2] == items.text, "Incorrect Error type is present"
        print("Correct Error type present for: ", UserData.submit_form_type[0])
        time.sleep(10)
        report_name = "Saved Raw Forms, Errors & Duplicates Report " + fetch_random_string()
        self.verify_favorite_empty(report_name)
        self.save_report_donot_save(report_name)
        report = self.save_report(report_name)
        self.wait_to_click(self.red_rep)
        self.wait_for_element(self.apply_id, 100)
        self.verify_favorite_created(report)
        time.sleep(10)
        error_type = self.find_elements(self.error_type_column_list)
        for items in error_type:
            assert UserData.submit_form_type[2] == items.text, "Incorrect Error type is present"
        print("Correct Error type present for: ", UserData.submit_form_type[0])
        assert self.is_visible_and_displayed(
            (By.XPATH, self.form_type_selected_after.format(UserData.submit_form_type[2])))
        self.delete_saved_report(report)
        self.wait_to_click(self.red_rep)
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
        self.wait_to_clear_and_send_keys(self.description_field, report_name)
        assert self.is_present(self.name_field)
        assert self.is_present(self.description_field)
        assert self.is_present(self.cancel_report_button)
        assert self.is_present(self.save_report_button)
        text = self.get_text(self.saved_report_title)
        print(text)
        assert report_name in text, "Report Name is visible in the Title"
        self.wait_to_click(self.cancel_report_button)
        time.sleep(2)
        assert not self.is_visible_and_displayed(self.name_field, 10), "Save Report Form not closed"
        assert not self.is_visible_and_displayed(self.description_field, 10)
        assert not self.is_visible_and_displayed(self.cancel_report_button, 10)
        assert not self.is_visible_and_displayed(self.save_report_button, 10)
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
        self.clear(self.description_field)
        text = self.get_text(self.saved_report_title)
        print(text)
        assert report_name in text, "Report Name is visible in the Title"
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

    def export_red_to_excel(self):
        self.wait_to_click(self.red_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.RED_TITLE in self.driver.title, "This is not the Worker Activity page."
        self.verify_user_lookup_table()
        self.remove_default_users()
        self.send_keys(self.users_field, UserData.user_group)
        self.wait_to_click((By.XPATH, self.users_list_item.format(UserData.user_group)))
        time.sleep(1)
        self.select_application_and_forms(UserData.reassign_cases_application,
                                          list(UserData.reasign_modules_forms.keys())[1],
                                          UserData.reasign_modules_forms[
                                              list(UserData.reasign_modules_forms.keys())[1]][0])
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

    def export_red_email(self):
        self.wait_to_click(self.red_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.RED_TITLE in self.driver.title, "This is not the Raw Forms, Errors & Duplicates page."
        self.verify_user_lookup_table()
        self.remove_default_users()
        self.send_keys(self.users_field, UserData.user_group)
        self.wait_to_click((By.XPATH, self.users_list_item.format(UserData.user_group)))
        time.sleep(1)
        self.select_application_and_forms(UserData.reassign_cases_application,
                                          list(UserData.reasign_modules_forms.keys())[1],
                                          UserData.reasign_modules_forms[
                                              list(UserData.reasign_modules_forms.keys())[1]][0])
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
        subject = UserData.email_red_report
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
        assert self.is_visible_and_displayed(self.email_success_message), "Email report not sent successfully"
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

    def red_users_active(self):
        self.wait_to_click(self.red_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.RED_TITLE in self.driver.title, "This is not the Worker Activity page."
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
        self.select_application_and_forms(UserData.reassign_cases_application,
                                          list(UserData.reasign_modules_forms.keys())[1],
                                          UserData.reasign_modules_forms[
                                              list(UserData.reasign_modules_forms.keys())[1]][0])

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
        assert not self.is_present((By.XPATH, self.result_rows_names.format(
            UserData.deactivated_user))), "Deactivated user " + UserData.deactivated_user + " is present in the active worker list."
        print("All Active users are present")

    def red_users_deactivated(self):
        self.wait_to_click(self.red_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.RED_TITLE in self.driver.title, "This is not the Worker Activity page."
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
        self.select_application_and_forms(UserData.reassign_cases_application,
                                          list(UserData.reasign_modules_forms.keys())[1],
                                          UserData.reasign_modules_forms[
                                              list(UserData.reasign_modules_forms.keys())[1]][0])

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
        assert self.is_present((By.XPATH, self.result_rows_names.format(
            UserData.deactivated_user))), "Deactivated user " + UserData.deactivated_user + " is not present in the Deactivated worker list."
        print("All Deactivated users are present")

    def verify_assigned_cases_count(self, actives, totals):
        print("Sleeping for some time for the cases to be assigned")
        time.sleep(60)
        self.wait_to_click(self.red_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.RED_TITLE in self.driver.title, "This is not the Worker Activity page."
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
            assert int(actives[i]) - 10 == actives_new[i], "Active Cases not reduced"
            print("Active cases reduced")
        for i in range(len(totals_new)):
            assert int(totals[i]) - 10 == totals_new[i], "Active Cases not reduced"
            print("Active cases reduced")
        print("Cases successfully assigned")

    def filter_dates_and_verify(self, filter):
        self.wait_to_click(self.red_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.RED_TITLE in self.driver.title, "This is not the Worker Activity page."
        self.verify_user_lookup_table()
        self.remove_default_users()
        self.send_keys(self.users_field, UserData.user_group)
        self.wait_to_click((By.XPATH, self.users_list_item.format(UserData.user_group)))
        time.sleep(1)
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
            time.sleep(1)
            self.js_click((By.XPATH, self.result_rows_names.format(items)))
            time.sleep(15)
            self.wait_for_element(self.submit_history_table_title)
            self.wait_for_element(self.result_table, 300)
            assert self.is_visible_and_displayed(self.report_content_id, 120), "Report not loaded"
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
            time.sleep(2)
            # info = self.get_text(self.submit_history_table_info)
            # print(info)
            # info = str(info).split(" ")
            # print("Total records: ", info[-2])
            # assert count == info[-2], "Form counts not matching"
            # print("Form Count matching")
            # if count == '0':
            #     assert self.is_present(self.empty_table)
            #     print("Correct value displayed")
            time.sleep(5)
            self.driver.back()

    def advanced_options(self):
        self.wait_to_click(self.red_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.RED_TITLE in self.driver.title, "This is not the Worker Activity page."
        self.wait_for_element(self.apply_id, 100)
        self.verify_user_lookup_table()
        self.remove_default_users()
        self.send_keys(self.users_field, UserData.daily_form_groups[0])
        self.wait_to_click((By.XPATH, self.users_list_item.format(UserData.daily_form_groups[0])))
        time.sleep(1)
        self.wait_to_click(self.show_adv_options)
        assert self.is_selected(self.show_adv_options), "Show Advanced Options is not selected"
        print("Show Advanced Option is successfully selected")
        time.sleep(2)
        assert self.is_present(self.known_forms), "Known Forms option not present"
        assert self.is_present(self.unknown_forms), "Unknown Forms option not present"
        assert self.is_present(self.application_type_dropdown), "Application Type dropdown not present"
        active_apps, deleted_apps = self.known_forms_options()
        self.unknown_forms_options(active_apps, deleted_apps)
        self.wait_to_click(self.show_adv_options)
        assert not self.is_selected(self.show_adv_options), "Show Advanced Options is still selected"
        time.sleep(2)
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
        time.sleep(2)
        assert not self.is_visible_and_displayed(self.application_dropdown, 10), "Application dropdown is still present"
        print("Application dropdown successfully disappeared after selecting option ", UserData.app_type_list[0])
        self.select_by_text(self.application_type_dropdown, UserData.app_type_list[2])
        time.sleep(2)
        assert self.is_present(self.application_dropdown), "Application dropdown is not present"
        list_app_active = self.get_all_dropdown_options(self.application_dropdown)
        for items in list_app_active[1:]:
            assert "[Deleted Application]" in items, "Not a Deleted Application option"
        print("All Deleted Application present")
        self.select_by_text(self.application_type_dropdown, UserData.app_type_list[1])
        time.sleep(2)
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

        assert self.is_visible_and_displayed(self.unknown_form_dropdown), "Unknown forms dropdown is not present"
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
                    string = app + " > " + m + " > " + f
                    column_list.append(string)
        elif mod != None and forms == None:
            for f in list(UserData.reasign_modules_forms[mod]):
                string = app + " > " + mod + " > " + f
                column_list.append(string)
        else:
            string = app + " > " + mod + " > " + forms
            column_list.append(string)
        print(column_list)
        return column_list

    def form_column_verification(self, app, mod=None, form=None):
        self.wait_to_click(self.red_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.RED_TITLE in self.driver.title, "This is not the Worker Activity page."
        self.verify_user_lookup_table()
        self.remove_default_users()
        self.send_keys(self.users_field, UserData.user_group)
        self.wait_to_click((By.XPATH, self.users_list_item.format(UserData.user_group)))
        time.sleep(1)
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
        time.sleep(2)
        self.wait_to_click(self.apply_id)
        time.sleep(10)
        self.wait_for_element(self.result_table, 300)
        assert self.is_visible_and_displayed(self.report_content_id, 120), "Report not loaded"
        print("Report loaded successfully!")
        self.scroll_to_bottom()
        self.verify_users_in_the_group()
        for items in column_list:
            assert self.is_present(
                (By.XPATH, self.app_mod_form_column.format(items))), "Form Name Column not present: " + column_name

    def verify_submission_form_type(self, form):
        self.wait_to_click(self.red_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.RED_TITLE in self.driver.title, "This is not the Worker Activity page."
        self.wait_to_click((By.XPATH, self.submit_form_type.format(form)))
        assert self.is_visible_and_displayed((By.XPATH, self.form_type_selected.format(form)))
        time.sleep(1)
        self.wait_to_click(self.apply_id)
        time.sleep(10)
        self.wait_for_element(self.result_table, 300)
        assert self.is_visible_and_displayed(self.report_content_id, 120), "Report not loaded"
        print("Report loaded successfully!")
        assert self.is_visible_and_displayed((By.XPATH, self.form_type_selected_after.format(form)))
        self.scroll_to_bottom()
        if self.is_visible_and_displayed(self.empty_table, 10):
            print("No data to display for Submission type: ", form)
        else:
            error_type = self.find_elements(self.error_type_column_list)
            for items in error_type:
                assert form in items.text, "Incorrect Error type is present"
            print("Correct Error type present for: ", form)

    def verify_submission_form_type_all(self):
        self.wait_to_click(self.red_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.RED_TITLE in self.driver.title, "This is not the Worker Activity page."
        for item in UserData.submit_form_type:
            self.wait_to_click((By.XPATH, self.submit_form_type.format(item)))
            assert self.is_visible_and_displayed((By.XPATH, self.form_type_selected.format(item)))
        time.sleep(1)
        self.wait_to_click(self.apply_id)
        time.sleep(10)
        self.wait_for_element(self.result_table, 300)
        assert self.is_visible_and_displayed(self.report_content_id, 120), "Report not loaded"
        print("Report loaded successfully!")
        for item in UserData.submit_form_type:
            assert self.is_visible_and_displayed((By.XPATH, self.form_type_selected_after.format(item)))
        if self.is_visible_and_displayed(self.empty_table, 20):
            print("No data to display for any of the Submission types")
        else:
            error_type = self.find_elements(self.error_type_column_list)
            for items in error_type:
                text = items.text
                words = text.lower().split()
                check = any(map(lambda element: any(word in element.lower() for word in words), UserData.submit_form_type))
                assert check is True, "Incorrect Error type is present"
                print("Correct Error type present for: ", items.text)

    def view_form_update(self):
        self.wait_to_click(self.red_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.RED_TITLE in self.driver.title, "This is not the Raw Forms, Errors & Duplicates page."
        self.wait_to_click((By.XPATH, self.submit_form_type.format(UserData.submit_form_type[0])))
        time.sleep(1)
        self.select_application_and_forms(UserData.reassign_cases_application,
                                          list(UserData.reasign_modules_forms.keys())[1],
                                          UserData.reasign_modules_forms[
                                              list(UserData.reasign_modules_forms.keys())[1]][2])
        time.sleep(2)
        self.wait_to_click(self.apply_id)
        time.sleep(10)
        self.wait_for_element(self.result_table, 300)
        assert self.is_visible_and_displayed(self.report_content_id, 120), "Report not loaded"
        print("Report loaded successfully!")
        self.wait_to_click(self.view_form_column_first)
        # self.switch_to_next_tab()
        time.sleep(10)
        assert self.is_visible_and_displayed(self.form_data_table, 200), "data Table for user is not present"
        for items in UserData.view_form_tabs:
            assert self.is_present((By.XPATH, self.view_form_tabs.format(items))), "Tab " + items + " is not present"
        print("View Form page is successfully loaded")
        assert self.is_present(self.clean_form_submission), "Clean Form Submission button is not present"
        assert self.is_present(self.archive_this_form), "Archive this form button is not present"
        assert self.is_present(self.form_table_case_name), "Case name is not present"

        old_text = self.get_text(self.form_table_case_name)
        print("Current Case name: ", old_text)

        self.click(self.clean_form_submission)
        time.sleep(3)
        self.wait_for_element(self.clean_form_save)
        assert self.is_visible_and_displayed(self.clean_form_save), "Clean Form Submission Save button not present"
        assert self.is_visible_and_displayed(self.clean_form_cancel), "Clean Form Submission Cancel button not present"
        assert self.is_visible_and_displayed(self.clean_form_submission_title), "Clean Form Submission Title not present"
        assert self.is_present(self.clean_form_input_field), "Form input field is not present"

        assert old_text == self.get_attribute(self.clean_form_input_field, "value"), "Input field value does not match the "
        self.wait_to_clear_and_send_keys(self.clean_form_input_field, old_text+"_updated")
        time.sleep(2)
        new_text =self.get_attribute(self.clean_form_input_field, "value")
        print("Updated Case name: ", new_text)

        self.wait_to_click(self.clean_form_save)
        time.sleep(3)
        self.wait_for_element(self.form_table_case_name)
        assert not self.is_visible_and_displayed(
            self.clean_form_submission_title), "Clean Form Submission Title is still present"
        assert new_text == self.get_text(self.form_table_case_name), "Case name is not updated"
        print("Case name successfully updated")

        self.click(self.archive_this_form)
        self.wait_for_element(self.restore_this_form, 100)
        assert not self.is_visible_and_displayed(self.archive_this_form, 10)
        assert self.is_present(self.archive_success_msg)
        assert self.is_present(self.undo_archive)
        assert self.is_present(self.restore_this_form)
        assert self.is_present(self.delete_this_form)

        self.click(self.undo_archive)
        self.wait_for_element(self.archive_this_form, 100)
        assert not self.is_visible_and_displayed(self.restore_this_form, 10)
        assert not self.is_visible_and_displayed(self.delete_this_form, 10)
        assert self.is_present(self.restore_success_msg)
        assert self.is_present(self.archive_this_form)

        self.click(self.clean_form_submission)
        time.sleep(3)
        self.wait_for_element(self.clean_form_save)
        assert self.is_visible_and_displayed(self.clean_form_save), "Clean Form Submission Save button not present"
        assert self.is_visible_and_displayed(self.clean_form_cancel), "Clean Form Submission Cancel button not present"
        assert self.is_visible_and_displayed(
            self.clean_form_submission_title), "Clean Form Submission Title not present"
        assert self.is_present(self.clean_form_input_field), "Form input field is not present"

        assert new_text == self.get_attribute(self.clean_form_input_field,
                                              "value"), "Input field value does not match the "
        self.wait_to_clear_and_send_keys(self.clean_form_input_field, old_text)
        time.sleep(2)
        self.wait_to_click(self.clean_form_save)
        time.sleep(3)
        self.wait_for_element(self.form_table_case_name)
        assert not self.is_visible_and_displayed(
            self.clean_form_submission_title), "Clean Form Submission Title is still present"
        assert old_text == self.get_text(self.form_table_case_name), "Case name is not updated"
        print("Case name successfully updated")
