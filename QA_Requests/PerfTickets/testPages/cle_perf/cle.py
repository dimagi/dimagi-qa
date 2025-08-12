import time

from selenium.webdriver.common.by import By
from common_utilities.selenium.base_page import BasePage


class CLEPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

        self.reports_dropdown = (By.LINK_TEXT, 'Reports')
        self.cle = (By.LINK_TEXT, 'Case List Explorer')
        self.query_search = (By.XPATH, "//input[@name='search_xpath']")
        self.case_type = (By.XPATH, "//select[@id='report_filter_case_type']")
        self.apply = (By.ID, "apply-filters")
        self.report_content = (By.ID, "report-content")
        self.record_count = (By.ID, "report_table_case_list_explorer_info")
        self.remove_existing_filter = (By.XPATH, "(//*[@title='Remove item'])[1]")
        self.case_owner = (By.XPATH, "//span[@class='select2-selection select2-selection--multiple']")
        self.case_owner_loc = (By.XPATH, "//li[contains(text(),'US')]")
        self.case_owner_all = (By.XPATH, "//li[contains(text(),'All')]")
        self.sort = (By.XPATH, "(//*[@class='clickable headerSort header'])[1]")
        self.loading_none = (
            By.XPATH, "//div[@id='report_table_case_list_explorer_processing' and @style='display: none;']")
        self.loading_in_progress = (
            By.XPATH, "//div[@id='report_table_case_list_explorer_processing' and @style='display: block;']")
        self.pagination = (By.XPATH, "//select[@name='report_table_case_list_explorer_length']")

    def open_cle(self):
        self.wait_to_click(self.reports_dropdown)
        self.wait_to_click(self.cle)
        time.sleep(2)

    def search_query(self, query):
        self.wait_to_click(self.query_search)
        javaScript = "document.getElementsByName('search_xpath')[0].setAttribute('type', '')"
        self.driver.execute_script(javaScript)
        time.sleep(2)
        self.wait_to_clear_and_send_keys(self.query_search, query)

    def capture_time(self, case_type):
        start_time = time.perf_counter()
        self.case_type_in_table = (By.XPATH, "(//td[contains(text(),'" + case_type + "')])[1]")
        self.is_visible_and_displayed(self.report_content) and self.is_visible_and_displayed(
            self.case_type_in_table)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print(f'Case {case_type} executed in {run_time :.2f}s')
        self.get_text(self.record_count)
        print(self.driver.current_url)

    def sort_and_capture_time(self, case_type):
        self.wait_to_click(self.sort)
        start_time = time.perf_counter()
        self.is_visible_and_displayed(self.loading_in_progress)
        self.find_element(self.loading_none)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print(f'Sorted {case_type}  in {run_time :.2f}s')

    def capture_network_perf(self):
        items = self.driver.execute_script(
            "var performance = window.performance || {}; var network = performance.getEntries() || {}; return network;")
        for item in items:
            print(item)

    def record_cle_time(self, search_against_load, case_type, location):
        query_dict = {search_against_load: [
            "prop_value= '50' and prop_yes_no = 'yes' and prop_all_none != 'none' and prop_test_on = 'cle' and prop_loc ='us'",
            "prop_value= '100' and prop_yes_no = 'yes' and prop_all_none != 'none' and prop_test_on = 'cle' and prop_loc ='us'",
            "prop_value= '500' and prop_yes_no = 'yes' and prop_all_none != 'none' and prop_test_on = 'cle' and prop_loc ='us'",
            "prop_value= '1000' and prop_yes_no = 'yes' and prop_all_none != 'none' and prop_test_on = 'cle' and prop_loc ='us'"
        ]}

        for list in query_dict.values():
            print(list)
            for query in list:
                print(query)
                self.open_cle()
                self.search_query(query=query)
                self.select_by_text(self.case_type, case_type)
                if location == "yes":
                    self.wait_to_click(self.case_owner)
                    self.wait_to_click(self.case_owner_loc)
                    self.wait_to_click(self.remove_existing_filter)
                self.wait_to_click(self.apply)
                # self.select_by_value(self.pagination, "25")
                self.capture_time(case_type=case_type)
                self.sort_and_capture_time(case_type=case_type)
                time.sleep(10)
                # self.capture_network_perf()
                print('**************************************')

    def record_subquery_cle_time(self, search_against_load, child_case_type, parent_case_type):
        query_dict = {search_against_load: [
            'subcase-exists("parent", @case_type = "' + child_case_type + '" and fuzzy-match(name, "Anywhoop"))',
            'subcase-exists("parent", @case_type = "' + child_case_type + '"  and selected(multi_data_1, "a"))',
            'subcase-exists("parent", @case_type = "' + child_case_type + '"  and selected-any(multi_data_1, "a b"))',
            'subcase-exists("parent", @case_type = "' + child_case_type + '"  and selected-all(multi_data_1, "a b"))',
            'subcase-count("parent", @case_type = "' + child_case_type + '" and fuzzy-match(name, "Anywhoop")) >= 1',
            'subcase-count("parent", @case_type = "' + child_case_type + '"  and selected(multi_data_1, "a")) >= 1',
            'subcase-count("parent", @case_type = "' + child_case_type + '"  and selected-any(multi_data_1, "a b")) >=1',
            'subcase-count("parent", @case_type = "' + child_case_type + '"  and selected-all(multi_data_1, "a b")) >=1'
        ]}
        for list in query_dict.values():
            print(list)
            for query in list:
                print(query)
                self.open_cle()
                self.search_query(query=query)
                self.wait_to_click(self.case_owner)
                self.wait_to_click(self.case_owner_all)
                self.wait_to_click(self.remove_existing_filter)
                self.wait_to_click(self.apply)
                self.capture_time(case_type=parent_case_type)
                print('**************************************')

    def record_cle_time_without_filter(self):
        case_types = ['song_perf_1_10000', 'song_perf_1_50000', 'song_perf_1_100k', 'song_perf_1_200k',
                      'song_perf_1_1_500000']
        for case_type in case_types:
            self.open_cle()
            self.select_by_text(self.case_type, case_type)
            self.wait_to_click(self.apply)
            self.capture_time(case_type=case_type)
            self.sort_and_capture_time(case_type=case_type)
            time.sleep(10)
            print('**************************************')
