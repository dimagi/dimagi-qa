# import os
import random
import string
import time
import unittest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

app_path = 'C:\\Users\\dsi-user\\PycharmProjects\\Anroid\\apps\\commcare_2.54.1.apk'
capabilities = UiAutomator2Options().load_capabilities({
    "platformName": "Android",
    "udid": "emulator-5554",
    "automationName": "UIAutomator2",
    "deviceName": "Pixel_8_New_APK",
    "avd": "Pixel_8_New_APK",
    "appWaitPackage": "org.commcare.dalvik",
    # "appActivity": "org.commcare.activities.CommCareSetupActivity",
    "appWaitActivity": "org.commcare.activities.LoginActivity",
    # "appWaitActivity": "org.commcare.activities.DispatchActivity",
    "autoGrantPermissions": "true",
    "app": app_path,
    "noReset": "true",
    "fullReset": "false",
    "dontStopAppOnReset": "false"
    }
    )

appium_server_url = 'http://localhost:4723/wd/hub'
chars = string.ascii_lowercase + string.digits
random_string = ''.join(random.choices(chars, k=6))
random_number = random.randint(100, 19999)


class TestAppium(unittest.TestCase):
    def setUp(self) -> None:
        self.driver = webdriver.Remote(appium_server_url,
                                       options=capabilities
                                       )

        self.case_list_name = 'Case List'
        self.form_name = 'Registration Form'
        self.enter_code = "//android.widget.TextView[@text='Enter Code']"
        self.profile_code = "org.commcare.dalvik:id/edit_profile_location"
        self.start_install = "org.commcare.dalvik:id/start_install"
        self.install = "//android.widget.TextView[@text='Start Install']"
        self.username = "org.commcare.dalvik:id/edit_username"
        self.password = "org.commcare.dalvik:id/edit_password"
        self.login = "org.commcare.dalvik:id/login_button"
        self.start_button = "//android.widget.TextView[@text='Start']"
        self.sync_button = "//android.widget.TextView[@text='Sync with Server']"
        self.case_list = "//android.widget.TextView[@text='Case List']"
        self.form = "//android.widget.TextView[@text='Registration Form']"
        self.text_field = "//android.widget.EditText"
        self.radio_btn_field = "//*[@text='pune']"
        self.submit_button = "//android.widget.TextView[@text='FINISH']"
        self.next_btn = "org.commcare.dalvik:id/nav_btn_next"

        # self.go_to_menu = (AppiumBy.ID, "org.commcare.dalvik:id/connect_login_button")
        # self.password_field = (AppiumBy.ID, "org.commcare.dalvik:id/connect_password_verify_input")
        # self.password_verify_btn = (AppiumBy.ID, "org.commcare.dalvik:id/connect_password_verify_button")
        # self.my_jobs = (AppiumBy.ANDROID_UIAUTOMATOR, "new UiSelector().text(\"MY JOBS\")")
        # # self.payment_verification_job = (AppiumBy.XPATH, "//android.widget.TextView[@text=\"Payment Verifications\"]//following-sibling::android.widget.ImageView[@resource-id=\"org.commcare.dalvik:id/button\"]\n")
        # # self.verification_pay_tab =
        # self.launch_app =(AppiumBy.ID,"org.commcare.dalvik:id/connect_progress_button")
        # self.start_btn = (AppiumBy.XPATH,"//android.widget.TextView[@text='Start']")
        # self.case_list = (AppiumBy.XPATH, "//android.widget.TextView[@text='Case List']")
        # self.reg_form = (AppiumBy.XPATH, "//android.widget.TextView[@text='Registration Form']")
        # self.text_input = (AppiumBy.XPATH, "//android.widget.EditText")
        # self.number_input = (AppiumBy.XPATH, "//android.widget.EditText")
        #
        # self.finish_btn = (AppiumBy.XPATH, "//android.widget.TextView[@text='FINISH']")
        # self.back_btn = (AppiumBy.XPATH, "//android.widget.ImageButton[@content-desc='Navigate up']")
        # self.sync_btn = (AppiumBy.XPATH, "//android.widget.TextView[@text='Sync with Server']")
        self.log_out = "//android.widget.TextView[@text='Log out of CommCare']"
        # self.warning = (AppiumBy.ID, "org.commcare.dalvik:id/connect_progress_delivery_warning_text")

    def tearDown(self) -> None:
        if self.driver:
            self.driver.quit()

    def click_xpath(self, locator):
        element = self.driver.find_element(AppiumBy.XPATH, locator)
        element.click()

    def click_id(self, locator):
        element = self.driver.find_element(AppiumBy.ID, locator)
        element.click()

    def send_text_xpath(self, locator, user_input):
        element = self.driver.find_element(AppiumBy.XPATH, locator)
        element.send_keys(user_input)

    def send_text_id(self, locator, user_input):
        element = self.driver.find_element(AppiumBy.ID, locator)
        element.send_keys(user_input)

    def click(self, locator):
        time.sleep(2)
        clickable = ec.visibility_of_element_located(locator)
        element = WebDriverWait(self.driver, 30, poll_frequency=1).until(clickable,
                                                                         message="Couldn't find locator: " + str(
                                                                             locator
                                                                             )
                                                                         )
        element.click()

    def send_text(self, locator, value):
        time.sleep(2)
        clickable = ec.visibility_of_element_located(locator)
        element = WebDriverWait(self.driver, 30, poll_frequency=1).until(clickable,
                                                                         message="Couldn't find locator: " + str(
                                                                             locator
                                                                             )
                                                                         )
        element.send_keys(value)

    # def send_text_xpath(self, locator, user_input):
    #     element = self.driver.find_element(AppiumBy.XPATH, locator)
    #     element.send_keys(user_input)
    #
    # def send_text_id(self, locator, user_input):
    #     element = self.driver.find_element(AppiumBy.ID, locator)
    #     element.send_keys(user_input)

    def wait_for_element(self, locator, timeout=20):
        clickable = ec.element_to_be_clickable(locator)
        WebDriverWait(self.driver, timeout, poll_frequency=5).until(clickable,
                                                                    message="Couldn't find locator: " + str(locator)
                                                                    )

    def is_enabled(self, locator):
        try:
            element = self.driver.find_element(*locator)
            is_enabled = element.is_enabled()
        except TimeoutException:
            is_enabled = False
        return bool(is_enabled)
    #
    # def is_displayed(self, locator):
    #     try:
    #         element = self.driver.find_element(*locator)
    #         is_displayed = element.is_displayed()
    #     except (TimeoutException, NoSuchElementException):
    #         is_displayed = False
    #     return bool(is_displayed)

    # def is_present(self, locator):
    #     try:
    #         element = self.driver.find_element(*locator)
    #         is_displayed = True
    #     except NoSuchElementException:
    #         is_displayed = False
    #     return bool(is_displayed)

    def test_form_submission(self) -> None:
        # time.sleep(10)
        # self.driver.find_element(AppiumBy.XPATH, self.enter_code).click()
        # time.sleep(10)
        # self.driver.find_element(AppiumBy.ID, self.profile_code).send_keys('4gjhlPe')
        # time.sleep(5)
        # self.driver.find_element(AppiumBy.ID, self.start_install).click()
        # time.sleep(3)
        # self.driver.find_element(AppiumBy.XPATH, self.install).click()
        time.sleep(25)
        self.driver.find_element(AppiumBy.ID, self.username).send_keys('kdd')
        self.driver.find_element(AppiumBy.ID, self.password).send_keys('123')
        self.driver.find_element(AppiumBy.ID, self.login).click()
        time.sleep(30)
        self.driver.find_element(AppiumBy.XPATH, self.start_button).click()
        time.sleep(10)
        self.driver.find_element(AppiumBy.XPATH, self.case_list).click()
        time.sleep(10)
        self.driver.find_element(AppiumBy.XPATH, self.form).click()
        time.sleep(10)
        self.driver.find_element(AppiumBy.XPATH, self.text_field).send_keys(random_string)
        print(random_string)
        self.driver.find_element(AppiumBy.ID, self.next_btn).click()
        time.sleep(3)
        self.driver.find_element(AppiumBy.XPATH, self.radio_btn_field).click()
        time.sleep(3)
        self.driver.find_element(AppiumBy.ID, self.next_btn).click()
        time.sleep(3)
        self.driver.find_element(AppiumBy.XPATH, self.text_field).send_keys('23')
        self.driver.find_element(AppiumBy.XPATH, self.submit_button).click()
        time.sleep(2)
        # assert self.driver.find_element(AppiumBy.XPATH, "//android.widget.TextView[@text='1 form sent to server!']"
        #                                 ).is_displayed()
        self.driver.find_element(AppiumBy.XPATH, self.sync_button).click()
        time.sleep(120)
        self.driver.find_element(AppiumBy.XPATH, self.log_out).click()


if __name__ == '__main__':
    unittest.main()
