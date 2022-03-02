import time
import datetime

from selenium.webdriver.support.select import Select
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, \
    UnexpectedAlertPresentException, StaleElementReferenceException, NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from HQSmokeTests.userInputs.user_inputs import UserData

"""This class contains all the generic methods and utilities for all pages"""


class BasePage:
    def __init__(self, driver):
        self.driver = driver

        self.alert_button_accept = (By.ID, "hs-eu-confirmation-button")
        self.error_404 = (By.XPATH, "//h1[contains(text(),'404')]")
        self.error_403 = (By.XPATH, "//h1[text()='403 Forbidden']")

    def page_404(self):
        try:
            self.page_404_displayed = self.is_displayed(self.error_404)
        except NoSuchElementException:
            self.page_404_displayed = False
        return self.page_404_displayed

    def page_403(self):
        try:
            self.page_403_displayed = self.is_displayed(self.error_403)
        except NoSuchElementException:
            self.page_403_displayed = False
        return self.page_403_displayed

    def cookie_alert(self):
        try:
            self.cookie_alert_displayed = self.is_displayed(self.alert_button_accept)
        except NoSuchElementException:
            self.cookie_alert_displayed = False
        return self.cookie_alert_displayed

    def wait_to_click(self, locator, timeout=12):
        element = None
        try:
            clickable = ec.element_to_be_clickable(locator)
            element = WebDriverWait(self.driver, timeout).until(clickable,
                                                                        message="Couldn't find locator: "
                                                                                + str(locator))
            element.click()
        except ElementClickInterceptedException:
            if self.cookie_alert():
                self.click(self.alert_button_accept)
                element.click()
        except UnexpectedAlertPresentException:
            alert = self.driver.switch_to.alert
            alert.accept()
            element.click()
        except StaleElementReferenceException:
            self.js_click(locator)
        except TimeoutException:
            if self.page_403():
                self.driver.back()
                element.click()
            elif self.page_404():
                self.driver.back()
                element.click()

    def wait_to_clear_and_send_keys(self, locator, user_input):
        clickable = ec.visibility_of_element_located(locator)
        element = WebDriverWait(self.driver, 5).until(clickable, message="Couldn't find locator: " + str(locator))
        element.clear()
        element.send_keys(user_input)

    def wait_to_get_text(self, locator, timeout=20):
        clickable = ec.visibility_of_element_located(locator)
        element_text = WebDriverWait(self.driver, timeout).until(clickable).text
        return element_text

    def wait_for_element(self, locator, timeout=20):
        clickable = ec.element_to_be_clickable(locator)
        WebDriverWait(self.driver, timeout).until(clickable,
                                                  message="Couldn't find locator: " + str(locator))

    def wait_and_sleep_to_click(self, locator, timeout=20):
        element = None
        try:
            time.sleep(3)
            clickable = ec.element_to_be_clickable(locator)
            element = WebDriverWait(self.driver, timeout).until(clickable,
                                                                        message="Couldn't find locator: "
                                                                                + str(locator))
            element.click()
        except ElementClickInterceptedException:
            if self.cookie_alert():
                self.click(self.alert_button_accept)
                element.click()
        except UnexpectedAlertPresentException:
            alert = self.driver.switch_to.alert
            alert.accept()
            element.click()
        except StaleElementReferenceException:
            self.js_click(locator)
        except TimeoutException:
            if self.page_403():
                self.driver.back()
                element.click()
            elif self.page_404():
                self.driver.back()
                element.click()

    def find_elements(self, locator):
        elements = self.driver.find_elements(*locator)
        return elements

    def find_element(self, locator):
        element = self.driver.find_element(*locator)
        return element

    def click(self, locator):
        element = self.driver.find_element(*locator)
        element.click()

    def select_by_text(self, source_locator, value):
        select_source = Select(self.driver.find_element(*source_locator))
        select_source.select_by_visible_text(value)

    def select_by_value(self, source_locator, value):
        select_source = Select(self.driver.find_element(*source_locator))
        select_source.select_by_value(value)

    def js_click(self, locator):
        element = self.driver.find_element(*locator)
        self.driver.execute_script("arguments[0].click();", element)
        time.sleep(1)

    def move_to_element_and_click(self, locator):
        element = self.driver.find_element(*locator)
        ActionChains(self.driver).move_to_element(element).click(element).perform()

    def clear(self, locator):
        element = self.driver.find_element(*locator)
        element.clear()

    def send_keys(self, locator, user_input):
        element = self.driver.find_element(*locator)
        element.send_keys(user_input)

    def get_text(self, locator):
        element = self.driver.find_element(*locator)
        element_text = element.text
        print(element_text)
        return element_text

    def get_attribute(self, locator, attribute):
        element = self.driver.find_element(*locator)
        element_attribute = element.get_attribute(attribute)
        print(element_attribute)
        return element_attribute

    def is_selected(self, locator):
        try:
            element = self.driver.find_element(*locator)
            is_selected = element.is_selected()
        except TimeoutException:
            is_selected = False
        return bool(is_selected)

    def is_enabled(self, locator):
        try:
            element = self.driver.find_element(*locator)
            is_enabled = element.is_enabled()
        except TimeoutException:
            is_enabled = False
        return bool(is_enabled)

    def is_displayed(self, locator):
        try:
            element = self.driver.find_element(*locator)
            is_displayed = element.is_displayed()
        except TimeoutException:
            is_displayed = False
        return bool(is_displayed)

    def is_visible_and_displayed(self, locator, timeout=30):
        try:
            visible = ec.visibility_of_element_located(locator)
            element = WebDriverWait(self.driver, timeout).until(visible, message="Element" + str(locator) + "not displayed")
            is_displayed = element.is_displayed()
        except TimeoutException:
            is_displayed = False
        return bool(is_displayed)

    def is_present_and_displayed(self, locator, timeout=100):
        try:
            visible = ec.presence_of_element_located(locator)
            element = WebDriverWait(self.driver, timeout).until(visible, message="Element" + str(locator) + "not displayed")
            is_displayed = element.is_displayed()
        except TimeoutException:
            is_displayed = False
        return bool(is_displayed)

    def switch_to_next_tab(self):
        winHandles = self.driver.window_handles
        window_after = winHandles[1]
        self.driver.switch_to.window(window_after)

    def switch_to_new_tab(self):
        self.driver.switch_to.new_window('tab')

    def switch_back_to_prev_tab(self):
        winHandles = self.driver.window_handles
        window_before = winHandles[0]
        self.driver.switch_to.window(window_before)

    def get_environment(self):
        get_env = self.driver.current_url
        env_name = get_env.split("/")[2]
        print("server : " + env_name)
        return env_name

    def get_domain(self):
        get_url = self.driver.current_url
        domain_name = get_url.split("/")[4]
        print("domain: " + domain_name)
        return domain_name

    def assert_downloaded_file(self, newest_file, file_name):
        modTimesinceEpoc = (UserData.DOWNLOAD_PATH / newest_file).stat().st_mtime
        modificationTime = datetime.datetime.fromtimestamp(modTimesinceEpoc)
        timeNow = datetime.datetime.now()
        diff_seconds = round((timeNow - modificationTime).total_seconds())
        print("Last Modified Time : ", str(modificationTime) + 'Current Time : ', str(timeNow),
              "Diff: " + str(diff_seconds))
        assert file_name in newest_file and diff_seconds in range(0, 600), "Export not completed"

    def accept_pop_up(self):
        try:
            WebDriverWait(self.driver, 3).until(ec.alert_is_present(), 'Waiting for popup to appear.')
            alert = self.driver.switch_to.alert
            alert.accept()
            print("alert accepted")
        except TimeoutException:
            print("no alert")

    def page_source_contains(self, text):
        assert text in self.driver.page_source

    def scroll_to_bottom(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

    def hover_and_click(self, locator1, locator2):
        action = ActionChains(self.driver)
        element_1 = self.driver.find_element(locator1)
        action.move_to_element(element_1).perform()
        # identify sub menu element
        element_2 = self.driver.find_element(locator2)
        # hover over element and click
        action.move_to_element(element_2).click().perform()

    def double_click(self, locator, timeout=20):
        clickable = ec.element_to_be_clickable(locator)
        element = WebDriverWait(self.driver, timeout).until(clickable,
                                                            message="Couldn't find locator: "
                                                                    + str(locator))
        # action chain object
        action = ActionChains(self.driver)
        # double click operation
        action.double_click(element)

    def js_click(self, locator, timeout=20):
        clickable = ec.element_to_be_clickable(locator)
        element = WebDriverWait(self.driver, timeout).until(clickable,
                                                            message="Couldn't find locator: "
                                                                    + str(locator))
        self.driver.execute_script("arguments[0].click();", element)