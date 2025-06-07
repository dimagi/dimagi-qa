import html
import os
import time

import dateutil.relativedelta
import pandas as pd

from datetime import datetime, timedelta, date
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from natsort import natsorted, humansorted
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


class CaseListExplorerPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

        #queries
        self.query1 = "last_modified=today()"
        self.query2 = "starts-with(case_name, 'text') and @case_type='reassign_change'"
        self.proj_setting = "https://staging.commcarehq.org/a/qa-automation/settings/project/basic/"

        self.default_timezone = (By.XPATH, "//select[@id='id_default_timezone']")
        self.update_basic_info = (By.XPATH, "//button[@class='btn btn-primary'][.='Update Basic Info']")
        self.proj_setting_saved = (By.XPATH, "//div[contains(@class,'alert-success')][contains(.,'Project settings saved!')]")
        # Mobile Worker Reports
        self.reports_menu_id = (By.ID, "ProjectReportsTab")
        self.case_list_explorer_rep = (By.LINK_TEXT, "Case List Explorer")
        self.case_list_explorer_TITLE = "Case List Explorer - CommCare HQ"

        # Report Elements
        self.apply_id = (By.ID, "apply-filters")
        self.report_content_id = (By.ID, "report-content")
        self.homepage = (By.XPATH, ".//a[@href='/homepage/']")
        self.date_range_error = (By.XPATH, "//td[contains(.,'You are limited to a span of 90 days,')]")
        self.report_loading = (By.XPATH, "//div[@id='report_table_case_list_explorer_processing'][@style='display: block;']")
        self.column_editor = (By.XPATH, "//a[@href='#columns-editor']")
        self.add_property = (By.XPATH, "//button[@data-bind='click: addProperty']")
        self.properties_input = (By.XPATH, "//tbody[contains(@data-bind,'properties')]//td//input[contains(@data-bind,'Properties')]")
        self.value_input = (By.XPATH, "//tbody[contains(@data-bind,'properties')]//td//input[contains(@data-bind,'value: label')]")
        self.delete_property = (By.XPATH, "//tbody[contains(@data-bind,'properties')]//td[4]")
        self.last_properties_input = (
        By.XPATH, "(//tbody[contains(@data-bind,'properties')]//td//input[contains(@data-bind,'Properties')])[last()]")
        self.last_value_input = (
        By.XPATH, "(//tbody[contains(@data-bind,'properties')]//td//input[contains(@data-bind,'value: label')])[last()]")
        self.last_delete_property = (By.XPATH, "(//tbody[contains(@data-bind,'properties')]//td[4]/i)[last()]")

        self.form_activity_results = (By.XPATH, "//table[@id='report_table_case_list_explorer']/tbody/tr")
        self.form_activity_results_cells = (By.XPATH, "//table[@id='report_table_case_list_explorer']/tbody/tr/td")
        self.users_field = (By.XPATH, "(//textarea[@class='select2-search__field'])[1]")
        self.no_results = (By.XPATH, "//li[.='No results found']")
        self.filter_dates_by = (By.XPATH, "//select[@id='report_filter_sub_time']")
        self.remove_buttons = (By.XPATH, "//ul//button")
        self.custome_remove_button = "//span[contains(.,'{}')]//preceding-sibling::button[@class='select2-selection__choice__remove']"
        self.user_remove_btn = (By.XPATH, "(//button[@class='select2-selection__choice__remove'])[last()]")
        self.user_from_list = "//li[contains(.,'{}')]"
        self.export_to_excel = (By.XPATH, "//a[@id='export-report-excel']")
        self.export_success = (By.XPATH,
                               "//span[.='Your requested Excel report will be sent to the email address defined in your account settings.']")
        self.user_column = (
        By.XPATH, "(//thead/tr/th[@aria-controls='report_table_case_list_explorer']/div[contains(.,'Username')])[1]")
        self.group_column = (
        By.XPATH, "(//thead/tr/th[@aria-controls='report_table_case_list_explorer']/div[contains(.,'Group')])[1]")
        self.total_column = (By.XPATH, "(//thead/tr/th[@aria-controls='report_table_case_list_explorer']/div[contains(.,'Total')])[1]")
        self.users_list_item = "//ul[@role='listbox']/li[contains(.,'{}')]"
        self.users_list = (By.XPATH, "//ul[contains(@class,'select2-results__options')]/li")
        self.users_list_empty = (
        By.XPATH, "//ul[contains(@id,'select2-emw-bi-results')]/li[.='The results could not be loaded.']")

        self.column_names = "(//thead/tr/th[@aria-controls='report_table_case_list_explorer'][contains(@aria-label,'{}')])[1]"
        self.column_group_names = (By.XPATH, "(//thead)[1]/tr/th/div")
        self.result_table = (By.XPATH, "(//div[@id='report-content']//table//tbody//td[1])[1]")
        self.results_rows = (By.XPATH, "//tbody/tr/td[3]")
        self.result_rows_names = "//tbody/tr/td[2][contains(.,'{}')]"
        self.hide_filters_options = (By.XPATH, "//a[.='Hide Filter Options']")
        self.show_filters_options = (By.XPATH, "//a[.='Show Filter Options']")
        self.user_sort = "(//text()[contains(.,'{}')][not(contains(.,'View Form'))]//preceding-sibling::i[@class='icon-white fa dt-sort-icon'])[1]"
        self.column_name_headers = "//table[@id='report_table_case_list_explorer']//thead//th/div/div[contains(.,'{}')]"
        self.case_type_column_list = (By.XPATH, "//table[@id='report_table_case_list_explorer']//tbody//td[2]")
        self.case_name_column_list = (By.XPATH, "//table[@id='report_table_case_list_explorer']//tbody//td[3]")
        self.last_modified_list = (By.XPATH, "//table[@id='report_table_case_list_explorer']//tbody//td[4]")
        self.view_form_column_list = (By.XPATH, "//table[@id='report_table_submit_history']//tbody//td[1]/a")
        self.view_form_column_first = (By.XPATH, "(//table[@id='report_table_submit_history']//tbody//td[1]/a)[1]")
        self.status_column_list = (By.XPATH, "//table[@id='report_table_case_list']//tbody//td[5]")
        self.status_column_first = (By.XPATH, "(//table[@id='report_table_case_list']//tbody//td[5])[1]")

        self.case_type_dropdown = (By.XPATH, "//select[@id='report_filter_case_type']")
        self.case_type_field = (By.XPATH, "//span[contains(@id, 'report_filter_case_type-container')]")
        self.case_type_input = (By.XPATH, "//input[contains(@aria-controls,'report_filter_case_type-result')]")
        self.open_close_dropdown = (By.XPATH, "//select[@id='report_filter_is_open']")
        self.open_close_field = (By.XPATH, "//span[contains(@id, 'report_filter_is_open-container')]")
        self.open_close_input = (By.XPATH, "//input[contains(@aria-controls,'report_filter_is_open-result')]")
        self.search_input = (By.XPATH, "//div[@class='report-filter-xpath-textarea']//textarea")
        self.search_textarea_div = (By.XPATH, "(//div[@id='group_search_xpath']/div/div[2]/pre/div[2]/div)[2]")

        self.view_form_tabs = "//li/a[contains(.,'{}')]"
        self.form_data_table = (By.XPATH, "//table[contains(@class,'form-data-table')]")
        self.archive_this_form = (By.XPATH, "//button[contains(.,'Archive this form')]")
        self.restore_this_form = (By.XPATH, "//button[contains(.,'Restore this form')]")
        self.delete_this_form = (By.XPATH, "//button[contains(.,'Delete this form')]")
        self.delete_confirm_button = (By.XPATH, "//div[@class='modal-footer']/*[contains(@class,'btn btn-danger')]")
        self.delete_case_confirm = (By.XPATH, "//*[@data-target='#delete_case_confirmation']")
        self.case_text = (By.XPATH, "//p[contains(.,'delete this form, type')]/strong")
        self.textarea_delete_popup = (
        By.XPATH, "//p[contains(.,'delete this form, type')][./strong]//following-sibling::textarea")
        self.archive_success_msg = (
        By.XPATH, "//div[contains(@class,'alert-margin-top')][contains(.,'Form was successfully archived')]")
        self.restore_success_msg = (
            By.XPATH, "//div[contains(@class,'alert-margin-top')][contains(.,'Form was successfully restored')]")

        # Pagination
        self.page_list_dropdown = (By.XPATH, "//select[@name='report_table_case_list_explorer_length']")
        self.table_info = (By.XPATH, "//div[@id='report_table_case_list_explorer_info']")
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

        # Case Type Verify
        self.case_created_column = (By.XPATH, "//table[@id='report_table_case_list_explorer']//tbody//td[5]//a")
        self.case_created_title = (By.XPATH, "//table[@id='report_table_case_list_explorer']//tbody//td[5]//span")
        self.case_list_explorer_table = (By.XPATH, "//table[@id='report_table_case_list_explorer']/tbody/tr/td[1]")
        self.case_list_explorer_table_title = (By.XPATH, "//h2[@class='panel-title'][contains(.,'Case List Explorer')]")
        self.case_list_explorer_table_info = (By.XPATH, "//div[@id='report_table_case_list_explorer_info']")
        self.case_list_explorer_page_dropdown = (By.XPATH, "//select[@name='report_table_case_list_explorer_length']")

        # Email report
        self.email_report_btn = (By.XPATH, "//a[@id='email-report']")
        self.email_subject_field = (By.XPATH, "//input[@id='id_subject']")
        self.email_form_cancel_btn = (By.XPATH, "//input[@id='button-id-close']")
        self.send_email_btn = (By.XPATH, "//input[@id='submit-id-submit_btn']")
        self.email_success_message = (By.XPATH, "//*[.='Report successfully emailed']")

        # Case List Explorer Verification
        self.total_form_counts = "//td[contains(.,'{}')]//following-sibling::td[last()]"
        self.filter_column_name = "(//thead//th[@aria-controls='report_table_case_list_explorer'][3]/div[contains(.,'{}')])[1]"
        self.case_list_explorer_table_info = (By.XPATH, "//div[@id='report_table_case_list_explorer_info']")
        self.empty_table = (By.XPATH, "//tr/td[contains(.,'No data available to display.')]")
        self.case_list_explorer_table_title = (By.XPATH, "//h2[@class='panel-title'][contains(.,'Case List Explorer')]")
        self.panel_body_text = (By.XPATH, "//div[@class='panel-body-datatable']")

        # Case Data values
        self.case_property_tab = (By.XPATH, "//a[@href = '#properties']")
        self.case_history_tab = (By.XPATH, "//a[@href = '#history']")
        self.CASE_DATA_TITLE = "Case Data : Project Reports :: - CommCare HQ"
        self.case_data_property_values = "//th[contains(.,'{}')]//following-sibling::td[1]"
        self.case_data_history_values = "//td[./span[contains(@data-bind,'text: {}')]]"
        self.download_case_history = (By.XPATH, "//i[contains(@class,'fa-cloud-arrow-down')]")
        self.close_case = (By.XPATH, "//button[.//text()[contains(.,'Close Case')]]")
        self.close_success_msg = "//div[contains(@class,'alert-success')][./text()[contains(.,'Case {} has been closed')]]"

    def verify_page(self):
        self.wait_to_click(self.case_list_explorer_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.case_list_explorer_TITLE in self.driver.title, "This is not the Case List Explorer page."
        text = self.get_text(self.panel_body_text)
        print(text)
        assert "Why can't I see any data?" in text
        assert "Please choose your filters above and click Apply to see report data." in text

    def hide_filters(self):
        self.wait_to_click(self.case_list_explorer_rep)
        self.wait_for_element(self.hide_filters_options)
        self.click(self.hide_filters_options)
        
        assert not self.is_visible_and_displayed(self.users_field, 10), "Case owner field is still present"
        assert not self.is_visible_and_displayed(self.case_type_dropdown, 10), "Application dropdown is still present"
        assert not self.is_visible_and_displayed(self.open_close_dropdown,
                                                 10), "Open / Closed dropdown is still present"
        assert not self.is_visible_and_displayed(self.column_editor, 10), "Edit Column link is still present"
        assert not self.is_visible_and_displayed(self.search_input, 10), "Search input field is still present"
        assert self.is_present(self.show_filters_options), "Show Filters Options is not present"
        print("All filters are hidden!")

    def show_filters(self):
        self.wait_for_element(self.show_filters_options)
        self.click(self.show_filters_options)
        
        assert self.is_present(self.users_field), "Case owner field is not present"
        assert self.is_present(self.case_type_dropdown), "Application dropdown is not present"
        assert self.is_present(self.open_close_dropdown), "Open / Closed dropdown is not present"
        assert self.is_present(self.search_input), "Search input field is not present"
        assert self.is_present(self.column_editor), "Edit Column link is not present"
        assert self.is_present(self.hide_filters_options), "Show Filters Options is not present"
        print("All filters are shown!")

    def verify_case_list_explorer_page_fields_columns(self):
        self.wait_to_click(self.case_list_explorer_rep)
        time.sleep(2)
        self.wait_for_element(self.apply_id, 100)
        assert self.case_list_explorer_TITLE in self.driver.title, "This is not the Case List Explorer page."
        assert self.is_present(self.users_field), "User field is not present"
        assert self.is_present(self.case_type_dropdown), "Application dropdown is not present"
        assert self.is_present(self.open_close_dropdown), "Open / Closed dropdown is not present"
        assert self.is_present(self.search_input), "Search input field is not present"
        assert self.is_present(self.column_editor), "Edit Column link is not present"
        assert self.is_present(self.apply_id), "Apply button is not present"
        assert self.is_present(self.favorite_button), "Favorite button is not present"
        assert self.is_present(self.save_config_button), "Save button is not present"
        assert self.is_present(self.hide_filters_options), "Show Filters Options is not present"
        text = self.get_selected_text(self.case_type_dropdown)
        list_case = self.get_all_dropdown_options(self.case_type_dropdown)
        print(text)
        assert UserData.default_case_list_dropdown[0] in text, "Values mismatch: " + text + " and " + \
                                                         UserData.default_case_list_dropdown[0]
        assert UserData.case_pregnancy in list_case, "Required Case Type is not present in the dropdown"
        self.select_by_value(self.case_type_dropdown, UserData.case_reassign)
        text = self.get_selected_text(self.open_close_dropdown)
        print(text)
        assert UserData.default_case_list_dropdown[1] in text, "Values mismatch: " + text + " and " + \
                                                               UserData.default_case_list_dropdown[1]
        self.verify_dropdown_options(self.open_close_dropdown, UserData.open_close_options)
        self.verify_user_lookup_table()
        self.remove_default_users()
        self.send_keys(self.users_field, fetch_random_string())
        
        assert self.is_present(self.no_results), "No results not displayed"
        self.clear(self.users_field)
        self.send_keys(self.users_field, UserData.user_group)
        self.wait_to_click((By.XPATH, self.users_list_item.format(UserData.user_group)))
        
        self.wait_to_click(self.apply_id)
        assert self.is_present(self.report_loading), "Loading Report block is not present"
        time.sleep(2)
        self.wait_for_element(self.result_table, 300)
        self.wait_for_element(self.report_content_id, 120)
        print("Report loaded successfully!")
        self.scroll_to_bottom()
        self.verify_users_in_the_group()
        assert self.is_present(self.page_list_dropdown), "Page list dropdown not present"
        assert self.is_present(self.next_page_button), "Next page button not present"
        pages = self.find_elements(self.pagination_page_numbers)
        assert len(pages) > 0, "Number of pages not present"
        list_col = self.find_elements(self.column_group_names)
        for item in list_col:
            text = item.text
            print(text)
            assert text in UserData.cle_column_names, "Column not present"
            print(text, " is present!")
        case_list_explorer = self.find_elements(self.case_type_column_list)
        links = self.find_elements(self.view_form_column_list)
        for items in links:
            assert "View Form" == items.text, "View Form link is not present"
        for items in case_list_explorer:
            assert UserData.case_reassign == items.text, "Case type is not matching"


    def verify_user_lookup_table(self):
        self.wait_to_click(self.users_field)
        
        assert not self.is_visible_and_displayed(self.users_list_empty, 10), "Case Type List is not empty"
        list = self.find_elements(self.users_list)
        print(len(list))
        assert int(len(list)) >= 1
        print("A Look up for Case type is successfully loaded")

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
            for items in list:
                text = items.text
                assert (ele in text for ele in UserData.automation_group_users), "User " + text + " is not part of the selected group."
                print("User " + text + " is part of the selected group.")

    def verify_users_used_in_the_group(self, user_names):
        list = self.find_elements(self.status_column_list)
        if len(list) > 0:
            for items in list:
                text = items.text
                assert (ele in text for ele in user_names), "User " + text + " is not part of the selected group."
                print("User " + text + " is part of the selected group.")

    def verify_users_used_not_in_the_group(self, user_names):
        list_users = self.find_elements(self.status_column_list)
        text_list = list()
        if len(list_users) > 0:
            for items in list_users:
                text = items.text
                text_list.append(text)
        check = any(item in user_names for item in text_list)
        assert check is False, "User is still present"
        print("Following User(s) not present: ", user_names)

    def case_list_explorer_pagination_list(self):
        self.wait_to_click(self.case_list_explorer_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.case_list_explorer_TITLE in self.driver.title, "This is not the Case List Explorer page."
        self.select_by_value(self.case_type_dropdown, UserData.case_pregnancy)
        # self.select_by_text(self.open_close_dropdown, UserData.open_close_options[1])
        self.verify_user_lookup_table()
        self.remove_default_users()
        self.clear(self.users_field)
        self.send_keys(self.users_field, UserData.user_group)
        self.wait_to_click((By.XPATH, self.users_list_item.format(UserData.user_group)))
        # self.wait_to_click(self.search_textarea_div)
        # self.send_keys(self.search_input, "case_name!='' and last_modified>'2024-01-01'")
        
        self.wait_to_click(self.apply_id)
        time.sleep(2)
        self.wait_for_element(self.result_table, 300)
        self.wait_for_element(self.report_content_id, 120)
        print("Report loaded successfully!")
        self.scroll_to_element(self.result_table)
        # self.select_by_value(self.page_list_dropdown, UserData.pagination[3])
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
            list1 = self.find_elements(self.case_name_column_list)
            list1_names = list()
            for item in list1:
                list1_names.append(item.text)
            self.wait_to_click(self.next_page_button)
            time.sleep(2)
            list2 = self.find_elements(self.case_name_column_list)
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
            list3 = self.find_elements(self.case_name_column_list)
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
        if "case_type" in col_name:
            list1 = self.find_elements(self.case_type_column_list)
        elif "case_name" in col_name:
            list1 = self.find_elements(self.case_name_column_list)
        elif "last_modified" in col_name:
            list1 = self.find_elements(self.last_modified_list)
        else:
            print("Invalid Column Name")
        list1_names = list()
        for item in list1:
            list1_names.append(item.text)
        if "last_modified" in col_name:
            list1_names = [sub.replace(' IST', '') for sub in list1_names]
            print(list1_names)
            sorted_list = sorted(list1_names,
                                 key=lambda list1_names: datetime.strptime(list1_names, "%b %d, %Y %H:%M:%S"))
        # elif "case_name" in col_name:
        #     sorted_list = humansorted(list1_names)
        else:
            sorted_list = sorted(list1_names)
        print(list1_names)
        print(sorted_list)
        assert list1_names == sorted_list, "List is not sorted"
        print("List is in ascending order")
        self.wait_to_click((By.XPATH, self.user_sort.format(col_name)))
        time.sleep(15)
        if "case_type" in col_name:
            list2 = self.find_elements(self.case_type_column_list)
        # elif "case_name" in col_name:
        #     list2 = self.find_elements(self.case_name_column_list)
        elif "last_modified" in col_name:
            list2 = self.find_elements(self.last_modified_list)
        else:
            print("Invalid Column Name")
        list2_names = list()
        for item in list2:
            list2_names.append(item.text)
        if "last_modified" in col_name:
            list1_names = [sub.replace(' IST', '') for sub in list1_names]
            list2_names = [sub.replace(' IST', '') for sub in list2_names]
            print(list1_names)
            rev_list = sorted(list1_names, reverse=True,
                                 key=lambda list1_names: datetime.strptime(list1_names, "%b %d, %Y %H:%M:%S"))
        elif "case_name" in col_name:
            rev_list = humansorted(list1_names, reverse=True)
        else:
            rev_list = sorted(list1_names, reverse=True)
        print(list2_names)
        print(rev_list)
        assert list2_names == rev_list, "List is not sorted"
        print("List is in descending order")



    def verify_pagination_dropdown(self):
        info = self.get_text(self.table_info)
        info = str(info).split(" ")
        print("Total records: ", info[-2])
        for item in UserData.pagination:
            self.select_by_value(self.page_list_dropdown, item)
            time.sleep(15)
            list_rows = self.find_elements(self.case_name_column_list)
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

    def get_custom_dates_past(self, days, months, years):
        presentday = datetime.now()  # or presentday = datetime.today()
        pastday = presentday - relativedelta(days=days, months=months, years=years)
        return str(pastday.strftime('%Y-%m-%d') + " to " + presentday.strftime('%Y-%m-%d')), pastday.strftime(
            '%Y-%m-%d'), presentday.strftime('%Y-%m-%d')

    def case_list_explorer_date_range(self):
        date_string = start_date = end_date = ''
        self.wait_to_click(self.case_list_explorer_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.case_list_explorer_TITLE in self.driver.title, "This is not the Case List Explorer page."
        self.select_by_text(self.filter_dates_by, UserData.filter_dates_by[0])
        self.wait_to_click(self.date_input)
        time.sleep(3)
        self.wait_to_click(self.date_input)
        for item in UserData.date_range:
            if item == UserData.date_range[0]:
                date_string, start_date, end_date = self.value_date_range_7_days()
            elif item == UserData.date_range[1]:
                date_string, start_date, end_date = self.value_date_range_last_month()
            elif item == UserData.date_range[2]:
                date_string, start_date, end_date = self.value_date_range_30_days()
            elif item == UserData.date_range[3]:
                date_string, start_date, end_date = self.get_custom_dates_past(20, 0, 0)
            else:
                print("Invalid date range")
            self.wait_to_click(self.date_input)
            self.wait_to_click((By.XPATH, self.date_range_type.format(item)))
            if item == UserData.date_range[3]:
                self.select_date_from_picker(start_date, end_date)
            text = self.get_attribute(self.date_input, "value")
            print(text)
            assert text == date_string
        
        self.wait_to_click(self.apply_id)
        time.sleep(2)
        self.wait_for_element(self.result_table, 300)
        self.wait_for_element(self.report_content_id, 120)
        print("Report loaded successfully!")
        print("All date ranges are correctly updated in the date range field")


    def verify_dropdown_options(self, locator, list_to_compare):
        print("List to compare: ", list_to_compare)
        assert list_to_compare == self.get_all_dropdown_options(locator), "Dropdown does not have all the options"
        print("All module/form options are present in the dropdown")


    def case_list_explorer_save_report(self):
        self.wait_to_click(self.case_list_explorer_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.case_list_explorer_TITLE in self.driver.title, "This is not the Case List Explorer page."
        self.verify_user_lookup_table()
        self.remove_default_users()
        self.send_keys(self.users_field, UserData.user_group)
        self.wait_to_click((By.XPATH, self.users_list_item.format(UserData.user_group)))
        
        self.select_by_text(self.case_type_dropdown, UserData.case_reassign_change)
        self.select_by_text(self.open_close_dropdown, UserData.open_close_options[1])
        
        self.wait_to_click(self.apply_id)
        time.sleep(2)
        self.wait_for_element(self.result_table, 300)
        self.wait_for_element(self.report_content_id, 120)
        print("Report loaded successfully!")
        self.verify_users_in_the_group()
        time.sleep(2)
        report_name = "Saved Case List Explorer Report " + fetch_random_string()
        self.verify_favorite_empty(report_name)
        self.save_report_donot_save(report_name)
        report = self.save_report(report_name)
        self.wait_to_click(self.case_list_explorer_rep)
        self.wait_for_element(self.apply_id, 100)
        self.verify_favorite_created(report)
        time.sleep(2)
        self.verify_users_in_the_group()
        assert UserData.case_reassign_change in self.get_selected_text(self.case_type_dropdown)
        assert UserData.open_close_options[1] in self.get_selected_text(self.open_close_dropdown)
        print("Saved filters are selected")
        self.delete_saved_report(report)
        self.wait_to_click(self.case_list_explorer_rep)
        self.verify_favorite_empty(report_name)

    def verify_favorite_empty(self, report=None):
        self.scroll_to_element(self.favorite_button)
        self.wait_to_click(self.favorite_button)
        if report == None:
            self.wait_for_element(self.empty_fav_list)
        else:
            assert not self.is_visible_and_displayed((By.XPATH, self.saved_fav.format(report)),
                                                     30), "Favorite is already Present"
        print("No Favorites yet.")

    def verify_favorite_created(self, report):
        self.scroll_to_element(self.favorite_button)
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
        assert self.is_present(self.name_field)
        assert self.is_present(self.description_field)
        assert self.is_present(self.cancel_report_button)
        assert self.is_present(self.save_report_button)
        text = self.get_text(self.saved_report_title)
        print(text)
        assert report_name in text, "Report Name is visible in the Title"
        self.wait_to_click(self.cancel_report_button)
        
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
                    self.wait_for_element(self.case_list_explorer_table_title, 200)
                    self.scroll_to_bottom()
                    info = self.get_text(self.case_list_explorer_table_info)
                    info = str(info).split(" ")
                    print("Total records: ", info[-2])
                    assert info[-2] == text, "Case created count mismatch"
                    print("Cases created count matched")
                    self.select_by_value(self.case_list_explorer_page_dropdown, '100')
                    time.sleep(2)
                    cases = self.find_elements(self.case_list_explorer_table)
                    if len(cases) > 0:
                        for case in cases:
                            name = case.text
                            assert name == UserData.case_reassign, "Case Type mismatch"
                            print("Case Type matching")
                    
                    self.driver.close()
                    
                    self.switch_back_to_prev_tab()

    def export_case_list_explorer_to_excel(self):
        self.wait_to_click(self.case_list_explorer_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.case_list_explorer_TITLE in self.driver.title, "This is not the Case List Explorer page."
        self.verify_user_lookup_table()
        self.remove_default_users()
        self.send_keys(self.users_field, UserData.user_group)
        self.wait_to_click((By.XPATH, self.users_list_item.format(UserData.user_group)))
        
        self.select_by_text(self.case_type_dropdown, UserData.case_reassign)
        self.select_by_text(self.open_close_dropdown, UserData.open_close_options[2])
        
        self.wait_to_click(self.apply_id)
        time.sleep(2)
        self.wait_for_element(self.result_table, 300)
        self.wait_for_element(self.report_content_id, 120)
        print("Report loaded successfully!")
        self.select_by_value(self.page_list_dropdown, UserData.pagination[3])
        time.sleep(2)
        self.wait_to_click((By.XPATH, self.user_sort.format("last_modified")))
        time.sleep(2)
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
        time.sleep(2)
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
    def export_case_list_explorer_email(self):
        self.wait_to_click(self.case_list_explorer_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.case_list_explorer_TITLE in self.driver.title, "This is not the Case List Explorer page."
        self.verify_user_lookup_table()
        self.remove_default_users()
        self.send_keys(self.users_field, UserData.user_group)
        self.wait_to_click((By.XPATH, self.users_list_item.format(UserData.user_group)))
        
        self.select_by_text(self.case_type_dropdown, UserData.case_reassign)
        self.select_by_text(self.open_close_dropdown, UserData.open_close_options[2])
        
        self.wait_to_click(self.apply_id)
        time.sleep(2)
        self.wait_for_element(self.result_table, 300)
        self.wait_for_element(self.report_content_id, 120)
        print("Report loaded successfully!")
        self.select_by_value(self.page_list_dropdown, UserData.pagination[3])
        time.sleep(2)
        self.wait_to_click((By.XPATH, self.user_sort.format("last_modified")))
        time.sleep(2)
        self.wait_for_element(self.form_activity_results)
        col = self.find_elements(self.form_activity_results_cells)
        list = []
        for c in col:
            list.append(c.text)
        print(list)
        subject = UserData.email_case_list_explorer_report
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
        self.wait_for_element(self.email_success_message)
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

    def case_list_explorer_users_active(self):
        self.wait_to_click(self.case_list_explorer_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.case_list_explorer_TITLE in self.driver.title, "This is not the Case List Explorer page."
        self.wait_to_click(self.remove_active_worker)
        assert not self.is_present(self.remove_active_worker), "Active Mobile Worker is still not removed"
        print("Active Mobile Worker is removed successfully")
        self.reload_page()
        self.wait_for_element(self.apply_id, 100)
        self.verify_user_lookup_table()
        self.remove_default_users()
        self.send_keys(self.users_field, UserData.daily_form_groups[0])
        self.wait_to_click((By.XPATH, self.users_list_item.format(UserData.daily_form_groups[0])))
        
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
        assert not self.is_present((By.XPATH, self.result_rows_names.format(UserData.deactivated_user))), "Deactivated user " + UserData.deactivated_user + " is present in the active worker list."
        print("All Active users are present")



    def case_list_explorer_users_deactivated(self):
        self.wait_to_click(self.case_list_explorer_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.case_list_explorer_TITLE in self.driver.title, "This is not the Case List Explorer page."
        self.wait_to_click(self.remove_deactive_worker)
        assert not self.is_present(self.remove_deactive_worker), "Deactivated Mobile Worker is still not removed"
        print("Deactivated Mobile Worker is removed successfully")
        self.reload_page()
        self.wait_for_element(self.apply_id, 100)
        self.verify_user_lookup_table()
        self.remove_default_users()
        self.send_keys(self.users_field, UserData.daily_form_groups[1])
        self.wait_to_click((By.XPATH, self.users_list_item.format(UserData.daily_form_groups[1])))
        
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
        assert self.is_present((By.XPATH, self.result_rows_names.format(UserData.deactivated_user))), "Deactivated user " + UserData.deactivated_user + " is not present in the Deactivated worker list."
        print("All Deactivated users are present")


    def verify_assigned_cases_count(self, actives, totals):
        print("Sleeping for some time for the cases to be assigned")
        time.sleep(60)
        self.wait_to_click(self.case_list_explorer_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.case_list_explorer_TITLE in self.driver.title, "This is not the Case List Explorer page."
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
            assert int(actives[i])-10 == actives_new[i], "Active Cases not reduced"
            print("Active cases reduced")
        for i in range(len(totals_new)):
            assert int(totals[i])-10 == totals_new[i], "Active Cases not reduced"
            print("Active cases reduced")
        print("Cases successfully assigned")

    def filter_dates_and_verify(self, filter):
        self.wait_to_click(self.case_list_explorer_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.case_list_explorer_TITLE in self.driver.title, "This is not the Case List Explorer page."
        self.verify_user_lookup_table()
        self.remove_default_users()
        self.send_keys(self.users_field, UserData.user_group)
        self.wait_to_click((By.XPATH, self.users_list_item.format(UserData.user_group)))
        
        self.select_by_text(self.filter_dates_by, filter)
        self.wait_to_click(self.date_input)
        self.wait_to_click((By.XPATH, self.date_range_type.format(UserData.date_range[0])))
        date_string = self.get_attribute(self.date_input, "value")
        
        self.wait_to_click(self.apply_id)
        time.sleep(2)
        self.wait_for_element(self.result_table, 300)
        self.wait_for_element(self.report_content_id, 120)
        print("Report loaded successfully!")
        self.scroll_to_bottom()
        self.verify_users_in_the_group()
        assert self.is_present((By.XPATH, self.user_sort.format(filter))), "Column "+filter+" is not present"
        print("Column "+filter+" is present")

    def verify_users_selections(self):
        self.wait_to_click(self.case_list_explorer_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.case_list_explorer_TITLE in self.driver.title, "This is not the Case List Explorer page."
        length = self.add_new_property("owner_name", "Name of owner")
        self.verify_user_lookup_table()
        self.remove_default_users()
        self.send_keys(self.users_field, UserData.deactivated_user)
        self.wait_to_click((By.XPATH, self.users_list_item.format(UserData.deactivated_user)))
        
        self.send_keys(self.users_field, UserData.app_login)
        self.wait_to_click((By.XPATH, self.users_list_item.format(UserData.app_login)))
        
        self.select_by_text(self.case_type_dropdown, UserData.case_commcare)
        self.wait_to_click(self.apply_id)
        time.sleep(2)
        self.wait_for_element(self.result_table, 300)
        self.wait_for_element(self.report_content_id, 120)
        print("Report loaded successfully!")
        self.verify_users_used_in_the_group([UserData.app_login, UserData.deactivated_user])
        time.sleep(2)
        self.scroll_to_element((By.XPATH, self.custome_remove_button.format(UserData.deactivated_user)))
        self.click((By.XPATH, self.custome_remove_button.format(UserData.deactivated_user)))
        ActionChains(self.driver).send_keys(Keys.TAB).perform()
        
        self.wait_to_click(self.apply_id)
        time.sleep(2)
        self.wait_for_element(self.result_table, 300)
        self.wait_for_element(self.report_content_id, 120)
        print("Report loaded successfully!")
        self.verify_users_used_in_the_group([UserData.app_login])
        self.verify_users_used_not_in_the_group([UserData.deactivated_user])
        assert self.is_present((By.XPATH, self.column_names.format("Name of owner")))
        self.scroll_to_element(self.users_field)
        self.delete_last_added_property(length)
        self.wait_to_click(self.apply_id)
        time.sleep(2)
        self.wait_for_element(self.result_table, 300)
        self.wait_for_element(self.report_content_id, 120)
        print("Report loaded successfully!")
        assert not self.is_visible_and_displayed(self.status_column_first), "Owner column is not removed"

    def verify_group_selections(self):
        self.wait_to_click(self.case_list_explorer_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.case_list_explorer_TITLE in self.driver.title, "This is not the Case List Explorer page."
        length = self.add_new_property("owner_name", "Name of Owner")
        self.verify_user_lookup_table()
        self.remove_default_users()
        self.send_keys(self.users_field, UserData.user_group)
        self.wait_to_click((By.XPATH, self.users_list_item.format(UserData.user_group)))
        
        self.send_keys(self.users_field, UserData.deactivated_user)
        self.wait_to_click((By.XPATH, self.users_list_item.format(UserData.deactivated_user)))
        
        self.select_by_text(self.case_type_dropdown, UserData.case_commcare)
        self.wait_to_click(self.apply_id)
        time.sleep(2)
        self.wait_for_element(self.result_table, 300)
        self.wait_for_element(self.report_content_id, 120)
        print("Report loaded successfully!")
        self.verify_users_used_in_the_group([UserData.automation_group_users[0], UserData.automation_group_users[1], UserData.deactivated_user])
        time.sleep(2)
        self.scroll_to_element((By.XPATH, self.custome_remove_button.format(UserData.deactivated_user)))
        self.click((By.XPATH, self.custome_remove_button.format(UserData.deactivated_user)))
        ActionChains(self.driver).send_keys(Keys.TAB).perform()
        
        self.wait_to_click(self.apply_id)
        time.sleep(2)
        self.wait_for_element(self.result_table, 300)
        self.wait_for_element(self.report_content_id, 120)
        print("Report loaded successfully!")
        self.verify_users_used_in_the_group([UserData.automation_group_users[0], UserData.automation_group_users[1]])
        self.verify_users_used_not_in_the_group([UserData.deactivated_user])
        assert self.is_present((By.XPATH, self.column_names.format("Name of Owner")))
        self.scroll_to_element(self.users_field)
        self.delete_last_added_property(length)
        self.wait_to_click(self.apply_id)
        time.sleep(2)
        self.wait_for_element(self.result_table, 300)
        self.wait_for_element(self.report_content_id, 120)
        print("Report loaded successfully!")
        assert not self.is_visible_and_displayed(self.status_column_first), "Owner column is not removed"

    def report_filter_search_section(self):
        self.wait_to_click(self.case_list_explorer_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.case_list_explorer_TITLE in self.driver.title, "This is not the Case List Explorer page."
        self.wait_to_click(self.case_type_field)
        self.wait_for_element(self.case_type_input)
        self.send_keys(self.case_type_input, fetch_random_string())
        
        assert self.is_present(self.no_results), "No results not displayed"
        self.clear(self.case_type_input)
        self.send_keys(self.case_type_input, UserData.case_pregnancy)
        self.wait_to_click((By.XPATH, self.users_list_item.format(UserData.case_pregnancy)))
        
        assert UserData.case_pregnancy in self.get_selected_text(self.case_type_dropdown), "Case type is not selected"
        self.wait_to_click(self.open_close_field)
        self.wait_for_element(self.open_close_input)
        self.send_keys(self.open_close_input, fetch_random_string())
        
        assert self.is_present(self.no_results), "No results not displayed"
        self.clear(self.open_close_input)
        self.send_keys(self.open_close_input, UserData.open_close_options[1])
        self.wait_to_click((By.XPATH, self.users_list_item.format(UserData.open_close_options[1])))
        
        assert UserData.open_close_options[1] in self.get_selected_text(self.open_close_dropdown), "Open Close option is not selected"
        self.verify_user_lookup_table()
        self.remove_default_users()
        self.send_keys(self.users_field, fetch_random_string())
        
        assert self.is_present(self.no_results), "No results not displayed"
        self.clear(self.users_field)
        self.send_keys(self.users_field, UserData.user_group)
        self.wait_to_click((By.XPATH, self.users_list_item.format(UserData.user_group)))
        ActionChains(self.driver).send_keys(Keys.TAB).perform()
        print("All search filters are working fine")

    def verify_open_form_options(self, option):
        self.wait_to_click(self.case_list_explorer_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.case_list_explorer_TITLE in self.driver.title, "This is not the Case List Explorer page."
        length = self.add_new_property("@status")
        self.verify_user_lookup_table()
        self.remove_default_users()
        self.send_keys(self.users_field, UserData.web_user_email)
        self.wait_to_click((By.XPATH, self.users_list_item.format(UserData.web_user_email)))
        
        self.select_by_text(self.case_type_dropdown, UserData.case_reassign)
        self.select_by_text(self.open_close_dropdown, option)
        
        self.wait_to_click(self.apply_id)
        time.sleep(2)
        self.wait_for_element(self.result_table, 300)
        self.wait_for_element(self.report_content_id, 120)
        print("Report loaded successfully!")
        time.sleep(2)
        status_list = self.find_elements(self.status_column_list)
        case_list_explorer = self.find_elements(self.case_type_column_list)
        for items in case_list_explorer:
            assert UserData.case_reassign == items.text, "Case Type mismatch"
        if option == "Show All":
            for items in status_list:
                assert items.text in ["open", "closed"], "Status is neither Open nor Closed"
                print("Status is either Open or Closed")
        elif option == "Only Open":
            for items in status_list:
                assert items.text == "open", "Status is not Open"
                print("Status is Open")
        elif option == "Only Closed":
            for items in status_list:
                assert items.text == "closed", "Status is not Closed"
                print("Status is Closed")
        else:
            print("invalid option")
        self.scroll_to_element(self.users_field)
        self.delete_last_added_property(length)
        self.wait_to_click(self.apply_id)
        time.sleep(2)
        self.wait_for_element(self.result_table, 300)
        self.wait_for_element(self.report_content_id, 120)
        print("Report loaded successfully!")
        assert not self.is_visible_and_displayed(self.status_column_first), "Status column is not removed"

    def add_new_property(self, property, value=None):
        self.scroll_to_element(self.column_editor)
        self.wait_to_click(self.column_editor)
        props1 = self.find_elements(self.properties_input)
        value1 = self.find_elements(self.value_input)
        delete1 = self.find_elements(self.delete_property)
        assert len(props1) != 0, "Property fields not present"
        assert len(value1) != 0, "Value fields not present"
        assert len(delete1) != 0, "Delete fields not present"
        self.wait_for_element(self.add_property)
        self.wait_to_click(self.add_property)
        
        assert len(props1)+1 == len(self.find_elements(self.properties_input)), "Property fields not added"
        assert len(value1)+1 == len(self.find_elements(self.value_input)), "Value fields not added"
        assert len(delete1)+1 == len(self.find_elements(self.delete_property)), "Delete fields not added"
        self.send_keys(self.last_properties_input, property)
        ActionChains(self.driver).send_keys(Keys.TAB).perform()
        time.sleep(2)
        if value!=None:
            self.clear(self.last_value_input)
            self.send_keys(self.last_value_input, value)
            ActionChains(self.driver).send_keys(Keys.TAB).perform()
        return len(props1)

    def delete_last_added_property(self, length):
        self.scroll_to_element(self.column_editor)
        self.wait_to_click(self.column_editor)
        print(length)
        self.wait_to_click(self.last_delete_property)
        time.sleep(3)
        props1 = self.find_elements(self.properties_input)
        value1 = self.find_elements(self.value_input)
        delete1 = self.find_elements(self.delete_property)
        time.sleep(3)
        assert len(props1) == length, "Property fields not deleted"
        assert len(value1) == length, "Value fields not deleted"
        assert len(delete1) == length, "Delete fields not deleted"
        print("Last added property is deleted")

    def case_list_explorer_get_case_data(self):
        self.wait_to_click(self.case_list_explorer_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.case_list_explorer_TITLE in self.driver.title, "This is not the Case List Explorer page."
        self.verify_user_lookup_table()
        self.remove_default_users()
        self.send_keys(self.users_field, UserData.web_user_email)
        self.wait_to_click((By.XPATH, self.users_list_item.format(UserData.web_user_email)))
        
        self.select_by_text(self.case_type_dropdown, UserData.case_case)
        self.select_by_text(self.open_close_dropdown, UserData.open_close_options[1])
        # self.wait_to_clear_and_send_keys(self.search_input, "name*")
        self.wait_to_click(self.apply_id)
        time.sleep(2)
        self.wait_for_element(self.result_table, 300)
        self.wait_for_element(self.report_content_id, 120)
        print("Report loaded successfully!")
        self.verify_users_used_in_the_group([UserData.web_user_email])
        time.sleep(2)
        url1 = self.get_attribute(self.name_form_column_first, "href")
        self.wait_to_click(self.name_form_column_first)
        time.sleep(2)
        self.switch_to_next_tab()
        assert self.CASE_DATA_TITLE in self.driver.title, "This is not the Case Data page."
        self.wait_for_element(self.case_property_tab)
        self.wait_for_element(self.case_history_tab)
        self.wait_for_element(self.download_case_history)
        self.wait_for_element(self.close_case)
        data_dict = dict()
        for items in UserData.case_data_property:
            data_dict[items] = self.get_text((By.XPATH, self.case_data_property_values.format(items)))
        print(data_dict)
        self.wait_to_click(self.case_history_tab)
        self.wait_for_element((By.XPATH, self.case_data_history_values.format(UserData.case_data_history[-1])))
        for items in UserData.case_data_history:
            data_dict[items] = self.get_text((By.XPATH, self.case_data_history_values.format(items)))
        data_dict['owner_id'] = UserData.web_user_id_staging
        data_dict['url'] = url1
        print("Final dictionary", data_dict)
        self.wait_to_click(self.download_case_history)
        time.sleep(2)
        self.wait_to_click(self.close_case)
        self.wait_for_element((By.XPATH, self.close_success_msg.format(data_dict['Name'])), 100)
        self.driver.close()
        self.switch_back_to_prev_tab()
        return data_dict

    def compare_case_date_with_download(self, data_dict):
        newest_file = latest_download_file(".csv")
        path = os.path.join(PathSettings.DOWNLOAD_PATH, newest_file)
        print(path)
        df = pd.read_csv(path, index_col=None, names=['col1','col2'])
        res = dict(zip(list(df['col1']), list(df['col2'])))
        print("Downloaded Data: ", res)
        for item in UserData.case_data_vs_dictionary:
            assert res[item] in data_dict[UserData.case_data_vs_dictionary[item]],"Not Matching " + res[item] +" and " + data_dict[UserData.case_data_vs_dictionary[item]]
            print("Matching", res[item], data_dict[UserData.case_data_vs_dictionary[item]])

    def verify_case_close(self, data_dict):
        print("Sleeping some tine for the case to close")
        time.sleep(50)
        self.wait_to_click(self.case_list_explorer_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.case_list_explorer_TITLE in self.driver.title, "This is not the Case List Explorer page."
        self.verify_user_lookup_table()
        self.remove_default_users()
        self.send_keys(self.users_field, UserData.web_user_email)
        self.wait_to_click((By.XPATH, self.users_list_item.format(UserData.web_user_email)))
        
        self.wait_to_clear_and_send_keys(self.search_input, data_dict['Case ID'])
        # check in Closed Case List Explorer
        self.select_by_text(self.open_close_dropdown, UserData.open_close_options[2])
        self.wait_to_click(self.apply_id)
        time.sleep(2)
        self.wait_for_element(self.result_table, 300)
        self.wait_for_element(self.report_content_id, 120)
        print("Report loaded successfully!")
        self.verify_users_used_in_the_group([UserData.web_user_email])
        time.sleep(2)
        assert "closed" in self.get_text(self.status_column_first)
        assert data_dict['url'] == self.get_attribute(self.name_form_column_first, "href")
        print("Case closed successfully")
        # check in Open Case List Explorer
        self.select_by_text(self.open_close_dropdown, UserData.open_close_options[1])
        self.wait_to_click(self.apply_id)
        time.sleep(2)
        self.wait_for_element(self.result_table, 300)
        self.wait_for_element(self.report_content_id, 120)
        print("Report loaded successfully!")
        self.wait_for_element(self.empty_table)
        print("Case not present in Open Case List Explorer")

    def export_application_status_to_excel(self):
        self.wait_to_click(self.application_status_rep)
        self.wait_for_element(self.apply_id, 100)
        assert self.APPLICATION_STATUS_TITLE in self.driver.title, "This is not the Application Status page."
        self.verify_user_lookup_table()
        self.remove_default_users()
        self.send_keys(self.users_field, UserData.user_group)
        self.wait_to_click((By.XPATH, self.users_list_item.format(UserData.user_group)))
        
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

    def compare_status_with_email(self, link, web_data):
        print(link)
        print(web_data)
        self.driver.get(link)
        time.sleep(2)
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
            if i == 1 or i == 2:
                print("Not comparing", html.unescape(str(list[i])), " with ", str(web_data[i]))
            elif "View" in str(web_data[i]):
                print("Not comparing", html.unescape(str(list[i])), " with ", str(web_data[i]))
            else:
                print("Comparing ", html.unescape(str(list[i])), " with ", str(web_data[i]))
                assert html.unescape(str(list[i])) == str(web_data[i]), "Cpmparision failed for " + list[i] + " and " + web_data[i]


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

    def compare_status_with_html_table(self, table_data, web_data):
        list = table_data
        list = [el.replace(u'\xa0', ' ') for el in list]
        print("Old data rows: ", len(web_data), "New data rows: ", len(list))
        print("Old List: ", web_data)
        print("New list: ", list)
        assert len(web_data) == len(list), "Data in Both Email Body and Searched results do not match"
        print("Both Email Body and Searched results have same amount of data")
        for i in range(len(list)):
            print("Comparing ", str(list[i]), " with ", str(web_data[i]))
            assert str(list[i]) == str(web_data[i]), "Comparison failed for " + list[i] + " and " + \
                                                                    web_data[i]

    def verify_query_2_case_data(self):
        self.wait_to_click(self.case_list_explorer_rep)
        time.sleep(2)
        self.wait_for_element(self.apply_id, 100)
        assert self.case_list_explorer_TITLE in self.driver.title, "This is not the Case List Explorer page."
        self.wait_to_click(self.search_textarea_div)
        self.send_keys(self.search_input, self.query2)
        
        self.wait_to_click(self.apply_id)
        assert self.is_present(self.report_loading), "Loading Report block is not present"
        time.sleep(2)
        self.wait_for_element(self.result_table, 300)
        self.wait_for_element(self.report_content_id, 120)
        print("Report loaded successfully!")
        self.scroll_to_bottom()
        case_name = self.find_elements(self.case_name_column_list)
        case_type = self.find_elements(self.case_type_column_list)
        for items in case_name:
            text = items.text
            assert text.startswith('text'), "Case Name is not matching the query"
        for items in case_type:
            assert UserData.case_reassign_change == items.text, "Case type is not matching the query"

    def verify_query_1_case_data(self):
        self.wait_to_click(self.case_list_explorer_rep)
        time.sleep(2)
        self.wait_for_element(self.apply_id, 100)
        assert self.case_list_explorer_TITLE in self.driver.title, "This is not the Case List Explorer page."
        self.wait_to_click(self.search_textarea_div)
        self.send_keys(self.search_input, self.query1)
        date_string, start_date, end_date = self.get_custom_dates_past(0, 0, 0)
        
        self.verify_user_lookup_table()
        self.remove_default_users()
        self.send_keys(self.users_field, UserData.app_login)
        self.wait_to_click((By.XPATH, self.users_list_item.format(UserData.app_login)))
        
        self.select_by_text(self.case_type_dropdown, UserData.case_reassign)
        
        self.wait_to_click(self.apply_id)
        assert self.is_present(self.report_loading), "Loading Report block is not present"
        time.sleep(2)
        self.wait_for_element(self.result_table, 300)
        self.wait_for_element(self.report_content_id, 120)
        print("Report loaded successfully!")
        self.scroll_to_bottom()
        last_modified = self.find_elements(self.last_modified_list)
        date_list = []
        for items in last_modified:
            text = items.text
            text = text.replace("IST",'')
            print(text)
            date_list.append(text)
        print("Date List: ", date_list)
        for item in date_list:
            self.date_validator(item, start_date, end_date)

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
    def verify_timezone_change(self):
        self.wait_to_click(self.case_list_explorer_rep)
        time.sleep(2)
        self.wait_for_element(self.apply_id, 100)
        assert self.case_list_explorer_TITLE in self.driver.title, "This is not the Case List Explorer page."
        
        self.wait_to_click(self.apply_id)
        assert self.is_present(self.report_loading), "Loading Report block is not present"
        time.sleep(2)
        self.wait_for_element(self.result_table, 300)
        self.wait_for_element(self.report_content_id, 120)
        print("Report loaded successfully!")
        self.scroll_to_bottom()
        last_modified = self.find_elements(self.last_modified_list)
        for items in last_modified:
            assert "IST" in items.text, "Timezone is " + UserData.proj_settings_timezones[1]
        self.project_setting_update_timezone(UserData.proj_settings_timezones[0])
        self.wait_to_click(self.case_list_explorer_rep)
        time.sleep(2)
        self.wait_for_element(self.apply_id, 100)
        assert self.case_list_explorer_TITLE in self.driver.title, "This is not the Case List Explorer page."
        
        self.wait_to_click(self.apply_id)
        time.sleep(15)
        self.wait_for_element(self.report_content_id, 120)
        print("Report loaded successfully!")
        self.scroll_to_element(self.report_content_id)
        last_modified = self.find_elements(self.last_modified_list)
        for items in last_modified:
            assert "EDT" in items.text, "Timezone is " + UserData.proj_settings_timezones[0]
        time.sleep(2)
        self.project_setting_update_timezone(UserData.proj_settings_timezones[1])
        self.wait_to_click(self.case_list_explorer_rep)
        time.sleep(2)
        self.wait_for_element(self.apply_id, 100)
        assert self.case_list_explorer_TITLE in self.driver.title, "This is not the Case List Explorer page."
        
        self.wait_to_click(self.apply_id)
        time.sleep(15)
        self.wait_for_element(self.report_content_id, 120)
        print("Report loaded successfully!")
        self.scroll_to_element(self.report_content_id)
        last_modified = self.find_elements(self.last_modified_list)
        for items in last_modified:
            assert "IST" in items.text, "Timezone is " + UserData.proj_settings_timezones[1]

    def project_setting_update_timezone(self, value):
        self.driver.execute_script("window.open('');")
        self.switch_to_next_tab()
        self.driver.get(self.proj_setting)
        self.wait_for_element(self.update_basic_info)
        self.scroll_to_element(self.default_timezone)
        self.select_by_value(self.default_timezone, value)
        print("Default timezone changed to : ", value)
        self.scroll_to_element(self.update_basic_info)
        self.click(self.update_basic_info)
        self.wait_for_element(self.proj_setting_saved)
        print("Project Settings Saved!")
        self.driver.close()
        
        self.switch_back_to_prev_tab()
        time.sleep(10)
        print("sleeping for some time....")


