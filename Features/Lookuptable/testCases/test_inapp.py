import time

import pytest

from HQSmokeTests.testPages.applications.app_preview import AppPreviewPage
from HQSmokeTests.testPages.home.home_page import HomePage
from Features.Lookuptable.testPages.data.lookup_table_page import LookUpTablePage
from Features.Lookuptable.userInputs.user_inputs import UserData

"""Contains test cases related to the Data module"""
values = dict()

@pytest.mark.lookup
@pytest.mark.inapp
def test_34_Lookup_table_formbuilder_6(driver):
    data = LookUpTablePage(driver)
    data.test_application()
    data.delete_caselist()

@pytest.mark.lookup
@pytest.mark.inapp
def test_30_lookup_table_form_builder1(driver):
    data = LookUpTablePage(driver)
    data.create_new_form()
    data.lookuptable_display_list()
    data.delete_caselist()

@pytest.mark.lookup
@pytest.mark.inapp
def test_29_lookup_table_form_builder1(driver):  # Hover and click error.
    data = LookUpTablePage(driver)
    data.create_new_form()
    data.adding_questions()


@pytest.mark.lookup
@pytest.mark.inapp
def test_31_lookup_table_form_builder3(driver,settings):
    data = LookUpTablePage(driver)
    home = HomePage(driver, settings)
    home.data_menu()
    data.upload_1(UserData.state, "1")
    data.specific_table_upload("state")
    home.data_menu()
    data.delete_Specificlookup_table("state")
    data.navigation_to_application_tab()
    data.Navigation_to_a_caselist("Lookup table was not found in the project")
    data.delete_caselist()

def test_32_lookup_table_form_builder4(driver,settings):
    data = LookUpTablePage(driver)
    home = HomePage(driver, settings)
    home.data_menu()
    data.upload_1(UserData.state, "1")
    data.specific_table_upload("state")
    data.formbuilder_4()
    data.delete_caselist()

def test_33_lookup_table_form_builder5(driver,settings):
    data = LookUpTablePage(driver)
    home = HomePage(driver, settings)
    home.data_menu()
    data.upload_1(UserData.state, "1")
    data.specific_table_upload("state")
    data.formbuilder_5()
    home.data_menu()
    data.edit_state("state")
    data.delete_caselist()



def test_22_filtered_lookup_table(driver,settings):
    data = LookUpTablePage(driver)
    home = HomePage(driver, settings)
    home.data_menu()
    data.upload_1(UserData.Inapp, "1")
    data.specific_table_upload("Inapp")
    data.formbuilder_5()
    AppPreview = AppPreviewPage(driver)
    AppPreview.check_access_to_app_preview()
    for i in range(len(UserData.user_ids_list)):
        data.submit_form_on_registration("en",UserData.user_ids_list[i])
    driver.switch_to.default_content()
    data.delete_caselist()


def test_35_languages_check(driver,settings):
    data = LookUpTablePage(driver)
    home = HomePage(driver, settings)
    home.data_menu()
    data.upload_1(UserData.state, "1")
    data.specific_table_upload("state")
    data.language_check()
    AppPreview = AppPreviewPage(driver)
    AppPreview.check_access_to_app_preview()
    data.submit_form_on_registration("en","kiran")
    data.submit_form_on_registration("hin","kiran")
    driver.switch_to.default_content()
    data.delete_caselist()













