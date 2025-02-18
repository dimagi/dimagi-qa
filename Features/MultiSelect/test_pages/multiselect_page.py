import time

from selenium.webdriver.common.by import By

from common_utilities.selenium.base_page import BasePage
from Features.CaseSearch.constants import *

""""Contains test page elements and functions related to the Case Search functionality"""


class MultiSelectWorkflows(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

        self.row_checkbox_xpath = "(//input[contains(@class,'select-row-checkbox') and @type='checkbox'])[{}]"
        self.value_in_table_format = "(//td[@class='module-case-list-column-checkbox']//following::td[@class='module-case-list-column'][1])[{}]"
        self.select_all_checkbox = (By.ID, "select-all-checkbox")
        self.case_names = (By.XPATH, "//td[contains(@class,'case-list-column')][3]")
        self.multi_select_continue = (By.XPATH, "(//button[contains(@class,'multi-select-continue-btn')])[1]")
        self.selected_case_names_on_forms = "//span[contains(@class,'webapp-markdown-output')][contains(.,'{}:')]"
        self.select_case_button = (By.ID, "select-case")
        self.checkbox = "(//td[@class='module-case-list-column' and text() = '{}'][1]//preceding::input[1])[1]"
        self.dropdown_menu_value = (By.XPATH, "//*[contains(@data-bind,'moduleOptions, value')]/option")
        self.max_limit_error = (By.XPATH, "//div[contains(text(),'Too many cases')]")
        self.open_app_builder_menu = "//span[contains(text(),'{}')]"
        self.case_list_settings = (By.XPATH, "//a[@href='#case-detail-screen-config-tab']")
        """Case Tiles"""
        self.case_tile_grid_one = "(//div[@class='list-grid-style-1 box'])[{}]"
        self.select_all_tile_checkbox = (By.ID, "select-all-tile-checkbox")

    def multi_select_cases(self, case_count):
        song_names = []
        for i in range(1, case_count+1):
            row_checkbox = self.get_element(self.row_checkbox_xpath, str(i))
            time.sleep(2)
            self.js_click(row_checkbox)
            case_name_in_table = self.get_element(self.value_in_table_format, str(i))
            selected_song_names = self.get_text(case_name_in_table)
            song_names.append(selected_song_names)
        return song_names

    def multi_select_case_tiles(self, case_count):
        song_names = []
        for i in range(1, case_count+1):
            row_checkbox = self.get_element(self.row_checkbox_xpath, str(i))
            self.js_click(row_checkbox)
            case_name_in_table = self.get_element(self.case_tile_grid_one, str(i))
            song_on_case_tiles = self.get_text(case_name_in_table)
            stripped_song = song_on_case_tiles.split("</b>")
            selected_song_names = stripped_song[1]
            song_names.append(selected_song_names)
            print(song_names)
        return song_names

    def click_select_all_checkbox(self):
        self.js_click(self.select_all_checkbox)

    def click_select_all_tile_checkbox(self):
        self.js_click(self.select_all_tile_checkbox)

    def continue_to_proceed_multiselect(self):
        self.js_click(self.multi_select_continue)
        self.wait_for_ajax()

    def check_no_of_cases_on_form(self, max_size, type):
        song_names_on_form = self.find_elements_texts((By.XPATH, self.selected_case_names_on_forms.format(type)))
        size = len(song_names_on_form)
        print(size)
        assert size < max_size, "Number of forms exceeded the max size "+max_size
        print("Number of forms within limit")

    def check_error_message_shown_for_max_limit_exceed(self):
        assert self.is_displayed(self.max_limit_error), "Max limit error not displayed"
        print("Max limit error displayed as expected")

    def check_selected_cases_present_on_form(self, items_selected_on_case_list, case_type):
        time.sleep(5)
        stripped_final = None
        song_names_on_form = self.find_elements_texts((By.XPATH, self.selected_case_names_on_forms.format(str(case_type).lower())))
        if case_type == SONG:
            stripped = list(filter(None, [s.partition(" by")[0] for s in song_names_on_form]))
            stripped_final = list(filter(None, [s.replace("song: ", "") for s in stripped]))
        elif case_type == SHOW:
            stripped = list(filter(None, [s.replace("show:", "") for s in song_names_on_form]))
            stripped_final = list(filter(None, [s.lstrip() for s in stripped]))
        assert items_selected_on_case_list == stripped_final, f"No, list1 {items_selected_on_case_list} doesn't match list2{stripped_final}"
        print(f"List1 {items_selected_on_case_list} matches List2 {stripped_final}")

    def select_case_on_case_detail(self):
        self.js_click(self.select_case_button)

    def check_if_checkbox_is_selected(self, case_name):
        checkbox = self.get_element(self.checkbox, case_name)
        assert self.is_selected(checkbox), "Checkbox for "+case_name+" is not selected"
        print("Checkbox for "+case_name+" is selected")

    def check_if_checkbox_are_selected(self, case_names):
        for case in case_names:
            checkbox = self.get_element(self.checkbox, case)
            assert self.is_selected(checkbox), "Checkbox for "+case+" is not selected"
            print("Checkbox for "+case+" is selected")

    def check_if_value_present_in_drop_down(self, menu_name_input, match=None):
        menu_names = self.find_elements_texts(self.dropdown_menu_value)
        if match == NO:
            assert menu_name_input not in menu_names, "Names should not match"
            print("Input name"+str(menu_name_input)+" not in "+str(menu_names))
        elif match == YES:
            assert menu_name_input in menu_names, "Names should match"
            print("Input name"+str(menu_name_input)+" present in "+str(menu_names))

    def open_menu_settings(self, menu):
        menu_xpath = self.get_element(self.open_app_builder_menu, menu)
        self.wait_for_element(menu_xpath)
        self.js_click(menu_xpath)
        time.sleep(2)
        self.wait_for_element(self.case_list_settings)
        self.js_click(self.case_list_settings)





