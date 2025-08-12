import base64
import os

import cv2
from selenium.webdriver.common.by import By
from visual_comparison.utils import ImageComparisonUtil
from Screenshot import Screenshot

from common_utilities.path_settings import PathSettings
from common_utilities.selenium.base_page import BasePage


class VisualTestPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

        self.prod_screens_path = os.path.abspath(PathSettings.ROOT + '/' + 'prod_screens')
        self.staging_screens_path = os.path.abspath(PathSettings.ROOT + '/' + 'staging_screens')

    def take_screenshots(self, pic_name):
        output_file_path =  None
        url = self.get_current_url()
        screenshot_path = "temp_"+pic_name
        # Save the screenshot of the entire page
        # self.driver.save_screenshot(screenshot_path)
        self.take_full_screenshot(screenshot_path)

        if 'www' in url:
            os.makedirs(self.prod_screens_path, exist_ok=True)
            screenshot_image = cv2.imread(screenshot_path)
            output_file_path = os.path.join(self.prod_screens_path, pic_name)
            cv2.imwrite(output_file_path, screenshot_image)
        elif 'staging' in url:
            os.makedirs(self.staging_screens_path, exist_ok=True)
            screenshot_image = cv2.imread("temp_"+pic_name)
            output_file_path = os.path.join(self.staging_screens_path, pic_name)
            cv2.imwrite(output_file_path, screenshot_image)

        else:
            print("Invalid url")
        print(f"Full page screenshot saved successfully to {output_file_path}")

        # Clean up: Delete the temporary screenshot file
        os.remove(screenshot_path)
        # ob = Screenshot.Screenshot()
        # if 'www' in url:
        # # Saving screenshot
        #     img = ob.full_screenshot(self.driver, save_path=self.prod_screens_path,
        #                          image_name=pic_name
        #                          )
        # elif 'staging' in url:
        #     img = ob.full_screenshot(self.driver, save_path=self.prod_screens_path,
        #                          image_name=pic_name
        #                          )
        # else:
        #     print("Invalid url")

        # print(pic_name, img)
        # full_page = self.driver.find_element(By.TAG_NAME, "body")
        # full_page.screenshot(f"{pic_name}")


    def compare_screeshot(self, pic_name):
        output_file_path = None
        # ob = Screenshot.Screenshot()
        url = self.get_current_url()
        screenshot_path = "new_"+pic_name
        # Save the screenshot of the entire page
        # self.driver.save_screenshot(screenshot_path)
        self.take_full_screenshot(screenshot_path)

        if 'www' in url:
            output_file_path = os.path.join(self.prod_screens_path, pic_name)
        elif 'staging' in url:
            output_file_path = os.path.join(self.staging_screens_path, pic_name)

        else:
            print("Invalid url")

        # if 'www' in url:
        # # Saving screenshot
        #     img = ob.full_screenshot(self.driver, save_path=self.prod_screens_path,
        #                          image_name="new_"+pic_name
        #                          )
        # elif 'staging' in url:
        #     img = ob.full_screenshot(self.driver, save_path=self.prod_screens_path,
        #                          image_name="new_"+pic_name
        #                          )
        # else:
        #     print("Invalid url")
        # expected_filepath = os.path.abspath(os.path.join(self.prod_screens_path, pic_name))
        # print(expected_filepath)
        # print(type(expected_filepath), type(img))
        # if os.path.exists(expected_filepath):
        #     print("expected file exists")
        # else:
        #     print("expected file doesn't exist")
        # if os.path.exists(img):
        #     print("actual file exists")
        # else:
        #     print("actual file doesn't exist")

        expected_image = ImageComparisonUtil.read_image(output_file_path)
        actual_image = ImageComparisonUtil.read_image(screenshot_path)
        result_destination = "result_"+pic_name

        # Compare the images, print the similarity index and save it as result.png
        similarity_index = ImageComparisonUtil.compare_images(expected_image, actual_image, result_destination)
        print("Similarity Index:", similarity_index)
        # Asserting both images
        match_result = ImageComparisonUtil.check_match(output_file_path, screenshot_path)
        if match_result:
            print("Image matches for: ", pic_name)
            os.remove(result_destination)
            assert True
        else:
            print("Image mismatch for: ", pic_name)
            assert False
        os.remove(screenshot_path)



    def take_full_screenshot(self, pic_name):
        result = self.driver.execute_cdp_cmd("Page.captureScreenshot", {
            "captureBeyondViewport": True,
            "fromSurface": True
            }
                                        )

        # Save the screenshot
        with open(pic_name, "wb") as f:
            f.write(base64.b64decode(result['data']))