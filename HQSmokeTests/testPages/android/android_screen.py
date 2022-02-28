from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from HQSmokeTests.userInputs.user_inputs import UserData
import time


class AndroidScreen:

    def __init__(self, settings):
        self.desired_cap = {
            # Set your access credentials
            "browserstack.user": settings["bs_user"],
            "browserstack.key": settings["bs_key"],

            # Set URL of the application under test
            "app": "bs://f2623680346beb48d2d6f12d5e2f8628f3e2278e",

            # Specify device and os_version for testing
            "device": "Google Pixel 4 XL",
            "os_version": "10.0",

            # Set other BrowserStack capabilities
            "project": "First Python project",
            "build": "Python Android",
            "platformName": "android",
            "name": "first_test",
            "autoGrantPermissions": "true",
            "fullReset": "true"
        }
        # Initialize the remote Webdriver using BrowserStack remote URL
        # and desired capabilities defined above
        self.driver = webdriver.Remote(
            command_executor="http://hub-cloud.browserstack.com/wd/hub",
            desired_capabilities=self.desired_cap
        )

        # Locator
        self.enter_code = "//android.widget.TextView[@text='Enter Code']"
        self.profile_code = "org.commcare.dalvik:id/edit_profile_location"
        self.start_install =  "org.commcare.dalvik:id/start_install"
        self.install = "//android.widget.TextView[@text='Start Install']"
        self.username =  "org.commcare.dalvik:id/edit_username"
        self.password = "org.commcare.dalvik:id/edit_password"
        self.login =  "org.commcare.dalvik:id/login_button"
        self.start_button = "//android.widget.TextView[@text='Start']"
        self.case_list = "//android.widget.TextView[@text='"+UserData.case_list_name+"']"
        self.form =  "//android.widget.TextView[@text='"+UserData.new_form_name+"']"
        self.text_field = "//android.widget.EditText"
        self.submit_button = "//android.widget.TextView[@text='FINISH']"


    def click_xpath(self, locator):
        element = self.driver.find_element_by_xpath(locator)
        element.click()

    def click_id(self, locator):
        element = self.driver.find_element_by_id(locator)
        element.click()

    def send_text_xpath(self, locator, user_input):
        element = self.driver.find_element_by_xpath(locator)
        element.send_keys(user_input)

    def send_text_id(self, locator, user_input):
        element = self.driver.find_element_by_id(locator)
        element.send_keys(user_input)

    def install_app_and_submit_form(self, code, random_text):
        self.driver.find_element_by_xpath(self.enter_code).click()
        self.driver.find_element_by_id(self.profile_code).send_keys(code)
        self.driver.find_element_by_id(self.start_install).click()
        time.sleep(2)
        self.driver.find_element_by_xpath(self.install).click()
        time.sleep(15)
        self.driver.find_element_by_id(self.username).send_keys(UserData.app_login)
        self.driver.find_element_by_id(self.password).send_keys(UserData.app_password)
        self.driver.find_element_by_id(self.login).click()
        time.sleep(15)
        self.driver.find_element_by_xpath(self.start_button).click()
        time.sleep(2)
        self.driver.find_element_by_xpath(self.case_list).click()
        time.sleep(2)
        self.driver.find_element_by_xpath(self.form).click()
        time.sleep(2)
        assert self.driver.find_element_by_xpath("//android.widget.TextView[@text='Add Text "+random_text+"']").is_displayed()
        self.driver.find_element_by_xpath(self.text_field).send_keys(random_text)
        self.driver.find_element_by_xpath(self.submit_button).click()
        time.sleep(5)
        assert self.driver.find_element_by_xpath( "//android.widget.TextView[@text='1 form sent to server!']").is_displayed()

    def close_android_driver(self):
        self.driver.quit()