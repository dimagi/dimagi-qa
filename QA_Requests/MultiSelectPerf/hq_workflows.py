import time

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from common_utilities.selenium.base_page import BasePage
from common_utilities.decorators import timer


class AppCreationPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

        self.app_name = "500k_data"
        self.add_questions = (By.XPATH, "//div[@class='dropdown fd-add-question-dropdown']")
        self.hidden_value = (By.XPATH, "//*[@data-qtype='DataBindOnly']")
        self.label_value = (By.XPATH, "//*[@data-qtype='Trigger']")
        self.calc_cond = (By.XPATH, "//*[@name='property-calculateAttr']")
        self.ques_id = (By.ID, "property-nodeID")
        self.form_name_save_button = (By.XPATH, "//span[text()='Save']")
        self.display_text = (By.XPATH, "//*[@name='itext-en-label']")
        self.here = (By.XPATH, "(//a[@role='treeitem'])[2]")

        # Readings Capture
        self.sync_app = (By.XPATH, "//div[@class='js-sync-item appicon appicon-sync']")
        self.sync_success = (By.XPATH, "(//div[text()='User Data successfully synced.'])[last()]")
        self.app_500k = (By.XPATH, '//h3[contains(text(), "Multi for 500k-data")]')
        self.into_the_app = (By.XPATH, "//h1[text()='Multi for 500k-data']")
        self.menu_name = "//*[@aria-label='{}']/div"
        self.menu_name_header = "//*[text()='{}']"
        self.search_all_cases_button = (By.XPATH, "//button[text()='Search All Cases']")
        self.search_again_button = (By.XPATH, "//button[text()='Search Again']")
        self.submit_on_case_search_page = (By.XPATH, "//button[@type='submit' and @id='query-submit-button']")
        self.case_list = (By.XPATH, "//table[@class='table module-table module-table-case-list']")
        self.page2 = (By.XPATH, "//a[@aria-label='Page 2']")
        self.omni_search_input = (By.ID, "searchText")
        self.omni_search_button = (By.ID, "case-list-search-button")
        self.pagination_select = (By.XPATH, "//select[@class='form-control per-page-limit']")
        self.select_all_checkbox = (By.ID, "select-all-checkbox")
        self.continue_button = (By.ID, "multi-select-continue-btn")
        self.form_name = (By.XPATH, '//h1[contains(text(),"Update songs you picked out")]')
        self.form_submit = (By.XPATH, "//button[@class='submit btn btn-primary']")
        self.form_submission_successful = (By.XPATH, "//p[contains(text(), 'Form successfully saved')]")

    def pass_prop_to_case_list(self, url, start_range, stop_range):
        self.driver.get(url)
        for i in range(start_range, stop_range):
            self.wait_to_click(self.here)
            
            self.click(self.add_questions)
            
            self.wait_to_click(self.hidden_value)
            prop_name = 'prop{}p'.format(i)
            self.xpath_value = "instance('casedb')/casedb/case[@case_id = current()/../@id]/" + prop_name
            print(self.xpath_value)
            self.wait_to_clear_and_send_keys(self.calc_cond, self.xpath_value)
            self.wait_to_clear_and_send_keys(self.ques_id, prop_name)
            self.wait_to_click(self.form_name_save_button)
            prop_name_full = "#form/here_are_your_cases/item/" + prop_name
            label = "prop_name " + prop_name_full
            
            self.click(self.add_questions)
            
            self.wait_to_click(self.label_value)
            self.wait_to_clear_and_send_keys(self.display_text, label)
            self.wait_to_click(self.form_name_save_button)

    @timer
    def sync_user(self):
        self.driver.get("https://www.commcarehq.org/a/casesearch/cloudcare/apps/v2/#apps")
        self.wait_to_click(self.sync_app)
        self.wait_for_element(self.sync_success, timeout=500)

    def open_app(self):
        self.driver.get("https://www.commcarehq.org/a/casesearch/cloudcare/apps/v2/#apps")
        self.wait_to_click(self.app_500k)
        self.is_visible_and_displayed(self.into_the_app, timeout=200)

    @timer
    def open_case_list_menu(self, caselist):
        self.caselist_menu = (By.XPATH, self.menu_name.format(caselist))
        self.case_list_header = (By.XPATH, self.menu_name_header.format(caselist))
        self.wait_to_click(self.caselist_menu)
        self.wait_for_element(self.case_list_header)

    def search_all_cases(self):
        try:
            self.wait_to_click(self.search_all_cases_button)
        except TimeoutException:
            pass

    @timer
    def search_all_cases_on_case_search_page(self):
        self.wait_to_click(self.submit_on_case_search_page)
        self.is_visible_and_displayed(self.case_list)

    def change_page_number(self, page_number):
        self.select_by_value(self.pagination_select, page_number)

    @timer
    def switch_bw_pages(self):
        self.wait_to_click(self.page2)
        self.wait_for_ajax()

    # Goes to base page
    def wait_for_ajax(self):
        wait = WebDriverWait(self.driver, 15)
        bool1 = wait.until(lambda driver: self.driver.execute_script('return jQuery.active') == 0)
        bool2 = wait.until(lambda driver: self.driver.execute_script('return document.readyState') == 'complete')
        print(bool1, bool2)

    def omni_search(self, search_input):
        self.wait_to_clear_and_send_keys(self.omni_search_input, search_input)

    @timer
    def omni_results(self):
        self.wait_to_click(self.omni_search_button)
        self.wait_for_ajax()

    def multi_select_cases(self):
        self.wait_to_click(self.search_again_button)
        self.wait_to_click(self.submit_on_case_search_page)
        self.wait_to_click(self.select_all_checkbox)

    @timer
    def open_and_load_form(self):
        self.wait_to_click(self.continue_button)
        self.is_visible_and_displayed(self.form_name, timeout=500)

    @timer
    def submit_the_form(self):
        self.wait_to_click(self.form_submit)
        self.is_visible_and_displayed(self.form_submission_successful, timeout=500)
