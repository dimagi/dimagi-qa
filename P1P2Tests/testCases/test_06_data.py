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
@pytest.mark.reassignCases
@pytest.mark.p1p2EscapeDefect
def test_case_30_reassign_cases(driver, settings):
    home = HomePage(driver, settings)
    home.data_menu()
    reassign = ReassignCasesPage(driver, settings)
    reassign.get_cases(settings['login_username'])
    reassign.reassign_case()

@pytest.mark.data
@pytest.mark.copyCases
@pytest.mark.p1p2EscapeDefect
def test_case_60_copy_cases(driver, settings):
    home = HomePage(driver, settings)
    home.data_menu()
    copy = CopyCasesPage(driver, settings)
    copy.get_cases(settings['login_username'])
    copy.copy_case()
