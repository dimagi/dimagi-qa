import random
import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from AppSprintPerformanceTests.CICT.UserInputs.co_cict_user_inputs import COUserData
from common_utilities.selenium.base_page import BasePage
from AppSprintPerformanceTests.CICT.UserInputs.ny_cict_user_inputs import NYUserData
from common_utilities.decorators import timer

""""Contains test page elements and functions related to workflows in test"""


class HomePage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

        self.app_settings = (By.XPATH, "//div[@class='js-settings appicon appicon-settings']")
        self.break_pending_locks = (By.XPATH, "//button[contains(@class,'js-break-locks btn btn-sm btn-danger')]")
        self.lock_exists = (By.XPATH, "//div[contains(text(),'existed')]")
        self.clear_user_data = (By.XPATH, "//button[contains(@class,'js-clear-user-data btn btn-sm btn-danger')]")
        self.clear_user_data_success = (By.XPATH, "//div[text()='User data successfully cleared.'][last()]")
        self.done = (By.XPATH, "//button[contains(@class,'btn btn-primary js-done')]")
        self.sync_app = (By.XPATH, "//div[@class='js-sync-item appicon appicon-sync']")
        self.sync_success = (By.XPATH, "(//div[text()='User Data successfully synced.'])[last()]")
        self.login_as = (By.CSS_SELECTOR, ".js-restore-as-item")
        self.search_user = (By.XPATH, "//input[@class='js-user-query form-control']")
        self.search_confirm = (By.XPATH, "//button[@type ='submit' and @class= 'btn btn-default']")
        self.confirm_user_login = (By.XPATH, "//button[@id = 'js-confirmation-confirm']")
        self.all_cases_menu = (By.XPATH, "(//div[@aria-label='All Cases']/div)[1]")
        self.case_list_table = (By.XPATH, "//table[@class='table module-table module-table-case-list']")
        self.case_detail_modal = (By.XPATH, "//div[@id='case-detail-modal']//div[@class='modal-content']")
        self.continue_button = (By.ID, "select-case")
        self.menu_list = (By.XPATH, "//div[@class='module-menu-container']")
        self.ci_form = (By.XPATH, "//tr[@aria-label='Case Investigation']")
        self.form_content = (By.ID, "webforms")
        # CO
        self.lang_dropdown = (By.XPATH, "(//span[contains(text(),'What language')])/following::span[@class='select2-selection__rendered'][1]")
        self.lang_search = random.choice(COUserData.language_list)
        self.lang_answer = (
            By.XPATH, "//span[@class='select2-results']//ul//li[contains(text(),'" + self.lang_search + "')][1]")
        self.lang_selected_displayed = (By.XPATH, "(//span[contains(text(), '" + self.lang_search + "')])[1]")
        # NY
        self.name_of_school_dropdown = (By.XPATH, "(//*[contains(text(),'Name of university')])[1]"
                                                  "/following::span[@class='select2-selection__rendered'][1]")
        self.search_dropdown = (By.XPATH, "//span[@class='select2-search select2-search--dropdown']")
        self.school_search = random.choice(NYUserData.school_list)
        self.name_of_school_answer = (
            By.XPATH, "//span[@class='select2-results']//ul//li[contains(text(),'" + self.school_search + "')][1]")
        self.school_selected_displayed = (By.XPATH, "//span[contains(text(), '" + self.school_search + "')]")

        self.submit_form = (By.XPATH, "//button[@type='submit' and @class='submit btn btn-primary']")
        self.form_submission_success = (By.XPATH, "//p[text()='Form successfully saved!']")
        self.all_contacts_menu = (By.XPATH, "(//div[@aria-label='All Contacts']/div)[1]")
        self.cm_form = (By.XPATH, "//tr[@aria-label='Contact Monitoring']")
        self.cn_form = (By.XPATH, "//tr[@aria-label='Contact Notification']")
        self.search_case_list = (By.ID, "searchText")
        self.search_button = (By.ID, "case-list-search-button")
        self.use_web_user = (By.XPATH, "//a[@class='js-clear-user']")

    def break_locks_and_clear_user_data(self, project_space):
        self.webapps_home = (
            By.XPATH, "//a[@href='/a/" + project_space + "/cloudcare/apps/v2/' and @class='navbar-brand']")
        try:
            self.wait_to_click(self.app_settings)
        except TimeoutException:
            self.wait_to_click(self.webapps_home)
            self.wait_to_click(self.app_settings)
        self.wait_to_click(self.break_pending_locks)
        if self.is_displayed(self.lock_exists):
            time.sleep(180)
        self.wait_to_click(self.clear_user_data)
        self.wait_for_element(self.clear_user_data_success, timeout=240)
        self.wait_to_click(self.done)
        self.wait_to_click(self.webapps_home)

    def login_as_ci_ct_user(self, username, url):
        self.ci_ct_user = (By.XPATH, "//b[contains(text(),'" + username + "')]")
        try:
            self.wait_to_click(self.login_as)
            self.wait_to_clear_and_send_keys(self.search_user, username)
            self.wait_to_click(self.search_confirm)
            
        except TimeoutException:
            try:
                self.wait_to_clear_and_send_keys(self.search_user, username)
                self.wait_to_click(self.search_confirm)
            except TimeoutException:
                self.wait_to_click(self.webapps_home)
                self.wait_to_click(self.login_as)
                self.wait_to_clear_and_send_keys(self.search_user, username)
                self.wait_to_click(self.search_confirm)
        try:
            self.wait_to_click(self.ci_ct_user)
        except TimeoutException:
            self.wait_to_click(self.ci_ct_user)
        try:
            self.wait_to_click(self.confirm_user_login)
        except TimeoutException:
            self.wait_to_click(self.confirm_user_login)
        self.wait_for_element(self.ci_ct_user, timeout=240)

    @timer
    def sync_application(self, username, application_name):
        self.wait_to_click(self.sync_app)
        self.wait_for_element(self.sync_success, timeout=900)

    @timer
    def open_application(self, application_name, username):
        self.pre_application = (By.XPATH, '//div[contains(@aria-label,"' + application_name + '")]')
        self.app_name_in_breadcrumb = (By.XPATH, "//ol//li[contains(.,'" + application_name + "')]")
        self.wait_to_click(self.pre_application)
        self.wait_for_element(self.app_name_in_breadcrumb, timeout=240)

    @timer
    def all_cases_menu_load(self, application_name, username):
        self.wait_to_click(self.all_cases_menu)
        self.wait_for_element(self.case_list_table, timeout=240)

    def search_case_in_test(self, application_name, username, pre_configured_case):
        self.preconfig_case = (By.XPATH, "(//tr[.//td[text()='" + pre_configured_case +
                               "' and @class='module-case-list-column']])[1]")
        self.wait_to_clear_and_send_keys(self.search_case_list, pre_configured_case)
        self.wait_to_click(self.search_button)
        time.sleep(10)
        self.wait_for_element(self.preconfig_case, timeout=240)

    @timer
    def open_case_detail(self, application_name, username, pre_configured_case):
        self.preconfig_case = (By.XPATH, "(//tr[.//td[text()='" + pre_configured_case +
                               "' and @class='module-case-list-column']])[1]")
        self.wait_to_click(self.preconfig_case)
        self.wait_for_element(self.case_detail_modal, timeout=240)

    @timer
    def case_menu_display(self, application_name, username):
        self.wait_to_click(self.continue_button)
        self.wait_for_element(self.menu_list, timeout=240)

    @timer
    def open_case_investigation_form(self, application_name, username):
        self.wait_to_click(self.ci_form)
        self.wait_for_element(self.form_content, timeout=240)

    @timer
    def ci_form_answer_question(self, application_name, username, site):
        if site == "NY":
            self.scroll_to_element(self.name_of_school_dropdown)
            self.driver.execute_script("window.scrollBy(0,-80)")
            self.wait_to_click(self.name_of_school_dropdown)
            time.sleep(0.5)
            self.wait_to_click(self.name_of_school_answer)
            self.wait_for_element(self.school_selected_displayed, timeout=240)
        elif site == "CO":
            self.scroll_to_element(self.lang_dropdown)
            self.driver.execute_script("window.scrollBy(0,-80)")
            self.wait_to_click(self.lang_dropdown)
            self.wait_to_click(self.lang_answer)
            print(self.lang_search)
            self.wait_for_element(self.lang_selected_displayed, timeout=240)

    @timer
    def ci_form_submission(self, application_name, username):
        self.wait_to_click(self.submit_form)
        self.wait_for_element(self.form_submission_success, timeout=240)

    def app_home_screen(self, app_in_test):
        self.app_home = (By.XPATH, "//ol//li[contains(.,'" + app_in_test + "')]")
        self.wait_to_click(self.app_home)

    @timer
    def all_contacts_menu_load(self, application_name, username):
        self.wait_to_click(self.all_contacts_menu)
        self.wait_for_element(self.case_list_table, timeout=240)

    def search_contact_in_test(self, application_name, username, pre_configured_contact):
        self.preconfig_contact = (By.XPATH, "(//tr[.//td[text()='" + pre_configured_contact +
                                  "' and @class='module-case-list-column']])[1]")
        self.wait_to_clear_and_send_keys(self.search_case_list, pre_configured_contact)
        self.wait_to_click(self.search_button)
        time.sleep(10)
        self.wait_for_element(self.preconfig_contact, timeout=240)

    @timer
    def open_contact_detail(self, application_name, username):
        self.wait_to_click(self.preconfig_contact)
        self.wait_for_element(self.case_detail_modal, timeout=240)

    @timer
    def contact_menu_display(self, application_name, username):
        self.wait_to_click(self.continue_button)
        self.wait_for_element(self.menu_list, timeout=240)

    @timer
    def open_contact_monitoring_form(self, application_name, username):
        self.click(self.cm_form)
        self.wait_for_element(self.form_content, timeout=240)

    @timer
    def open_contact_notification_form(self, application_name, username):
        self.click(self.cn_form)
        self.wait_for_element(self.form_content, timeout=240)

    @timer
    def cm_form_answer_question(self, application_name, username):
        self.scroll_to_element(self.name_of_school_dropdown)
        self.driver.execute_script("window.scrollBy(0,-80)")
        self.wait_to_click(self.name_of_school_dropdown)
        self.wait_to_click(self.name_of_school_answer)

    @timer
    def cn_form_answer_question(self, application_name, username):
        self.scroll_to_element(self.lang_dropdown)
        self.driver.execute_script("window.scrollBy(0,-80)")
        self.wait_to_click(self.lang_dropdown)
        self.wait_to_click(self.lang_answer)
        self.wait_for_element(self.lang_selected_displayed, timeout=240)

    @timer
    def cm_form_submission(self, application_name, username):
        self.wait_to_click(self.submit_form)
        self.wait_for_element(self.form_submission_success, timeout=240)

    @timer
    def cn_form_submission(self, application_name, username):
        self.wait_to_click(self.submit_form)
        self.wait_for_element(self.form_submission_success, timeout=240)

    def back_to_webapps_home(self):
        self.wait_to_click(self.webapps_home)
        self.wait_for_element(self.use_web_user)
        self.wait_to_click(self.use_web_user)
        assert not self.is_displayed(self.use_web_user)
