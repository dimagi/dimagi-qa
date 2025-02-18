import pytest

from HQSmokeTests.testPages.data.copy_cases_page import CopyCasesPage
from HQSmokeTests.testPages.data.data_dictionary_page import DataDictionaryPage
from HQSmokeTests.testPages.data.deduplicate_case_page import DeduplicateCasePage
from HQSmokeTests.testPages.data.manage_forms_page import ManageFormsPage
from HQSmokeTests.testPages.data.import_cases_page import ImportCasesPage
from HQSmokeTests.testPages.data.reassign_cases_page import ReassignCasesPage
from HQSmokeTests.testPages.data.auto_case_update_page import AutoCaseUpdatePage
from HQSmokeTests.testPages.data.lookup_table_page import LookUpTablePage
from HQSmokeTests.testPages.home.home_page import HomePage

""""Contains test cases related to the Data module"""


@pytest.mark.data
@pytest.mark.importCases
def test_case_29_import_cases(driver, settings):
    home = HomePage(driver, settings)
    home.data_menu()
    imp = ImportCasesPage(driver)
    imp.replace_property_and_upload()


@pytest.mark.data
@pytest.mark.reassignCases
def test_case_30_reassign_cases(driver, settings):
    home = HomePage(driver, settings)
    home.data_menu()
    reassign = ReassignCasesPage(driver, settings)
    reassign.get_cases(settings['login_username'])
    reassign.reassign_case()


@pytest.mark.data
@pytest.mark.manageForms
@pytest.mark.archiveForms
@pytest.mark.restoreForms
def test_case_31_manage_forms(driver, settings):
    home = HomePage(driver, settings)
    home.data_menu()
    manage = ManageFormsPage(driver)
    manage.get_normal_forms(settings['url'])
    manage.view_normal_form()
    manage.archive_forms()
    manage.get_archived_forms()
    manage.view_archived_forms()
    manage.restore_forms()


@pytest.mark.data
@pytest.mark.automaticallyUpdateCase
def test_case_32_auto_case_update(driver, settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = AutoCaseUpdatePage(driver)
    data.delete_test_rules()
    data.open_auto_case_update_page()
    data.add_new_rule()
    data.remove_rule()


@pytest.mark.data
@pytest.mark.lookupTable
@pytest.mark.manageTables
def test_case_33_create_lookup_table(driver, settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = LookUpTablePage(driver)
    data.create_lookup_table()


@pytest.mark.data
@pytest.mark.lookupTable
@pytest.mark.viewTables
def test_case_34_view_lookup_table(driver, settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = LookUpTablePage(driver)
    data.view_lookup_table()
    data.delete_lookup_table()


@pytest.mark.data
@pytest.mark.deduplicateCases
def test_case_58_deduplicate_cases(driver, settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = DeduplicateCasePage(driver)
    data.open_deduplicate_case_page()
    data.add_new_rule()
    data.remove_rule()


@pytest.mark.data
@pytest.mark.dataDictionary
@pytest.mark.downloadDataDictionary
@pytest.mark.uploadDataDictionary
def test_case_59_data_dictionary(driver, settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = DataDictionaryPage(driver)
    data.open_data_dictionary_case_page()
    data.export_data_dictionary()
    data.import_data_dictionary()


@pytest.mark.data
@pytest.mark.copyCases
@pytest.mark.skip
def test_case_60_copy_cases(driver, settings):
    home = HomePage(driver, settings)
    home.data_menu()
    copy = CopyCasesPage(driver, settings)
    copy.get_cases()
    copy.copy_case()
