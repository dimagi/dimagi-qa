import pytest

from HQSmokeTests.testPages.data.manage_forms_page import ManageFormsPage
from HQSmokeTests.testPages.home.home_page import HomePage
from USH_Apps.WeeklyBHACleanup.userInputs.user_inputs import UserData

""""Contains test cases related to the Data module"""


@pytest.mark.data
@pytest.mark.manageForms
@pytest.mark.archiveForms
@pytest.mark.admitClient
def test_case_01_archive_forms_admit_client(driver, settings):
    """
        1. Navigate to Data>Manage Forms.
        2. Verify user is able to view data for Normal and Archived forms.
        3. Select one form (ideally a survey else a followup form) and archive it
    """
    home = HomePage(driver, settings)
    home.data_menu()
    manage = ManageFormsPage(driver)
    manage.weekly_archive_forms(UserData.cr_app, UserData.cr_admit_client, UserData.date_range, UserData.sub_time)

@pytest.mark.data
@pytest.mark.manageForms
@pytest.mark.archiveForms
@pytest.mark.updateBedAvailability
def test_case_02_archive_forms_update_bed_avail(driver, settings):
    """
        1. Navigate to Data>Manage Forms.
        2. Verify user is able to view data for Normal and Archived forms.
        3. Select one form (ideally a survey else a followup form) and archive it
    """
    home = HomePage(driver, settings)
    home.data_menu()
    manage = ManageFormsPage(driver)
    manage.weekly_archive_forms(UserData.ccs_app, UserData.ccs_bed_avail, UserData.date_range, UserData.sub_time)


@pytest.mark.data
@pytest.mark.manageForms
@pytest.mark.archiveForms
@pytest.mark.sendReferrals
def test_case_03_archive_forms_send_referrals(driver, settings):
    """
        1. Navigate to Data>Manage Forms.
        2. Verify user is able to view data for Normal and Archived forms.
        3. Select one form (ideally a survey else a followup form) and archive it
    """
    home = HomePage(driver, settings)
    home.data_menu()
    manage = ManageFormsPage(driver)
    manage.weekly_archive_forms(UserData.ccs_app, UserData.ccs_send_refferals, UserData.date_range, UserData.sub_time)
