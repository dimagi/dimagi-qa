import time
from random import randint
from datetime import datetime

from Formplayer.userInputs.generate_random_string import fetch_random_string, fetch_random_digit
from common_utilities.selenium.base_page import BasePage
from Formplayer.userInputs.user_inputs import UserData

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

""""Contains test page elements and functions related to the WebApps Access/Basics of Commcare"""


class WebAppsBasics(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

        self.name_input = "name" + fetch_random_string()
        self.parent_name_input = "parent" + fetch_random_string()

        self.webapps_menu_id = (By.LINK_TEXT, "Web Apps")
        self.login_as_button = (By.XPATH, "//div[@class='js-restore-as-item appicon appicon-restore-as']")
        self.filter_workers = (By.XPATH, "//input[@class= 'js-user-query form-control']")
        self.search_button = (By.XPATH, "//i[@class = 'fa fa-search']")
        self.login_user = (By.XPATH, "//td[@class = 'module-column module-column-name'][1]")
        self.confirm_login_button = (By.XPATH, "//button[@id ='js-confirmation-confirm']")
        self.test_application = (By.XPATH, "//h3[contains(text(), '"+UserData.basic_tests_app+"')]")
        self.case_list_menu = (By.XPATH, "//h3[contains(text(), 'Case List')]")
        self.registration_form = (By.XPATH, "//h3[contains(text(), 'Registration Form')]")
        self.followup_form = (By.XPATH, "//h3[contains(text(), 'Followup Form')]")
        self.name_question = (By.XPATH, "//textarea[@class ='textfield form-control']")
        self.dob_question = (By.XPATH, '''//input[@data-bind = "attr: { id: entryId, 'aria-required': $parent.required() ? 'true' : 'false' }"]''')
        self.click_today_date = (By.XPATH, "//a[@data-action='today']")
        self.close_date_picker = (By.XPATH, "//a[@data-action='close']")
        self.mobileno_question = (By.XPATH, "//label[.//span[text()='Mobile No.']]/following-sibling::div//input")
        self.submit_form_button = (By.XPATH, "//button[@type= 'submit']")
        self.success_message = (By.XPATH, "//p[text()='Form successfully saved!']")
        self.search_case_filter = (By.XPATH, "//input[@id ='searchText']")
        self.case_name = (By.XPATH, "//tr[td[text()='" + self.name_input +"']]")
        self.continue_button = (By.XPATH, "//button[text()='Continue']")
        self.parent_question = (By.XPATH, "//label[.//span[text()='Parent/Gaurdian Name']]/following-sibling::div//textarea")
        self.no_of_kids = (By.XPATH, "//label[.//span[text()='No of Kids']]/following-sibling::div//input")
        self.settings = (By.XPATH, "//h3[text()='Settings']")
        self.break_button = (By.XPATH, "//button[text()='Break']")
        self.break_message = (By.XPATH, "//div[text()='No locks for the current user']")
        self.clear_user_data_button = (By.XPATH, "//button[text()='Clear']")
        self.clear_data_message = (By.XPATH, "//div[text()='User data successfully cleared.']")
        self.done_button = (By.XPATH, "//button[text()='Done']")
        self.settings_dropdown = (By.XPATH, "//a[@class ='dropdown-toggle dropdown-toggle-with-icon track-usage-link']")
        self.sign_out = (By.XPATH, "//a[@data-label ='Sign Out']")
        self.question_display_text = (By.XPATH, "//span[text()='Name (es)']")

        #login xpaths
        self.username_textbox_id = (By.ID, "id_auth-username")
        self.password_textbox_id = (By.ID, "id_auth-password")
        self.submit_button_xpath = (By.XPATH, '(//button[@type="submit"])[last()]')

        self.reports_menu_id = (By.LINK_TEXT, "Reports")
        self.submit_history_rep = (By.LINK_TEXT, "Submit History")
        self.case_list_rep = (By.LINK_TEXT, "Case List")
        self.apply_id = (By.ID, "apply-filters")

        # Submit History
        self.users_box = (By.XPATH, "//span[@class='select2-selection select2-selection--multiple']")
        self.select_user = (By.XPATH, "//li[contains(text(),'[All Data]')]")
        self.application_select = (By.XPATH, "//select[@id='report_filter_form_app_id']")
        self.module_select = (By.XPATH, "//select[@id='report_filter_form_module']")
        self.form_select = (By.XPATH, "//select[@id='report_filter_form_xmlns']")
        self.case_type_select = (By.XPATH, "//select[@id='report_filter_case_type']")
        self.date_input = (By.XPATH, "//input[@id='filter_range']")
        self.view_form_link = (By.XPATH, "//tbody/tr[1]/td[1]/a[.='View Form']")
        self.submit_history_table = (By.XPATH, "//table[@id='report_table_submit_history']/tbody/tr")

        # Case List
        self.search_input = (By.XPATH, "//input[@id='report_filter_search_query']")
        self.case_list_table = (By.XPATH, "//table[@id='report_table_case_list']/tbody/tr")
        self.case_id_block = (By.XPATH, "//th[@title='_id']/following-sibling::td")

        self.click_outside = (By.XPATH, "//label[.//span[text()='Mobile No.']]")

    def application_is_present(self):
        self.wait_to_click(self.webapps_menu_id)
        assert self.is_present_and_displayed(self.test_application), "Application is not present in Web Apps"
        print("App is present")

    def login_as_a_user(self):
        self.wait_to_click(self.login_as_button)
        self.wait_to_clear_and_send_keys(self.filter_workers, UserData.app_preview_mobile_worker)
        self.wait_to_click(self.search_button)
        self.wait_to_click(self.login_user)
        self.wait_to_click(self.confirm_login_button)

    def submit_form(self):
        self.wait_to_click(self.webapps_menu_id)
        self.login_as_a_user()
        self.wait_to_click(self.test_application)
        self.wait_to_click(self.case_list_menu)
        self.wait_to_click(self.registration_form)
        self.wait_to_clear_and_send_keys(self.name_question, self.name_input)
        self.wait_to_click(self.dob_question)
        self.wait_to_click(self.click_today_date)
        self.wait_to_click(self.close_date_picker)
        self.wait_to_clear_and_send_keys(self.mobileno_question, UserData.mobile_number + Keys.TAB)
        self.js_click(self.submit_form_button)
        assert self.is_present_and_displayed(self.success_message), ("Form is not submitted!")
        self.wait_to_click(self.case_list_menu)
        self.wait_to_click(self.followup_form)
        self.wait_to_clear_and_send_keys(self.search_case_filter, self.name_input)
        self.wait_to_click(self.search_button)
        self.js_click(self.case_name)
        self.wait_to_click(self.continue_button)
        self.wait_to_clear_and_send_keys(self.parent_question, self.parent_name_input)
        self.wait_to_clear_and_send_keys(self.no_of_kids, fetch_random_digit(1,5))
        self.wait_to_click(self.submit_form_button)
        assert self.is_present_and_displayed(self.success_message)

    def get_yesterday_tomorrow_dates(self):
        # Get today's date
        presentday = datetime.now()  # or presentday = datetime.today()
        return presentday.strftime('%Y-%m-%d')+" to "+presentday.strftime('%Y-%m-%d')

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

    def verify_form_data_submit_history(self):
        self.driver.find_element_by_link_text("Show Full Menu").click()
        self.wait_to_click(self.reports_menu_id)
        self.wait_to_click(self.submit_history_rep)
        self.select_by_text(self.application_select, UserData.test_application)
        self.select_by_text(self.module_select, UserData.case_list_name)
        self.select_by_text(self.form_select, UserData.form_name)
        date_range = self.get_current_date()
        self.clear(self.date_input)
        self.send_keys(self.date_input, date_range+Keys.TAB)
        self.wait_to_click(self.apply_id)
        time.sleep(10)
        self.scroll_to_bottom()
        self.verify_table_not_empty(self.submit_history_table)
        self.is_present_and_displayed(self.view_form_link)
        form_link = self.get_attribute(self.view_form_link, "href")
        print("View Form Link: ", form_link)
        self.driver.get(form_link)
        time.sleep(3)
        self.page_source_contains(self.name_input)
        assert True, "Case name is present in Submit history"
        self.driver.back()

    def verify_form_data_case_list(self, case_name):
        self.wait_to_click(self.reports_menu_id)
        self.wait_to_click(self.case_list_rep)
        self.wait_to_click(self.users_box)
        self.wait_to_click(self.select_user)
        self.send_keys(self.search_input, self.name_input)
        self.wait_to_click(self.apply_id)
        time.sleep(15)
        self.scroll_to_bottom()
        self.verify_table_not_empty(self.case_list_table)
        case_search = self.name_input
        self.page_source_contains(case_search)
        self.wait_and_sleep_to_click((By.LINK_TEXT, str(case_search)))
        time.sleep(3)
        self.page_source_contains(case_search)
        assert True, "Case name is present in Case List"
        self.driver.back()

    def verify_web_apps_settings(self):
        self.wait_to_click(self.webapps_menu_id)
        self.login_as_a_user()
        self.wait_to_click(self.settings)
        self.wait_to_click(self.break_button)
        assert self.is_present_and_displayed(self.break_message)
        self.wait_to_click(self.clear_user_data_button)
        assert self.is_present_and_displayed(self.clear_data_message)
        self.wait_to_click(self.done_button)

    def verify_language(self):
        self.wait_to_click(self.settings_dropdown)
        self.wait_to_click(self.sign_out)
        self.wait_to_clear_and_send_keys(self.username_textbox_id, UserData.mw_username)
        self.wait_to_clear_and_send_keys(self.password_textbox_id, UserData.mw_password)
        self.click(self.submit_button_xpath)
        self.wait_to_click(self.test_application)
        self.wait_to_click(self.case_list_menu)
        self.wait_to_click(self.registration_form)
        assert self.is_present_and_displayed(self.question_display_text)



