import pytest

from HQSmokeTests.testPages.applications.app_preview import AppPreviewPage
from HQSmokeTests.testPages.applications.application_page import ApplicationPage
from HQSmokeTests.testPages.home.home_page import HomePage
from Features.Lookuptable.testPages.data.lookup_table_page import LookUpTablePage
from Features.Lookuptable.userInputs.user_inputs import UserData

"""Contains test cases related to lookup table reference in the app builder"""


@pytest.mark.lookup
@pytest.mark.inapp
def test_case_34_Lookup_table_formbuilder_6(driver, settings):
    data = LookUpTablePage(driver)
    home = HomePage(driver, settings)
    home.applications_menu(UserData.application)
    data.test_application()
    data.delete_caselist()


@pytest.mark.lookup
@pytest.mark.inapp
def test_case_30_lookup_table_form_builder1(driver, settings):
    data = LookUpTablePage(driver)
    home = HomePage(driver, settings)
    home.applications_menu(UserData.application)
    data.create_new_form()
    data.lookuptable_display_list()
    data.delete_caselist()


@pytest.mark.lookup
@pytest.mark.inapp
def test_case_29_lookup_table_form_builder1(driver, settings):  # Hover and click error.
    data = LookUpTablePage(driver)
    home = HomePage(driver, settings)
    home.applications_menu(UserData.application)
    data.create_new_form()
    data.adding_questions()


@pytest.mark.lookup
@pytest.mark.inapp
def test_case_31_lookup_table_form_builder3(driver, settings):
    data = LookUpTablePage(driver)
    home = HomePage(driver, settings)
    home.data_menu()
    data.upload_2(UserData.state, "1")
    home.applications_menu(UserData.application)
    data.specific_table_upload(UserData.specific_table_data[0])
    home.data_menu()
    data.delete_lookup_table(UserData.specific_table_data[0])
    home = HomePage(driver, settings)
    home.applications_menu(UserData.application)
    data.navigation_to_a_caselist(UserData.caselist_nav)
    data.delete_caselist()

@pytest.mark.lookup
@pytest.mark.inapp
def test_case_32_lookup_table_form_builder4(driver, settings):
    data = LookUpTablePage(driver)
    home = HomePage(driver, settings)
    home.data_menu()
    data.upload_2(UserData.state, "1")
    home.applications_menu(UserData.application)
    data.specific_table_upload(UserData.specific_table_data[0])
    data.formbuilder_4()
    data.delete_caselist()

@pytest.mark.lookup
@pytest.mark.inapp
def test_case_33_lookup_table_form_builder5(driver, settings):
    data = LookUpTablePage(driver)
    home = HomePage(driver, settings)
    home.data_menu()
    data.upload_2(UserData.state, "1")
    home.applications_menu(UserData.application)
    data.specific_table_upload(UserData.specific_table_data[0])
    data.formbuilder_5()
    home.data_menu()
    data.edit_state()
    data.delete_caselist()

@pytest.mark.lookup
@pytest.mark.inapp
def test_case_22_filtered_lookup_table(driver, settings):
    data = LookUpTablePage(driver)
    home = HomePage(driver, settings)
    home.data_menu()
    data.upload_2(UserData.Inapp, "1")
    home.applications_menu(UserData.application)
    data.specific_table_upload(UserData.specific_table_data[1])
    data.formbuilder_5()
    app_preview = AppPreviewPage(driver)
    app_preview.check_access_to_app_preview()
    data.loop_submit_form_on_registration()
    driver.switch_to.default_content()
    data.delete_caselist()

@pytest.mark.lookup
@pytest.mark.inapp
def test_case_35_languages_check(driver, settings):
    data = LookUpTablePage(driver)
    home = HomePage(driver, settings)
    home.data_menu()
    data.upload_2(UserData.state, "1")
    home.applications_menu(UserData.application)
    application = ApplicationPage(driver)
    application.add_language(UserData.languages[0])
    application.add_language(UserData.languages[1])
    data.specific_table_upload(UserData.specific_table_data[0])
    data.language_check()
    data.language_submit_form_on_registration(UserData.languages, UserData.user_ids_list[0], UserData.specific_table_data[0])
    driver.switch_to.default_content()
    data.delete_caselist()
