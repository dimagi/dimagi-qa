from common_utilities.path_settings import PathSettings
from common_utilities.selenium.base_page import BasePage


import os
from percy import percy_screenshot

class VisualTestPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.screens_path = os.path.abspath(PathSettings.ROOT + '/' + 'screenshots')

    def take_screenshots(self, tag, name):
        """
        Takes a Percy visual snapshot AND saves a local screenshot, tagged by environment.
        """
        path = self.screens_path

        # Ensure the local folder exists
        os.makedirs(path, exist_ok=True)

        # Local screenshot path
        local_file_path = os.path.join(path, f"{name}.png")

        # Save local screenshot
        self.driver.save_screenshot(local_file_path)
        print(f"[Local] Screenshot saved at: {local_file_path}")

        # Send Percy snapshot
        snapshot_name = f"{tag}: {name}"
        # self.driver.save_screenshot(snapshot_name)
        percy_screenshot(self.driver, name=snapshot_name)
        print(f"[Percy] Snapshot taken: {snapshot_name}")

