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
    """
        1. Navigate to Data>Import Cases from Excel.
        2. Verify you are able to Import Cases successfully from the excel sheet.
        (A quick way to do this is to download a previously successful upload and change one property)
    """
    home = HomePage(driver, settings)
    home.data_menu()
    imp = ImportCasesPage(driver)
    imp.replace_property_and_upload()


@pytest.mark.data
@pytest.mark.reassignCases
def test_case_30_reassign_cases(driver, settings):
    """
        1. Navigate to the Reassign Cases routine
        2. Run the routine and identify a case
        3. Reassign this case to a new parent
        (This routine may take a few minutes to run)
    """
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
    """
        1. Navigate to Data>Manage Forms.
        2. Verify user is able to view data for Normal and Archived forms.
        3. Select one form (ideally a survey else a followup form) and archive it
    """
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
    """
        1. Navigate to Data>Automatically Update Cases and delete any existing test rules.
        2. Click on "Add Automatic Case Close Rule" button.
        3. Enter Rule name.
        4. Select Case Type.
        5. Define other necessary attribute and save the rule
        6. Verify you are able to create an Automatic Case Close rule successfully.
        7. After the test, delete the rule.
    """
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
    """
        1. Navigate to Data>Manage Tables
        2. Click on "Add Table" button.
        3. Enter desired table ID and fields.
        4. Click Save.
        5. Verify user is able to create a lookup table.
    """
    home = HomePage(driver, settings)
    home.data_menu()
    data = LookUpTablePage(driver)
    data.create_lookup_table()


@pytest.mark.data
@pytest.mark.lookupTable
@pytest.mark.viewTables
def test_case_34_view_lookup_table(driver, settings):
    """
        1. Select View Tables
        2. Choose a table from the dropdown
        3. Ensure you're able to view its contents
    """
    home = HomePage(driver, settings)
    home.data_menu()
    data = LookUpTablePage(driver)
    data.view_lookup_table()
    data.delete_lookup_table()


@pytest.mark.data
@pytest.mark.deduplicateCases
def test_case_58_deduplicate_cases(driver, settings):
    """
        1. Navigate to Data > Deduplicate Cases
        2. Click on "+ Add Deduplicate Rule" button
        3. Enter name for the dedupe rule in the Name field
        4. Select the Case Type and enter the Case Property value
        5. Click on Save button.
        6. Verify user gets a Successfully create a dedupe rule message at the top
        7. Delete the dedup rule
    """
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
    """
        1. Navigate to Data > Data Dictionary
        2. Click on 'Export to Excel' button
        3. Verify an excel file starts downloading
        4. Click on Import from Excel button
        5. Upload the file you just downloaded in step 3
        6 Click on Upload Data Dictionary button
        7. Verify Data Dictionary import successful message appears at the top
    """
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
    """
        1. Navigate to the Copy Cases routine
        2. Run the routine and identify a case
        3. Copy this case to a new user
        4. Verify that a copy of the case is created for the selected user.
    """
    home = HomePage(driver, settings)
    home.data_menu()
    copy = CopyCasesPage(driver, settings)
    copy.get_cases()
    copy.copy_case()
