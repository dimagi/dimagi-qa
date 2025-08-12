import pytest

from Features.CaseSearch.constants import *
from Features.CaseSearch.test_pages.casesearch_page import CaseSearchWorkflows
from QA_Requests.BHAStressTest.test_pages.bha_app_pages import BhaWorkflows
from QA_Requests.BHAStressTest.user_inputs.bha_user_inputs import BhaUserInput
from common_utilities.selenium.webapps import WebApps


def test_case_stress_load_files_2MB_1st(driver, settings):
    """use case: Admit the client - case doesn't exist"""
    app = BhaWorkflows(driver)
    app.create_csv_file(BhaUserInput.csv_file_2MB_1st)
    app.stress_load_files(BhaUserInput.bha_app_name, BhaUserInput.case_list, BhaUserInput.registration_form, BhaUserInput.random_text_2MB, BhaUserInput.csv_file_2MB_1st)

def test_case_stress_load_files_2MB_2nd(driver, settings):
    """use case: Admit the client - case doesn't exist"""
    app = BhaWorkflows(driver)
    app.create_csv_file(BhaUserInput.csv_file_2MB_2nd)
    app.stress_load_files(BhaUserInput.bha_app_name, BhaUserInput.case_list, BhaUserInput.registration_form, BhaUserInput.random_text_2MB, BhaUserInput.csv_file_2MB_2nd)

def test_case_stress_load_files_2MB_2rd(driver, settings):
    """use case: Admit the client - case doesn't exist"""
    app = BhaWorkflows(driver)
    app.create_csv_file(BhaUserInput.csv_file_2MB_3rd)
    app.stress_load_files(BhaUserInput.bha_app_name, BhaUserInput.case_list, BhaUserInput.registration_form, BhaUserInput.random_text_2MB, BhaUserInput.csv_file_2MB_3rd)