import os.path
import time
from time import sleep

from selenium.common import TimeoutException, ElementClickInterceptedException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from common_utilities.selenium.base_page import BasePage
from common_utilities.generate_random_string import fetch_random_string
from common_utilities.path_settings import PathSettings
from Features.Powerbi_integration_exports.userInputs.user_inputs import UserData


""""Contains test page elements and functions related to the Lookup Table module"""

class PowerBiPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.Data = (By.LINK_TEXT, "Data")
        self.view_all = (By.LINK_TEXT, "View All")
        self.power_bi = (By.XPATH, "//*[@id='hq-sidebar']/nav/ul[1]/li[7]/a")
        self.add_odata_feed = (By.XPATH, "//*[@id='create-export']/p/a")
        self.disabled = (By.XPATH,"//*[@data-bind='visible: showSubmit, disable: disableSubmit']")
        self.feed_type = (By.XPATH,"//select[@id='id_model_type']")
        self.feed_type_visible = (By.XPATH,"//*[@data-bind='visible: modelType()']")
        self.case_type = (By.XPATH,"//*[@for='id_case_type']")
        self.cancel_button = (By.XPATH,"//*[@id='createExportOptionsModal']/div/form/div/div[7]/button[1]")
        self.applications = (By.XPATH,"//select[contains(@name,'application')]")
        self.app_dropdown = (By.XPATH,"//input[contains(@aria-controls,'id_application-results')]")
        self.users_list_item = "//ul[@role='listbox']/li[contains(.,'{}')]"
        self.menu =(By.XPATH,"//select[contains(@name,'module')]")
        self.menu_select = (By.XPATH,"//input[@aria-controls='select2-id_module-results']")
        self.form = (By.XPATH,"//select[contains(@placeholder,'Select Form')]")
        self.add_export_conf = (By.XPATH, "//button[@data-bind='visible: showSubmit, disable: disableSubmit']")
        self.submission_msg = (By.XPATH, "//span[contains(@data-bind,'text: submissionCountText')]")
        self.case = (By.XPATH,"//span[@aria-controls='select2-id_case_type-container']")
        self.case_select = (By.XPATH,"//input[@aria-controls='select2-id_case_type-results']")
        self.save = (By.XPATH,"//button[@type='submit'][contains(@data-bind,'click: save')]")
        self.settings = (By.XPATH, "//*[@id='customize-export']/header/div/div/h3")
        self.success = (By.XPATH,"//*[@class='alert alert-margin-top fade in alert-success']")
        self.odata_feed_name = (By.XPATH,"//input[@id='export-name']")
        self.powerBI_tab_int = (By.LINK_TEXT, "PowerBi/Tableau Integration")
        self.select_all_btn = (By.XPATH, '//button[@data-bind="click: selectAll"]')
        self.delete_selected_exports = (By.XPATH, '//a[@href= "#bulk-delete-export-modal"]')
        self.bulk_delete_confirmation_btn = (By.XPATH, '//button[@data-bind="click: BulkExportDelete"]')
        self.show_advance = (By.XPATH, "//span[@data-bind='visible: !table.showAdvanced()']")
        self.hide_advance = (By.XPATH,"//span[@data-bind='visible: table.showAdvanced']")
        self.show_delete = (By.XPATH,"//span[@data-bind='visible: !table.showDeleted()']")
        self.copy_edit_button = (By.XPATH,"(//*[@data-bind='if: isOData()'])[1]")
        self.description = (By.XPATH,("//*[@id='export-description']"))
        self.disabled1 =(By.XPATH,("//td[5][./input[@disabled]]//preceding-sibling::td//input[@type='checkbox' and @disabled='disabled']"))
        self.copy_odata_feed = (By.XPATH,("//*[@id='export-list']/div[2]/div[1]/div[2]/table/tbody/tr/td[2]/div/span/a"))
        self.link = (By.XPATH,("//*[@id='export-list']/div[2]/div[1]/div[2]/table/tbody/tr/td[2]/div/input"))
        self.delete = (By.XPATH,("(//a[@data-bs-toggle='modal'])[9]"))
        self.delete_button = (By.XPATH,("//*[@id='export-list']/div[2]/div[1]/div[2]/table/tbody/tr/td[5]/div/a"))
        self.edit_filter = (By.XPATH,("//*[@id='export-list']/div[2]/div[1]/div[2]/table/tbody/tr/td[3]/a[2]"))
        self.daterange =(By.XPATH,("//*[@id='id_date_range']"))
        self.save_filter = (By.XPATH,("//*[@id='setFeedFiltersModal']/div/form/div/div[3]/button[2]"))
        self.pagination = (By.XPATH,("//*[@id='export-list']/div[2]/div[1]/div[2]/pagination/div/div/div[2]/nav/ul/li[3]/a"))
        self.delete_question = (By.XPATH,("//span[@data-bind='visible: !table.showDeleted()']"))
        self.process = (By.XPATH, "//*[@id='export-process-deleted-applications']/div/div/div[3]/button[2]")
        self.refresh_page = (By.XPATH, "//*[@id='export-process-deleted-applications']/div/div/div[3]/button[2]")
        self.hide_delete_question = (By.XPATH,"//*[@data-bind='visible: table.showDeleted()']")
        self.allow_sensitive = (By.XPATH, "//*[@id='customize-export']/form/fieldset[3]/button")
        self.de_identified1 = (By.XPATH,"//*[@id='is_deidentified']")
        self.label = (By.XPATH,"/html/body/div[1]/div[4]/div/div[2]/div[4]/div[2]/div[1]/div[2]/table/tbody/tr/td[2]/h4/label")
        self.check_data = (By.XPATH, "//*[contains(text(), '@odata.context')]")
        self.copy_odata_link = (By.XPATH,"//*[@id='export-list']/div[2]/div[1]/div[2]/table/tbody/tr/td[2]/div[2]/button" )
        self.copy_odata_link_form = (By.XPATH,"(//*[contains(@class,'form-control input-sm')])[1]")
        self.copy_odata_link_btn_form = (
            By.XPATH,
            "//div[contains(@data-bind,'text-body-secondary')][.//span[text()='"+ UserData.name +"']]//following-sibling::div[contains(@data-bind,'showLink')]//button")
        self.repeat_checkbox = (By.XPATH,"//*[@id='customize-export']/form/fieldset[2]/div[2]/legend/span[1]/input")
        self.parent_checkbox = (By.XPATH,"//*[@id='customize-export']/form/fieldset[2]/div[3]/legend/span[1]/input")
        self.case_id_duplicate =(By.XPATH,"//body[1]/div[1]/div[3]/div[1]/div[2]/div[2]/form[1]/fieldset[2]/div[1]/div[1]/table[1]/tbody[1]/tr[9]/td[1]/input[1]")
        self.repeat_checkbox1 =(By.XPATH,"//*[@id='customize-export']/form/fieldset[2]/div[4]/legend/span[1]/input")

    def ui(self):
        self.wait_to_click(self.power_bi,2)
        self.power_bi_tableau_integration_bulk_delete()
        self.wait_to_click(self.add_odata_feed)

    def select_feed_type(self):
        self.is_present_and_displayed(self.disabled,10)
        print("Add OData Feed button is disabled")

    def select_form(self):
        self.wait_to_click(self.feed_type,50)
        ss = Select(self.find_element(self.feed_type))
        ss.select_by_visible_text('Form')
        self.is_present_and_displayed(self.feed_type_visible)
        print("App type, application,Menu , form are displayed")

    def application_dropdown(self,selectapp):
        self.wait_to_click(self.applications)
        app_dropdown=[]
        app_dropdown=(self.find_elements_texts(self.applications))
        time.sleep(10)
        print(app_dropdown)
        self.wait_to_click(self.applications)
        self.select_by_text(self.applications,selectapp)

    def menu_dropdown(self):
        self.wait_to_click(self.menu)
        menu_dropdown=[]
        menu_dropdown=(self.find_elements_texts(self.menu_select))
        time.sleep(10)
        print(menu_dropdown)

    def select_case(self):
        self.wait_to_click(self.feed_type,30)
        ss = Select(self.find_element(self.feed_type))
        # Select option by visible text
        ss.select_by_visible_text('Case')
        self.is_present_and_displayed(self.case_type,15)
        print("case type field displayed")

    def cancel(self):
        time.sleep(10)
        self.wait_to_click(self.cancel_button,10)

    def form_feed(self,appselect,menu_select,form_select):
        self.wait_to_click(self.applications)
        self.select_by_text(self.applications,appselect)
        self.wait_to_click(self.menu)
        self.select_by_text(self.menu,menu_select)
        self.wait_to_click(self.form)
        self.select_by_text(self.form,form_select)
        self.is_present_and_displayed(self.submission_msg)
        print("Form submission message displayed")

    def add_odata(self):
        self.wait_to_click(self.add_export_conf)
        self.is_present_and_displayed(self.settings,10)
        print ("odata feed settings page displayed")
        self.wait_to_click(self.odata_feed_name)
        self.wait_to_clear_and_send_keys(self.odata_feed_name,UserData.name+Keys.TAB)
        self.wait_to_click(self.case_id_duplicate)
        self.scroll_to_bottom()
        self.is_present_and_displayed(self.save,10)

    def repeat_checkbox2(self):
        self.scroll_to_element(self.repeat_checkbox)
        self.wait_to_click(self.repeat_checkbox)
        self.scroll_to_element(self.repeat_checkbox1)
        self.wait_to_click(self.repeat_checkbox1)

    def parent_checkbox1(self):
        self.scroll_to_element(self.parent_checkbox)
        self.js_click(self.parent_checkbox,2)


    def delete_bulk_exports(self):
        try:
            self.wait_to_click(self.select_all_btn)
            self.wait_to_click(self.delete_selected_exports)
            self.wait_to_click(self.bulk_delete_confirmation_btn)
            time.sleep(10)
        except TimeoutException:
            print("No exports available")


    def power_bi_tableau_integration_bulk_delete(self):
        try:
            self.wait_and_sleep_to_click(self.powerBI_tab_int)
        except ElementClickInterceptedException:
            self.js_click(self.powerBI_tab_int)
        self.delete_bulk_exports()

    def case_feed(self,select_case):
        self.wait_to_click(self.case,10)
        self.wait_for_element(self.case_select)
        self.send_keys(self.case_select, select_case)
        self.wait_to_click((By.XPATH, self.users_list_item.format(select_case)))

    def save_odata_feed(self):
        self.js_click(self.save)
        time.sleep(2)
        self.is_present_and_displayed(self.success,10)
        print("odata feed is created")

    def show_advance_question(self):
        self.wait_to_click(self.show_advance)
        self.wait_to_click(self.hide_advance)
        self.is_present_and_displayed(self.show_advance)
        self.is_present_and_displayed(self.show_delete)
        print("show advance and show delete questions buttons are displayed")

    def copy_edit_feed(self):
        self.wait_to_click(self.copy_edit_button,20)
        self.wait_to_click(self.odata_feed_name)
        self.wait_to_clear_and_send_keys(self.odata_feed_name,UserData.updatedname)
        self.wait_to_click(self.save)

    def odata_20(self):
        self.wait_to_click(self.description,5)
        self.send_keys(self.description, UserData.description+Keys.TAB)
        assert self.is_present_and_displayed(self.disabled1,10)
        print("disabled button present")
        self.scroll_to_bottom()
        time.sleep(2)
        self.js_click(self.save)
        print("clicked on saved button")
        self.is_present_and_displayed(self.success, 10)



    def delete1(self):
        self.wait_to_click(self.delete)
        self.wait_to_click(self.delete_button)

    def edit_filters(self):
        self.wait_to_click(self.edit_filter,2)
        self.wait_to_click(self.daterange, 5)
        ss = Select(self.find_element(self.daterange))
        # Select option by visible text
        ss.select_by_visible_text('Last year')
        self.wait_to_click(self.save_filter,10)
        self.wait_to_click(self.edit_filter)
        print("Data range values", self.daterange)

    def create_multiple_odatafeed(self,no_of_feeds):
        for i in range(1,no_of_feeds):
            self.ui()
            self.select_form()
            self.form_feed(UserData.reassign_cases_application,UserData.reassign_menu,UserData.reassign_form)
            self.add_odata()
            self.save_odata_feed()


    def go_to_page(self):
        self.wait_to_click(self.pagination,10)
        print("pagination working fine")

    def delete_questions(self):
        self.wait_to_click(self.delete_question)
        self.is_present_and_displayed(self.hide_delete_question)
        print("Deleted questions become included in the question list for form feeds")

    def de_identified(self):
        self.scroll_to_bottom()
        self.js_click(self.allow_sensitive,2)
        self.js_click(self.de_identified1,2)
        self.js_click(self.save,10)
        self.is_present_and_displayed(self.label)
        print("odatafeed marked as de-identified")

    def view_odata_feed(self,username,password):
        self.driver.refresh()
        time.sleep(10)
        print(self.copy_odata_link_btn_form)
        self.wait_and_sleep_to_click(self.copy_odata_link_btn_form,40)
        self.get_url_paste_browser(username, password, 'forms')
        self.assert_odata_feed_data()

    def get_url_paste_browser(self, username, password, item):
        global odata_feed_link1
        if item == 'forms':
            odata_feed_link1 = self.wait_to_get_value(self.copy_odata_link_form)
        print("===="+odata_feed_link1)
        final_URL_case = f"https://{username}:{password}@{odata_feed_link1[8:]}"
        print("--------"+final_URL_case)
        time.sleep(10)
        self.driver.get(final_URL_case)

    def assert_odata_feed_data(self):
        odata_feed_data = self.driver.page_source
        verify_data = self.find_elements(self.check_data)
        assert len(verify_data) > 0, "Odata feed is Empty "
        # self.driver.close()  # Close the feed URL
        self.driver.back()