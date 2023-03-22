from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from common_utilities.selenium.base_page import BasePage
from HQSmokeTests.userInputs.user_inputs import UserData

""""Contains test page elements and functions related to the Homepage of Commcare"""


class HomePage(BasePage):

    def __init__(self, driver, settings):
        super().__init__(driver)

        self.available_application = UserData.village_application
        self.dashboard_link = settings['url']+"/dashboard/project/"
        self.dashboard_menu_id = (By.ID, "DashboardTab")
        self.reports_menu_id = (By.ID, "ProjectReportsTab")
        self.view_all = (By.LINK_TEXT, "View All")
        self.data_menu_id = (By.ID, "ProjectDataTab")
        self.users_menu_id = (By.ID, "ProjectUsersTab")
        self.applications_menu_id = (By.ID, "ApplicationsTab")
        self.web_apps_menu_id = (By.ID, "CloudcareTab")
        self.show_full_menu = (By.ID, "commcare-menu-toggle")
        self.messaging_menu_id = (By.ID, "MessagingTab")
        self.admin_menu_id = (By.ID, "AdminTab")
        self.alert_button_accept = (By.ID, "hs-eu-confirmation-button")
        self.application_path = (By.LINK_TEXT, UserData.reassign_cases_application)
        self.mobile_workers_menu_link_text = (By.LINK_TEXT, "Mobile Workers")
        self.show_full_menu_id = (By.ID, "commcare-menu-toggle")

        self.DASHBOARD_TITLE = "CommCare HQ"
        self.REPORTS_TITLE = "My Saved Reports : Project Reports :: - CommCare HQ"
        self.DATA_TITLE = "Export Form Data : Data :: - CommCare HQ"
        self.APP_TITLE = "Releases - " + UserData.reassign_cases_application + " - CommCare HQ"
        self.USERS_TITLE = "Mobile Workers : Users :: - CommCare HQ"
        self.MESSAGING_TITLE = "Dashboard : Messaging :: - CommCare HQ"
        self.WEBAPPS_TITLE = "Web Apps - CommCare HQ"

    def dashboard_menu(self):
        self.open_menu(self.dashboard_menu_id)
        self.wait_to_click(self.dashboard_menu_id)
        assert self.DASHBOARD_TITLE == self.driver.title, "This is not the Dashboard page."

    def reports_menu(self):
        try:
            self.wait_to_click(self.reports_menu_id)
        except TimeoutException:
            if self.is_displayed(self.show_full_menu_id):
                self.click(self.show_full_menu_id)
                self.click(self.reports_menu_id)
            else:
                raise TimeoutException
        self.wait_to_click(self.view_all)
        assert self.REPORTS_TITLE in self.driver.title, "This is not the Reports menu page."

    def data_menu(self):
        self.open_menu(self.data_menu_id)
        self.wait_to_click(self.view_all)
        assert self.DATA_TITLE in self.driver.title, "This is not the Data menu page."

    def applications_menu(self):
        self.open_menu(self.applications_menu_id)
        self.wait_to_click(self.application_path)
        assert self.APP_TITLE in self.driver.title, "This is not the Applications page."

    def users_menu(self):
        self.open_menu(self.users_menu_id)
        self.wait_to_click(self.view_all)
        assert self.USERS_TITLE in self.driver.title, "This is not the Users menu page."

    def messaging_menu(self):
        self.open_menu(self.messaging_menu_id)
        self.wait_to_click(self.view_all)
        assert self.MESSAGING_TITLE in self.driver.title, "This is not the Messaging menu page."

    def web_apps_menu(self):
        self.open_menu(self.web_apps_menu_id)
        self.wait_to_click(self.show_full_menu)
        assert self.WEBAPPS_TITLE in self.driver.title, "This is not the Webaspps menu page."

    def rage_clicks(self):
        # Rage Clicks on menus
        self.open_menu(self.users_menu_id)
        self.click(self.users_menu_id)
        self.click(self.users_menu_id)
        # Rage Clicks on redirect links
        self.wait_to_click(self.view_all)
        self.click(self.mobile_workers_menu_link_text)
        self.click(self.mobile_workers_menu_link_text)
        assert self.USERS_TITLE in self.driver.title, "Rage clicks failed!."

    def open_menu(self, menu):
        if self.is_present(self.show_full_menu):
            self.js_click(self.show_full_menu)
        self.driver.get(self.dashboard_link)
        self.wait_for_element(menu)
        self.wait_to_click(menu)
