from common_utilities.path_settings import PathSettings
from common_utilities.selenium.base_page import BasePage


import os
from percy import percy_snapshot

class VisualTestPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.prod_screens_path = os.path.abspath(PathSettings.ROOT + '/' + 'prod_screens')
        self.staging_screens_path = os.path.abspath(PathSettings.ROOT + '/' + 'staging_screens')

    def take_screenshots(self, name):
        """
        Takes a Percy visual snapshot AND saves a local screenshot, tagged by environment.
        """
        url = self.get_current_url()
        path = None

        if 'www' in url:
            tag = "prod"
            path = self.prod_screens_path
        elif 'staging' in url:
            tag = "staging"
            path = self.staging_screens_path
        else:
            tag = "unknown"
            path = os.path.abspath(PathSettings.ROOT + '/' + 'unknown_screens')

        # Ensure the local folder exists
        os.makedirs(path, exist_ok=True)

        # Local screenshot path
        local_file_path = os.path.join(path, f"{name}.png")

        # Save local screenshot
        self.driver.save_screenshot(local_file_path)
        print(f"[Local] Screenshot saved at: {local_file_path}")

        # Send Percy snapshot
        snapshot_name = f"{tag}: {name}"
        percy_snapshot(self.driver, name=snapshot_name)
        print(f"[Percy] Snapshot taken: {snapshot_name}")
