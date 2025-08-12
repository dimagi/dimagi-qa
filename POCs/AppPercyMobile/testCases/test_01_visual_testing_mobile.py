import pytest

from POCs.AppPercyMobile.testPages.application_page import ApplicationPage
from POCs.AppPercyMobile.testPages.android_screen import AndroidScreen
from POCs.AppPercyMobile.user_inputs.user_inputs import UserInput

""""Contains test cases related to the Application module"""

@pytest.mark.application
@pytest.mark.appBuilder
@pytest.mark.androidTest
@pytest.mark.reportSubmitHistory
@pytest.mark.appReleases
def test_case_1_create_new_build_deploy_to_mobile(driver, settings):
    """
        1. After adding few questions in the form.
        2. Click on the application's name which says 'Updates are available'.
        3. Make a new version of this app.
        4. Verify you are able to publish the version of the app from deploy page.
        5. Deploy this app in mobile.
        6. Login into the app using mobile worker you just created above in the sheet.
        7. Verify you are able to login and access the form successfully
        8. Submit the form and ensure you can find your submissions in the Submit History Report
    """
    tag = None
    if 'www' in settings['url']:
        tag = "prod"
    elif 'staging' in settings['url']:
        tag = "staging"
    else:
        tag = "unknown"
    mobile = AndroidScreen(settings)
    mobile.install_app_and_submit_form(tag, UserInput.install_code)
    mobile.close_android_driver()
