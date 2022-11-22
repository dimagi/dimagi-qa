from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from common_utilities.selenium.base_page import BasePage

""""Contains common  page elements and functions related to webapps actions"""


class WebApps(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

        self.app_name_format = "//*[contains(@aria-label,'{}')]/div"
        self.app_header_format = "//h1[contains(text(),'{}')]"
        self.menu_name_format = "//*[contains(@aria-label,'{}')]"
        self.menu_name_header_format = "//*[contains(text(),'{}')]"
        self.form_name_format = "//tr[contains(@aria-label,'{}')]"
        self.case_name_format = "//tr[.//td[contains(text(),'{}')]]"
        self.app_breadcrumb_format = "//li[contains(text(), '{}')]"

        self.form_submit = (By.XPATH, "//button[@class='submit btn btn-primary']")
        self.form_submission_successful = (By.XPATH, "//p[contains(text(), 'Form successfully saved')]")
        self.search_all_cases_button = (By.XPATH, "//*[contains(text(),'Search All')]//parent::div[@class='case-list-action-button btn-group formplayer-request']")
        self.search_again_button = (By.XPATH, "//*[contains(text(),'Search Again')]//parent::div[@class='case-list-action-button btn-group formplayer-request']")
        self.clear_case_search_page = (By.XPATH, "//button[@id='query-clear-button']")
        self.submit_on_case_search_page = (By.XPATH, "//button[@type='submit' and @id='query-submit-button']")
        self.case_list = (By.XPATH, "//table[@class='table module-table module-table-case-list']")
        self.omni_search_input = (By.ID, "searchText")
        self.omni_search_button = (By.ID, "case-list-search-button")
        self.continue_button = (By.ID, "select-case")

        self.webapps_home = (By.XPATH, "//i[@class='fcc fcc-flower']")
        self.webapp_login = (By.XPATH, "(//div[@class='js-restore-as-item appicon appicon-restore-as'])")
        self.search_user_webapps = (By.XPATH, "//input[@placeholder='Filter workers']")
        self.search_button_webapps = (By.XPATH, "//div[@class='input-group-btn']")
        self.login_as_username = "//h3/b[.='{}']"
        self.webapp_login_confirmation = (By.ID, 'js-confirmation-confirm')
        self.webapp_working_as = (By.XPATH, "//div[@class='restore-as-banner module-banner']/b")
        self.form_names = (By.XPATH, "//h3[text()]")
        self.list_is_empty = (By.XPATH, "//div[contains(text(), 'empty')]")

    def open_app(self, app_name):
        self.wait_to_click(self.webapps_home)
        self.application = self.get_element(self.app_name_format, app_name)
        self.application_header = self.get_element(self.app_header_format, app_name)
        self.wait_to_click(self.application)
        self.is_visible_and_displayed(self.application_header, timeout=200)

    def open_app_home(self, app_name):
        self.app_home = self.get_element(self.app_breadcrumb_format, app_name)
        self.js_click(self.app_home)

    def open_menu(self, menu_name):
        self.caselist_menu = self.get_element(self.menu_name_format, menu_name)
        self.caselist_header = self.get_element(self.menu_name_header_format, menu_name)
        self.wait_to_click(self.caselist_menu)
        assert self.is_visible_and_displayed(self.caselist_header)

    def open_form(self, form_name):
        self.form_name = self.get_element(self.form_name_format, form_name)
        self.wait_to_click(self.form_name)

    def search_all_cases(self):
        self.scroll_to_element(self.search_all_cases_button)
        self.wait_to_click(self.search_all_cases_button)

    def search_again_cases(self):
        self.scroll_to_element(self.search_again_button)
        self.click(self.search_again_button)

    def clear_selections_on_case_search_page(self):
        self.js_click(self.clear_case_search_page)

    def search_button_on_case_search_page(self, enter_key=None):
        if enter_key == "YES":
            self.send_keys(self.submit_on_case_search_page, Keys.ENTER)
        else:
            self.js_click(self.submit_on_case_search_page)
        self.is_visible_and_displayed(self.case_list)
        self.is_visible_and_displayed(self.search_again_button)

    def clear_and_search_all_cases_on_case_search_page(self):
        self.clear_selections_on_case_search_page()
        self.search_button_on_case_search_page()

    def omni_search(self, case_name):
        self.wait_to_clear_and_send_keys(self.omni_search_input, case_name)
        self.js_click(self.omni_search_button)
        self.case = self.get_element(self.case_name_format, case_name)
        self.is_visible_and_displayed(self.case)
        return case_name

    def select_case(self, case_name):
        self.case = self.get_element(self.case_name_format, case_name)
        self.wait_to_click(self.case)

    def select_case_and_continue(self, case_name):
        self.select_case(case_name)
        self.js_click(self.continue_button)
        form_names = self.find_elements_texts(self.form_names)
        return form_names

    def submit_the_form(self):
        self.js_click(self.form_submit)
        self.is_visible_and_displayed(self.form_submission_successful, timeout=500)

    def login_as(self, username):
        try:
            self.click(self.webapp_login)
        except NoSuchElementException:
            self.wait_to_click(self.webapps_home)
            self.click(self.webapp_login)
        self.send_keys(self.search_user_webapps, username)
        self.click(self.search_button_webapps)
        self.login_as_user = self.get_element(self.login_as_username, username)
        self.click(self.login_as_user)
        self.click(self.webapp_login_confirmation)
        logdedin_user = self.get_text(self.webapp_working_as)
        assert logdedin_user == username
        return username