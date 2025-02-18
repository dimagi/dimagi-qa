import os
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

connect_id_phn = '+74267611441'
app_path = os.getcwd() + '\\MobileTest\\ccc_bulk_submission\\20240422-app-cccStaging-release.apk'
capabilities = UiAutomator2Options().load_capabilities({
    "platformName": "Android",
    "udid": "emulator-5554",
    "automationName": "UIAutomator2",
    "deviceName": "Pixel_8_Pro_API_new",
    "avd": "Pixel_8_Pro_API_new",
    # "appPackage": "com.google.android.apps.nexuslauncher",
    "appWaitPackage": "org.commcare.dalvik",
    "appWaitActivity": "org.commcare.activities.LoginActivity",
    # "appActivity": "org.commcare.activities.DispatchActivity",
    "autoGrantPermissions": "true",
    "app":app_path,
    "noReset": "true",
    "fullReset": "false",
    "dontStopAppOnReset": "false"
    })

appium_server_url = 'http://localhost:4723/wd/hub'
chars = string.ascii_lowercase + string.digits
random_string = ''.join(random.choices(chars, k=6))
random_number = random.randint(100, 19999)

class TestAppium(unittest.TestCase):
    def setUp(self) -> None:
        self.driver = webdriver.Remote(appium_server_url,
                                       options=capabilities)

        self.go_to_menu = (AppiumBy.ID, "org.commcare.dalvik:id/connect_login_button")
        self.password_field = (AppiumBy.ID, "org.commcare.dalvik:id/connect_password_verify_input")
        self.password_verify_btn = (AppiumBy.ID, "org.commcare.dalvik:id/connect_password_verify_button")
        self.my_jobs = (AppiumBy.ANDROID_UIAUTOMATOR, "new UiSelector().text(\"MY JOBS\")")
        self.payment_verification_job = (AppiumBy.XPATH, "//android.widget.TextView[@text=\"Payment Verifications\"]//following-sibling::android.widget.ImageView[@resource-id=\"org.commcare.dalvik:id/button\"]\n")
        # self.verification_pay_tab =
        self.launch_app =(AppiumBy.ID,"org.commcare.dalvik:id/connect_progress_button")
        self.start_btn = (AppiumBy.XPATH,"//android.widget.TextView[@text='Start']")
        self.case_list = (AppiumBy.XPATH, "//android.widget.TextView[@text='Case List']")
        self.reg_form = (AppiumBy.XPATH, "//android.widget.TextView[@text='Registration Form']")
        self.text_input = (AppiumBy.XPATH, "//android.widget.EditText")
        self.number_input = (AppiumBy.XPATH, "//android.widget.EditText")
        self.next_btn = (AppiumBy.ID, "org.commcare.dalvik:id/nav_btn_next")
        self.finish_btn = (AppiumBy.XPATH, "//android.widget.TextView[@text='FINISH']")
        self.back_btn = (AppiumBy.XPATH, "//android.widget.ImageButton[@content-desc='Navigate up']")
        self.sync_btn = (AppiumBy.XPATH, "//android.widget.TextView[@text='Sync with Server']")
        self.log_out = (AppiumBy.XPATH, "//android.widget.TextView[@text='Log out of CommCare']")
        self.warning = (AppiumBy.ID, "org.commcare.dalvik:id/connect_progress_delivery_warning_text")


    def tearDown(self) -> None:
        if self.driver:
            self.driver.quit()

    def click(self, locator):
        time.sleep(2)
        clickable = ec.visibility_of_element_located(locator)
        element = WebDriverWait(self.driver, 30, poll_frequency=1).until(clickable, message="Couldn't find locator: " + str(locator))
        element.click()

    def send_text(self, locator, value):
        time.sleep(2)
        clickable = ec.visibility_of_element_located(locator)
        element = WebDriverWait(self.driver, 30, poll_frequency=1).until(clickable, message="Couldn't find locator: " + str(locator))
        element.send_keys(value)

    def send_text_xpath(self, locator, user_input):
        element = self.driver.find_element(AppiumBy.XPATH, locator)
        element.send_keys(user_input)

    def send_text_id(self, locator, user_input):
        element = self.driver.find_element(AppiumBy.ID, locator)
        element.send_keys(user_input)

    def wait_for_element(self, locator, timeout=20):
        clickable = ec.element_to_be_clickable(locator)
        WebDriverWait(self.driver, timeout, poll_frequency=5).until(clickable,
                                                                    message="Couldn't find locator: " + str(locator))

    def fetch_random_string(self):
        return random_string

    def fetch_random_digit(self):
        return str(random_number)

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
        except (TimeoutException, NoSuchElementException):
            is_displayed = False
        return bool(is_displayed)

    def is_present(self, locator):
        try:
            element = self.driver.find_element(*locator)
            is_displayed = True
        except NoSuchElementException:
            is_displayed = False
        return bool(is_displayed)

    def test_form_submission(self) -> None:
        time.sleep(10)
        self.wait_for_element(self.go_to_menu, 100)
        self.click(self.go_to_menu)
        self.click(self.password_field)
        self.send_text(self.password_field, "auto@test")
        time.sleep(2)
        self.click(self.password_verify_btn)
        time.sleep(5)
        self.click(self.my_jobs)
        time.sleep(3)
        self.click(self.payment_verification_job)
        time.sleep(3)
        self.wait_for_element(self.launch_app)
        self.click(self.launch_app)
        time.sleep(3)
        for i in range(0, 6):
            self.wait_for_element(self.start_btn, 100)
            print("App successfully launched")
            self.click(self.start_btn)
            self.click(self.case_list)
            self.click(self.reg_form)
            self.send_text(self.text_input, "test_"+str(i)+self.fetch_random_string())
            self.click(self.next_btn)
            self.send_text(self.text_input, self.fetch_random_digit()+str(i))
            self.click(self.next_btn)
            self.wait_for_element(self.finish_btn)
            self.click(self.finish_btn)
            time.sleep(2)
            self.wait_for_element(self.start_btn)
            self.click(self.back_btn)
            self.wait_for_element(self.launch_app)
            if i >= 5:
                assert self.is_present(self.warning), "Alert not present even after limit is crossed"
                print("Alert correctly present after limit is crossed")
            else:
                assert not self.is_present(self.warning),  "Alert present even before limit is crossed"
                print("Alert not present as expected")
            self.click(self.launch_app)
            time.sleep(10)

if __name__ == '__main__':
    unittest.main()

