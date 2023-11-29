import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from Formplayer.testPages.webapps.webapps_basics import WebAppsBasics
from Formplayer.userInputs.user_inputs import UserData
from common_utilities.selenium.base_page import BasePage


class CaseListPage(BasePage):
    def __init__(self, driver, settings):
        super().__init__(driver)
        self.webapp = WebAppsBasics(self.driver)

        self.dashboard_link = settings['url'] + "/dashboard/project/"
        self.reports_menu_id = (By.ID, "ProjectReportsTab")
        self.view_all = (By.LINK_TEXT, "View All")
        self.show_full_menu = (By.ID, "commcare-menu-toggle")
        self.case_list_rep = (By.LINK_TEXT, "Case List")

        self.DASHBOARD_TITLE = "CommCare HQ"
        self.REPORTS_TITLE = "My Saved Reports : Project Reports :: - CommCare HQ"

        self.users_box = (By.XPATH, "//span[@class='select2-selection select2-selection--multiple']")
        self.search_user = (By.XPATH, "//textarea[@class='select2-search__field']")
        self.select_user = (By.XPATH, "//li[contains(text(),'automation_user [group]')]")
        self.app_user_select = "(//li[contains(text(),'{}')])[1]"
        self.application_select = (By.XPATH, "//select[@id='report_filter_form_app_id']")
        self.module_select = (By.XPATH, "//select[@id='report_filter_form_module']")
        self.form_select = (By.XPATH, "//select[@id='report_filter_form_xmlns']")
        self.case_type_select = (By.XPATH, "//select[@id='report_filter_case_type']")
        self.date_input = (By.XPATH, "//input[@id='filter_range']")
        self.view_form_link = (By.XPATH, "//tbody/tr[1]/td[1]/a[.='View Form']")
        self.case_name = (By.XPATH, "//td[div[contains(text(),'abc')]]")
        self.submit_history_table = (By.XPATH, "//table[@id='report_table_submit_history']/tbody/tr")
        self.apply_id = (By.ID, "apply-filters")

        # Case List
        self.search_input = (By.XPATH, "//input[@id='report_filter_search_query']")
        self.case_list_table = (By.XPATH, "//table[@id='report_table_case_list']/tbody/tr")
        self.case_id_block = (By.XPATH, "//th[@title='_id']/following-sibling::td")

        self.related_cases_tab = (By.LINK_TEXT, "Related Cases")
        self.case_properties_tab = (By.PARTIAL_LINK_TEXT, "Case Properties")
        self.view_button = "//text()[contains(.,'{}')]//following-sibling::div/a[contains(@class,'view-related-case-link')]"
        self.table_data = "//th[.//a[@data-property-name='{}']]//following-sibling::td[contains(.,'{}')]"

    def open_reports_menu(self):
        if self.is_present(self.show_full_menu):
            self.js_click(self.show_full_menu)
        self.driver.get(self.dashboard_link)
        self.wait_for_element(self.reports_menu_id)
        self.click(self.reports_menu_id)
        self.wait_to_click(self.view_all)
        assert self.REPORTS_TITLE in self.driver.title, "This is not the Reports menu page."

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

    def verify_form_data_case_list(self, test_data):
        self.webapp.wait_to_click(self.case_list_rep)
        print("Waiting some time for the data to get updated")
        time.sleep(40)
        self.webapp.wait_to_click(self.users_box)
        self.send_keys(self.search_user, UserData.automation_user)
        self.webapp.wait_to_click((By.XPATH, self.app_user_select.format(UserData.automation_user_group)))
        self.select_by_text(self.case_type_select, UserData.case_type_formplayer)
        self.send_keys(self.search_input, test_data['sub_case_name'])
        self.webapp.wait_to_click(self.apply_id)
        time.sleep(15)
        self.scroll_to_bottom()
        self.verify_table_not_empty(self.case_list_table)
        self.page_source_contains(test_data['sub_case_name'])
        self.wait_to_click((By.LINK_TEXT, str(test_data['sub_case_name'])))
        time.sleep(5)
        self.switch_to_next_tab()
        time.sleep(3)
        self.page_source_contains(test_data['sub_case_name'])
        assert True, "Sub Case name is present in Case List"
        assert self.is_present_and_displayed(
            (By.XPATH, self.table_data.format('parent_case_name', test_data['parent case name'])))
        self.webapp.wait_to_click(self.related_cases_tab)
        assert self.is_visible_and_displayed((By.XPATH, self.view_button.format(test_data['parent case name'])))
        self.webapp.wait_to_click((By.XPATH, self.view_button.format(test_data['parent case name'])))
        time.sleep(1)
        assert self.is_present_and_displayed(
            (By.XPATH, self.table_data.format('name', test_data['parent case name'])))
        assert self.is_present_and_displayed(
            (By.XPATH, self.table_data.format('data_node', test_data['data node'])))
        assert self.is_present_and_displayed(
            (By.XPATH, self.table_data.format('dateval', test_data['dateval'])))
        assert self.is_present_and_displayed(
            (By.XPATH, self.table_data.format('intval', test_data['intval'])))
        assert self.is_present_and_displayed(
            (By.XPATH, self.table_data.format('multiselect',
                                              test_data['multiselect'][0].lower()+" "+test_data['multiselect'][1].lower())))
        assert self.is_present_and_displayed(
            (By.XPATH, self.table_data.format('singleselect', test_data['singleselect'][0].lower())))
        assert self.is_present_and_displayed(
            (By.XPATH, self.table_data.format('text', test_data['text'])))
        assert self.is_present_and_displayed(
            (By.XPATH, self.table_data.format('phone_number', test_data['phone number'])))
        self.driver.close()
        self.switch_back_to_prev_tab()





