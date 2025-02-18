import logging
import time

from selenium.webdriver import ActionChains

from Features.CaseSearch.constants import *
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from common_utilities.hq_login.login_page import LoginPage
from common_utilities.selenium.base_page import BasePage

""""Contains common  page elements and functions related to webapps actions"""


class WebApps(BasePage):

    def __init__(self, driver, settings):
        super().__init__(driver)
        self.settings = settings

        self.title = "//title[text()='{}']"
        self.current_page = "//a[@aria-current='page' and contains(.,'{}')]"
        self.content_container = (By.XPATH, "//div[@id='content-container']")
        self.url = self.settings['url']
        self.app_name_format = "//div[@aria-label='{}']/div/h3"
        self.app_header_format = "//h1[contains(text(),'{}')]"
        self.menu_name_format = '//*[contains(@aria-label,"{}")]'
        self.menu_name_header_format = '//*[contains(text(),"{}")]'
        self.form_name_format = "//h3[contains(text(), '{}')]"
        self.form_name_header_format = "//h1[contains(text(), '{}')]"
        self.case_name_format = "//div[@id='module-case-list']//*[contains(text(),'{}')]"
        self.breadcrumb_format = "//li[contains(@class,'breadcrumb')][contains(text(),'{}') or ./a[contains(.,'{}')]]"
        self.answer_format = "(//label[.//span[text()='{}']]/following-sibling::div//{})"
        self.per_answer_format = "(//label[.//span[text()='{}']]/following-sibling::div//{})[{}]"

        self.setting_button = (By.XPATH, "//h3[contains(@id,'setting')]")
        self.sync_button = (By.XPATH, "//button[contains(@class,'sync')]")
        self.done_button = (By.XPATH, "//button[contains(@class,'done')]")


        self.form_submit = (By.XPATH, "//div[contains(@id,'submit')]//button[contains(@class,'submit')]")
        self.form_submission_successful = (By.XPATH, "//div[contains(@class,'alert-success')][contains(text(), 'successfully saved') or .//p[contains(text(), 'successfully saved')]]")
        self.form_500_error = (By.XPATH, "//*[contains(text(),'500 :')]")
        self.search_all_cases_button = (By.XPATH,
                                        "(//*[contains(text(),'Search All')]//parent::div[@class='case-list-action-button btn-group formplayer-request']/button)[1]")
        self.search_again_button = (By.XPATH,
                                    "(//*[contains(text(),'Search Again')]//parent::div[@class='case-list-action-button btn-group formplayer-request']/button)[1]")
        self.clear_case_search_page = (By.XPATH, "//button[@id='query-clear-button']")
        self.submit_on_case_search_page = (By.XPATH, "//button[@type='submit' and @id='query-submit-button']")
        self.case_list = (By.XPATH, "//div[contains(@id,'results')][//tbody or //section[contains(@class,'list')]]")#"//table[@class='table module-table module-table-case-list']")
        self.omni_search_input = (By.ID, "searchText")
        self.omni_search_button = (By.ID, "case-list-search-button")
        self.continue_button = (By.XPATH, "//button[@id='select-case']")
        self.first_case_on_list = (By.XPATH, "(//*[@class='module-case-list-column'])[1]")

        self.webapps_home = (By.XPATH, "//i[@class='fcc fcc-flower']")
        self.webapp_login = (By.XPATH, "(//div[@class='js-restore-as-item appicon appicon-restore-as'])")
        self.search_user_webapps = (By.XPATH, "//input[@placeholder='Filter workers']")
        self.search_button_webapps = (By.XPATH, "//button/i[contains(@class,'search')]")
        self.login_as_username = "//h3/b[.='{}']"
        self.webapp_login_confirmation = (By.ID, 'js-confirmation-confirm')
        self.webapp_working_as = (By.XPATH, "//span[contains(.,'Working as')]//b")
        self.form_names = (By.XPATH, "//h3[text()]")
        self.list_is_empty = "//div[contains(text(), '{}')]"
        # Pagination
        self.last_page = (By.XPATH, "(//a[contains(@aria-label, 'Page')])[last()]")
        self.next_page = (By.XPATH, "//a[contains(@aria-label, 'Next')]")
        self.prev_page = (By.XPATH, "//a[contains(@aria-label, 'Previous')]")
        self.pagination_select = (By.XPATH, "//select[contains(@class,'per-page-limit')]")
        self.go_to_page_textarea = (By.ID, "goText")
        self.go_button = (By.ID, "pagination-go-button")
        self.value_in_data_preview = "//td[@title='{}']"
        self.data_preview = (By.XPATH, "//span[@class='debugger-title']")
        self.single_row_table = "//thead[1][.//th[{}][.='{}']]//following-sibling::tbody[1]/tr[1]/td[{}][contains(.,'{}')]"

        self.sidebar_open_app_preview = (By.XPATH, "//div[@class='preview-toggler js-preview-toggle']")
        self.iframe_app_preview = (By.XPATH, "//iframe[@class='preview-phone-window']")
        self.app_preview_model = (By.XPATH, "//div[@class='preview-phone-container']")

        self.async_restore_error = (By.XPATH, "//div[contains(@class,'alert-danger') and contains(.,'Asynchronous restore')]/button[contains(@class,'close')]")
        self.error_message = (By.XPATH, "//div[contains(@class,'alert-danger')]/button[contains(@class,'close')]")


    def open_app(self, app_name):
        time.sleep(2)
        if self.is_present_and_displayed(self.webapps_home, 20):
            self.js_click(self.webapps_home)
        self.application = self.get_element(self.app_name_format, app_name)
        self.application_header = self.get_element(self.app_header_format, app_name)
        self.scroll_to_element(self.application)
        self.js_click(self.application)
        time.sleep(10)
        self.wait_for_element(self.application_header, timeout=200)

    def navigate_to_breadcrumb(self, breadcrumb_value):
        self.link = (By.XPATH, self.breadcrumb_format.format(breadcrumb_value, breadcrumb_value))
        self.wait_for_element(self.link)
        self.js_click(self.link)
        time.sleep(5)
        self.wait_for_element((By.XPATH, self.current_page.format(breadcrumb_value)), timeout=60)

    def open_menu(self, menu_name):
        self.caselist_menu = self.get_element(self.menu_name_format, menu_name)
        self.caselist_header = self.get_element(self.menu_name_header_format, menu_name)
        self.scroll_to_element(self.caselist_menu)
        self.js_click(self.caselist_menu)
        time.sleep(5)
        self.wait_for_element((By.XPATH, self.current_page.format(menu_name)), timeout=60)
        assert self.is_visible_and_displayed(self.caselist_header)

    def open_form(self, form_name):
        self.form_header = self.get_element(self.form_name_header_format, form_name)
        if self.is_displayed(self.form_header):
            logging.info("Auto advance enabled")
        else:
            self.form_name = self.get_element(self.form_name_format, form_name)
            self.wait_for_element(self.form_name, timeout=50)
            self.scroll_to_element(self.form_name)
            self.js_click(self.form_name)
            time.sleep(5)
            self.wait_for_element((By.XPATH, self.current_page.format(form_name)), timeout=50)

    def search_all_cases(self):
        self.scroll_to_element(self.search_all_cases_button)
        self.js_click(self.search_all_cases_button)

    def search_again_cases(self):
        self.scroll_to_bottom()
        self.wait_for_element(self.search_again_button)
        self.js_click(self.search_again_button)

    def clear_selections_on_case_search_page(self):
        time.sleep(10)
        if self.is_present_and_displayed(self.error_message):
            print("Error present")
            self.js_click(self.error_message)
            time.sleep(3)
        else:
            print("No banners present")
        self.scroll_to_bottom()
        self.wait_for_element(self.clear_case_search_page)
        self.scroll_to_element(self.clear_case_search_page)
        time.sleep(2)
        self.js_click(self.clear_case_search_page)
        time.sleep(10)

    def search_button_on_case_search_page(self, enter_key=None, case_list=None):
        if enter_key == YES:
            time.sleep(2)
            ActionChains(self.driver).send_keys(Keys.ENTER).perform()
            # self.send_keys(self.submit_on_case_search_page, Keys.ENTER)
        else:
            time.sleep(2)
            self.scroll_to_element(self.submit_on_case_search_page)
            self.js_click(self.submit_on_case_search_page)
            time.sleep(10)
            self.wait_for_ajax()
        if case_list == None:
            self.is_visible_and_displayed(self.case_list, timeout=100)
        else:
            print("Case List is not displayed")

    def clear_and_search_all_cases_on_case_search_page(self):
        self.clear_selections_on_case_search_page()
        self.search_button_on_case_search_page()

    def omni_search(self, case_name, displayed=YES):
        if self.is_displayed(self.omni_search_input):
            self.wait_to_clear_and_send_keys(self.omni_search_input, case_name)
            self.wait_for_element(self.omni_search_button)
            self.js_click(self.omni_search_button)
            time.sleep(50)
        else:
            print("Split Screen Case Search enabled")
        self.case = self.get_element(self.case_name_format, case_name)
        if self.is_displayed(self.last_page) and self.is_displayed(self.case) == False:
            total_pages = int(self.get_attribute(self.last_page, "data-id")) - 1
            for page in range(total_pages):
                self.js_click(self.next_page)
                if displayed == YES:
                    assert self.is_displayed(self.case)
                    break
                elif displayed == NO:
                    assert not self.is_displayed(self.case)
        else:
            if displayed == YES:
                assert self.is_displayed(self.case)
            elif displayed == NO:
                assert not self.is_displayed(self.case)
        return case_name

    def select_case(self, case_name):
        time.sleep(5)
        self.case = self.get_element(self.case_name_format, case_name)
        self.scroll_to_element(self.case)
        self.wait_for_element(self.case)
        self.js_click(self.case)

    def select_first_case_on_list(self):
        self.case_name_first = self.get_text(self.first_case_on_list)
        self.wait_for_element(self.first_case_on_list)
        self.js_click(self.first_case_on_list)
        return self.case_name_first

    def select_first_case_on_list_and_continue(self):
        self.select_first_case_on_list()
        self.continue_to_forms()
        return self.case_name_first

    def continue_to_forms(self):
        self.wait_for_element(self.continue_button, 100)
        self.js_click(self.continue_button)
        time.sleep(10)

    def select_case_and_continue(self, case_name):
        self.select_case(case_name)
        self.continue_to_forms()
        self.wait_for_element(self.content_container, timeout=100)
        form_names = self.find_elements_texts(self.form_names)
        return form_names

    def async_restore_resubmit(self):
        time.sleep(10)
        if self.is_present_and_displayed(self.async_restore_error, 30):
            self.click(self.async_restore_error)
            time.sleep(10)
            self.scroll_to_element(self.form_submit)
            self.js_click(self.form_submit)
        else:
            print("No Asynchronous restore error present")



    def submit_the_form(self):
        time.sleep(3)
        self.wait_for_element(self.form_submit)
        self.js_click(self.form_submit)
        time.sleep(10)
        self.async_restore_resubmit()
        time.sleep(10)
        try:
            self.wait_for_element(self.form_submission_successful, timeout=50)
            assert self.is_visible_and_displayed(self.form_submission_successful, timeout=50)
        except AssertionError:
            if self.is_displayed(self.form_500_error):
                time.sleep(60)
                self.js_click(self.form_submit)
                self.wait_for_element(self.form_submission_successful, timeout=50)
                assert self.is_visible_and_displayed(self.form_submission_successful, timeout=50)
            else:
                raise AssertionError
        time.sleep(5)

    def select_user(self, username):
        self.login_as_user = self.get_element(self.login_as_username, username)
        self.wait_for_element(self.login_as_user)
        self.js_click(self.login_as_user)
        time.sleep(2)
        self.wait_for_element(self.webapp_login_confirmation)
        self.js_click(self.webapp_login_confirmation)
        time.sleep(5)
        self.wait_for_element(self.webapp_working_as, 50)
        loggedin_user = self.get_text(self.webapp_working_as)
        print("Logged in User: ", loggedin_user)
        print("User provided: ", username)
        assert loggedin_user == username

    def login_as(self, username):
        url = self.get_current_url()
        if url not in self.url:
            self.driver.get(self.url)
            time.sleep(10)
        else:
            self.js_click(self.webapps_home)
            time.sleep(10)
        try:
            self.wait_for_element(self.webapp_login)
            self.scroll_to_element(self.webapp_login)
            self.js_click(self.webapp_login)
        except NoSuchElementException:
            self.wait_to_click(self.webapps_home)
            self.wait_for_element(self.webapp_login)
            self.js_click(self.webapp_login)
        time.sleep(10)
        self.wait_for_element(self.search_user_webapps, timeout=100)
        self.send_keys(self.search_user_webapps, username)
        time.sleep(1)
        self.wait_for_element(self.search_button_webapps)
        self.js_click(self.search_button_webapps)
        time.sleep(2)
        self.select_user(username)
        return username

    def answer_question(self, question_label, input_type, input_value):
        self.answer_locator = (By.XPATH, self.answer_format.format(question_label, input_type))
        self.wait_to_clear_and_send_keys(self.answer_locator, input_value)

    def answer_repeated_questions(self, question_label, input_type, input_value):
        answer_locator = (By.XPATH, self.answer_format.format(question_label, input_type))
        elements = self.driver.find_elements(*answer_locator)
        for position in range(1, len(elements) + 1):
            per_answer_locator = (By.XPATH, self.per_answer_format.format(question_label, input_type, position))
            self.scroll_to_element(per_answer_locator)
            time.sleep(1)
            self.clear(per_answer_locator)
            self.send_keys(per_answer_locator, input_value)
            time.sleep(2)
            print(str(per_answer_locator), input_value)

    def open_domain(self, current_url, domain_name):
        env = "staging" if "staging" in current_url else "www"
        self.driver.get(f"https://{env}.commcarehq.org/a/{domain_name}/cloudcare/apps/v2/#apps")
        user_menu_url = f"https://{env}.commcarehq.org/a/casesearch/settings/users/commcare/"
        return user_menu_url

    def change_page_number(self, page_number):
        self.select_by_value(self.pagination_select, page_number)

    def switch_bw_pages(self):
        self.js_click(self.next_page)
        time.sleep(30)
        self.wait_for_element(self.prev_page)
        self.js_click(self.prev_page)
        time.sleep(30)

    def go_to_page(self, page_number):
        self.send_keys(self.go_to_page_textarea, page_number)
        self.js_click(self.go_button)

    def open_data_preview(self):
        self.js_click(self.data_preview)

    def present_in_data_preview(self, value):
        value_in_data_preview = self.get_element(self.value_in_data_preview, value)
        assert self.is_present(value_in_data_preview)

    def check_case_list_is_empty(self, empty_message):
        list_is_empty_message = self.get_element(self.list_is_empty, empty_message)
        assert self.is_displayed(list_is_empty_message)

    def check_form_table_values(self, table):
        for index, header in enumerate(table["headers"]):
            row_value = table["body"][header]
            self.is_visible_and_displayed((By.XPATH,self.single_row_table.format(index+1, header,index+1, row_value)))

    def logout_webapps(self, url):
        login = LoginPage(self.driver, self.settings['db'])
        self.get_url(url)
        login.logout()

    def login_webapps(self, user, password, link):
        login = LoginPage(self.driver, self.settings['db'])
        login.login(user, password)
        self.get_url(link)

    def bha_login_as(self, username, password, url, db):
        self.logout_webapps(db)
        self.login_webapps(username, password, url)

    def sync_app(self):
        url = self.get_current_url()
        if url not in self.url:
            self.driver.get(self.url)
            time.sleep(10)
        else:
            self.js_click(self.webapps_home)
            time.sleep(10)
        self.wait_for_element(self.setting_button)
        self.js_click(self.setting_button)
        self.wait_for_element(self.sync_button)
        self.js_click(self.sync_button)
        time.sleep(20)
        self.wait_for_element(self.done_button)
        self.js_click(self.done_button)
        time.sleep(10)

