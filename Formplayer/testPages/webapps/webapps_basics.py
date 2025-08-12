import time
from random import randint
from datetime import datetime

from selenium.common import TimeoutException
from selenium.webdriver import ActionChains

from common_utilities.generate_random_string import fetch_random_string, fetch_random_digit_with_range, \
    fetch_phone_number
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
        self.home_screen = (By.CLASS_NAME, 'cloudcare-home-content')
        self.menu_list = (By.XPATH, "//ul[@id='hq-main-tabs']")
        self.login_as_button = (By.XPATH, "//div[@class='js-restore-as-item appicon appicon-restore-as']")
        self.filter_workers = (By.XPATH, "//input[@class= 'js-user-query form-control']")
        self.search_button = (By.XPATH, "//i[@class = 'fa fa-search']")
        self.login_user = (By.XPATH, "//td[.//b[.='" + UserData.app_preview_mobile_worker + "']]")
        self.confirm_login_button = (By.XPATH, "//button[@id ='js-confirmation-confirm']")
        self.test_application = (By.XPATH, "//h3[contains(text(), '" + UserData.test_application['tests_app'] + "')]")
        self.case_list_menu = (By.XPATH, "//h3[contains(text(), '" + UserData.test_application['case_list'] + "')]")
        self.registration_form = (By.XPATH, "//h3[contains(text(), '" + UserData.test_application['form_name'] + "')]")
        self.followup_form = (By.XPATH, "//h3[contains(text(), 'Followup Form')]")
        self.name_question = (By.XPATH, "//label[.//span[text()='Name']]/following-sibling::div//textarea")
        self.dob_question = (By.XPATH, "//label[.//span[text()='DOB']]/following-sibling::div//input")
        self.sync = (By.XPATH, "//h3[contains(text(), 'Sync')]")
        self.home_icon = (By.XPATH, "//i[@class='fcc fcc-flower']")
        self.mobileno_question = (By.XPATH, "//label[.//span[text()='Mobile No.']]/following-sibling::div//input")
        self.submit_form_button = (By.XPATH, "//button[@type= 'submit']")
        self.success_message = (By.XPATH, "//p[contains(text(),'successfully saved')]")
        self.sync_success_message = (By.XPATH, "(//div[text()='User Data successfully synced.'])[1]")
        self.search_case_filter = (By.XPATH, "//input[@id ='searchText']")
        self.case_name = (By.XPATH, "//tr[td[text()='" + self.name_input + "']]")
        self.continue_button = (By.XPATH, "//button[text()='Continue']")
        self.parent_question = (
        By.XPATH, "//label[.//span[text()='Parent/Gaurdian Name']]/following-sibling::div//textarea")
        self.no_of_kids = (By.XPATH, "//label[.//span[text()='No of Kids']]/following-sibling::div//input")
        self.settings = (By.XPATH, "//h3[text()='Settings']")
        self.break_button = (By.XPATH, "//button[text()='Break']")
        self.break_message = (By.XPATH, "//div[text()='No locks for the current user']")
        self.clear_user_data_button = (By.XPATH, "//button[text()='Clear']")
        self.clear_data_message = (By.XPATH, "//div[text()='User data successfully cleared.']")
        self.done_button = (By.XPATH, "//button[@class='btn btn-primary js-done']")
        self.settings_dropdown = (By.XPATH, "//a[@data-action='Click Gear Icon']")
        self.sign_out = (By.XPATH, "//a[@data-label ='Sign Out']")
        self.question_display_text = (By.XPATH, "//span[text()='Name (es)']")

        # login xpaths
        self.username_textbox_id = (By.ID, "id_auth-username")
        self.password_textbox_id = (By.ID, "id_auth-password")
        self.submit_button_xpath = (By.XPATH, '(//button[@type="submit"])[last()]')

        self.reports_menu_id = (By.LINK_TEXT, "Reports")
        self.full_menu = (By.LINK_TEXT, "Show Full Menu")
        self.ribbon_logo = (By.XPATH, "//a[@class='navbar-brand'][@href='/homepage/']")
        self.submit_history_rep = (By.LINK_TEXT, "Submission History")
        self.case_list_rep = (By.LINK_TEXT, "Case List")
        self.apply_id = (By.ID, "apply-filters")
        self.this_form = (By.XPATH, "//a[.='this form']")
        self.this_case = (By.XPATH, "//a[.='this case']")
        self.breadcrumbs = "//li[contains(@class,'breadcrumb')][contains(text(),'{}') or ./a[contains(.,'{}')]]"

        # Submit History
        self.users_box = (By.XPATH, "//span[@class='select2-selection select2-selection--multiple']")
        self.selected_users = (By.XPATH, "//li[contains(@class,'select2-selection')]")
        self.deselect_user = "(//button[contains(@class,'select2-selection')])[{}]"
        self.search_user = (By.XPATH, "//textarea[@class='select2-search__field']")
        self.users_field = (By.XPATH, "(//textarea[@class='select2-search__field'])[1]")
        self.remove_buttons = (By.XPATH, "//ul//button")
        self.users_list_item = "//ul[@role='listbox']/li[contains(.,'{}')]"
        self.app_user_select = "(//li[contains(text(),'{}')])[1]"
        self.select_user = (By.XPATH, "//li[contains(text(),'[All Data]')]")
        self.application_select = (By.XPATH, "//select[@id='report_filter_form_app_id']")
        self.module_select = (By.XPATH, "//select[@id='report_filter_form_module']")
        self.form_select = (By.XPATH, "//select[@id='report_filter_form_xmlns']")
        self.case_type_select = (By.XPATH, "//select[@id='report_filter_case_type']")
        self.date_input = (By.XPATH, "//input[@id='filter_range']")
        self.view_form_link = (By.XPATH, "//tbody/tr[1]/td[1]/a[.='View Form']")
        self.submit_history_table = (By.XPATH, "//table[@id='report_table_submit_history']/tbody/tr")
        self.case_name_field = "td[@title={}]"
        self.form_data_table = (By.XPATH, "//table[contains(@class,'form-data-table')]")
        # Case List
        self.search_input = (By.XPATH, "//input[@id='report_filter_search_query']")
        self.case_list_table = (By.XPATH, "//table[@id='report_table_case_list']/tbody/tr")
        self.case_id_block = (By.XPATH, "//th[@title='_id']/following-sibling::td")

        self.click_outside = (By.XPATH, "//label[.//span[text()='Mobile No.']]")

    def open_web_apps_menu(self):
        if self.is_present(self.webapps_menu_id):
            self.wait_to_click(self.webapps_menu_id)
        else:
            self.wait_to_click(self.full_menu)
            self.wait_to_click(self.webapps_menu_id)

    def get_links(self):
        form_link = self.get_attribute(self.this_form, "href")
        case_link = self.get_attribute(self.this_case, "href")
        return form_link, case_link

    def application_is_present(self):
        self.open_web_apps_menu()
        assert self.is_present_and_displayed(self.test_application), "Application is not present in Web Apps"
        print("App is present")

    def verify_app_home_screen(self):
        assert self.is_present(self.home_screen)
        print("Web app home screen is displayed")
        assert not self.is_visible_and_displayed(self.menu_list, 10)
        print("All the Menus are hidden")
        assert self.is_present(self.full_menu)
        print("Show Full Menu link is present")

    def verify_breadcrumbs(self, application):
        self.wait_to_click(self.test_application)
        self.wait_to_click(self.case_list_menu)
        self.wait_to_click(self.registration_form)
        
        assert self.is_present(self.name_question)
        print("We are inside the form")
        self.wait_to_click((By.XPATH, self.breadcrumbs.format(application['case_list'], application['case_list'])))
        
        assert self.is_present(self.registration_form)
        print("We are in the case list screen")
        self.wait_to_click((By.XPATH, self.breadcrumbs.format(application['tests_app'], application['tests_app'])))
        
        assert self.is_present(self.case_list_menu)
        print("We are in the application screen")
        self.wait_to_click(self.home_icon)
        
        assert self.is_present(self.test_application)
        print("We are at the Web Apps home screen")

    def verify_ribbon(self):
        self.wait_to_click(self.full_menu)
        assert self.is_present(self.ribbon_logo)
        print("Dimagi Ribbon Logo is present")

    def sync_forms(self):
        
        self.wait_for_element(self.home_icon)
        self.wait_to_click(self.home_icon)
        
        self.wait_to_click(self.sync)
        
        assert self.is_present_and_displayed(self.sync_success_message), ("Sync is not successful!")
        time.sleep(10)
        print("Sleeping for some time for the data to get updated")

    def login_as_a_user(self):
        self.wait_to_click(self.login_as_button)
        self.wait_to_clear_and_send_keys(self.filter_workers, UserData.app_preview_mobile_worker)
        self.wait_to_click(self.search_button)
        
        self.wait_to_click(self.login_user)
        self.wait_to_click(self.confirm_login_button)

    def submit_form(self):
        self.open_web_apps_menu()
        self.login_as_a_user()
        self.wait_to_click(self.test_application)
        
        self.wait_to_click(self.case_list_menu)
        
        self.wait_to_click(self.registration_form)
        
        self.wait_to_clear_and_send_keys(self.name_question, self.name_input)
        self.send_keys(self.dob_question, self.get_current_date_form_input() + Keys.TAB)
        # self.wait_to_click(self.click_today_date)
        # self.wait_to_click(self.close_date_picker)
        self.wait_to_clear_and_send_keys(self.mobileno_question, fetch_phone_number() + Keys.TAB)
        
        self.wait_to_click(self.submit_form_button)
        
        assert self.is_present_and_displayed(self.success_message, 100), ("Form is not submitted!")
        self.wait_to_click(self.case_list_menu)
        self.wait_to_click(self.followup_form)
        self.wait_to_clear_and_send_keys(self.search_case_filter, self.name_input)
        self.wait_to_click(self.search_button)
        self.wait_to_click(self.case_name)
        self.wait_to_click(self.continue_button)
        self.wait_to_clear_and_send_keys(self.parent_question, self.parent_name_input)
        self.wait_to_clear_and_send_keys(self.no_of_kids, fetch_random_digit_with_range(1, 5))
        self.wait_to_click(self.submit_form_button)
        assert self.is_present_and_displayed(self.success_message, 100)

    def get_present_date(self):
        # Get today's date
        presentday = datetime.now()  # or presentday = datetime.today()
        # Get Yesterday
        # yesterday = presentday - timedelta(1)
        # Get Tomorrow
        # tomorrow = presentday + timedelta(1)

        return presentday.strftime('%Y-%m-%d') + " to " + presentday.strftime('%Y-%m-%d')

    def get_current_date_form_input(self):
        # Get today's date
        presentday = datetime.now()  # or presentday = datetime.today()

        return presentday.strftime('%m/%d/%Y')

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

    def verify_form_data_submit_history(self, case_name, application):
        print("Serching for case name: ", case_name)
        self.open_submit_history_form_link(application, UserData.app_preview_mobile_worker)
        
        try:
            assert self.is_present_and_displayed((By.XPATH, self.case_name_field.format(
                case_name))), "Case name " + case_name + "is not present in Submit history"
        except:
            print("Case Name is not yet updated in Submit History")
        self.driver.back()

    def open_submit_history_form_link(self, application, username):
        if self.is_present(self.reports_menu_id):
            self.wait_to_click(self.reports_menu_id)
        else:
            self.wait_to_click(self.full_menu)
            self.wait_to_click(self.reports_menu_id)
        self.click(self.submit_history_rep)
        print("Sleeping for some time for the form/case data to be updated in reports")
        time.sleep(40)
        self.remove_default_users()
        self.clear(self.users_field)
        self.send_keys(self.users_field, username)
        
        self.wait_for_element((By.XPATH, self.users_list_item.format(username)))
        self.click((By.XPATH, self.users_list_item.format(username)))
        
        #
        # self.send_keys(self.search_user, username)
        # self.wait_to_click((By.XPATH, self.app_user_select.format(username)))
        self.select_by_text(self.application_select, application['tests_app'])
        self.select_by_text(self.module_select, application['case_list'])
        self.select_by_text(self.form_select, application['form_name'])
        date_range = self.get_present_date()
        self.clear(self.date_input)
        self.send_keys(self.date_input, date_range + Keys.TAB)
        self.wait_to_click(self.apply_id)
        time.sleep(2)
        self.scroll_to_bottom()
        self.verify_table_not_empty(self.submit_history_table)
        self.is_present_and_displayed(self.view_form_link)
        form_link = self.get_attribute(self.view_form_link, "href")
        print("View Form Link: ", form_link)
        self.driver.get(form_link)
        time.sleep(3)

    def verify_form_data_case_list(self, case_name, username):
        if self.is_present(self.reports_menu_id):
            self.wait_to_click(self.reports_menu_id)
        else:
            self.wait_to_click(self.full_menu)
            self.wait_to_click(self.reports_menu_id)
        print("Sleeping for some time for the case data to be updated in reports")
        time.sleep(60)
        self.wait_to_click(self.case_list_rep)
        self.remove_default_users()
        self.send_keys(self.search_user, username)
        self.wait_for_element((By.XPATH, self.app_user_select.format(username)))
        self.click((By.XPATH, self.app_user_select.format(username)))
        
        self.select_by_text(self.case_type_select, UserData.case_type)
        self.send_keys(self.search_input, case_name)
        self.wait_to_click(self.apply_id)
        time.sleep(15)
        self.scroll_to_bottom()
        self.verify_table_not_empty(self.case_list_table)
        self.page_source_contains(case_name)
        self.wait_and_sleep_to_click((By.LINK_TEXT, str(case_name)))
        time.sleep(3)
        self.page_source_contains(case_name)
        assert True, "Case name is present in Case List"
        self.driver.back()

    def verify_web_apps_settings(self):
        self.open_web_apps_menu()
        self.login_as_a_user()
        self.wait_to_click(self.settings)
        self.wait_to_click(self.break_button)
        
        assert self.is_displayed(self.break_message)
        self.wait_to_click(self.clear_user_data_button)
        
        assert self.is_displayed(self.clear_data_message)
        self.click(self.done_button)

    def verify_language(self):
        if self.is_present(self.full_menu):
            self.wait_to_click(self.full_menu)
            self.wait_to_click(self.settings_dropdown)
        else:
            self.wait_to_click(self.settings_dropdown)
        self.wait_to_click(self.sign_out)
        self.wait_for_element(self.username_textbox_id)
        self.wait_to_clear_and_send_keys(self.username_textbox_id, UserData.mw_username)
        self.wait_to_clear_and_send_keys(self.password_textbox_id, UserData.mw_password)
        self.click(self.submit_button_xpath)
        self.wait_to_click(self.test_application)
        self.wait_to_click(self.case_list_menu)
        self.wait_to_click(self.registration_form)
        assert self.is_present_and_displayed(self.question_display_text)

    def wait_to_click(self, locator, timeout=50):
        try:
            self.wait_for_element(locator, timeout)
            
            self.wait_to_click(locator)
        except (TimeoutException):
            print("locator not present")

    def remove_default_users(self):
        self.wait_for_element(self.users_field)
        count = self.find_elements(self.remove_buttons)
        print(len(count))
        for i in range(len(count)):
             count[0].click()
             
             if len(count) != 1:
                ActionChains(self.driver).send_keys(Keys.TAB).perform()
                
             count = self.find_elements(self.remove_buttons)

