import pytest

from Features.CaseSearch.constants import *
from Features.CaseSearch.test_pages.casesearch_page import CaseSearchWorkflows
from QA_Requests.BHAStressTest.test_pages.bha_app_pages import BhaWorkflows
from QA_Requests.BHAStressTest.user_inputs.bha_user_inputs import BhaUserInput
from common_utilities.selenium.webapps import WebApps


def test_case_1_stress_load_files_3kb_1st(driver, settings):
    """use case: Admit the client - case doesn't exist"""
    app = BhaWorkflows(driver)
    app.create_csv_file(BhaUserInput.result_name_3kb_1st)
    app.stress_load_files(BhaUserInput.bha_app_name, BhaUserInput.case_list, BhaUserInput.registration_form,
                          BhaUserInput.result_name_3kb_1st, BhaUserInput.input_file_3kb
                          )

def test_case_2_stress_load_files_3kb_2nd(driver, settings):
    """use case: Admit the client - case doesn't exist"""
    app = BhaWorkflows(driver)
    app.create_csv_file(BhaUserInput.result_name_3kb_2nd)
    app.stress_load_files(BhaUserInput.bha_app_name, BhaUserInput.case_list, BhaUserInput.registration_form,
                          BhaUserInput.result_name_3kb_2nd, BhaUserInput.input_file_3kb
                          )

def test_case_2_stress_load_files_3kb_3rd(driver, settings):
    """use case: Admit the client - case doesn't exist"""
    app = BhaWorkflows(driver)
    app.create_csv_file(BhaUserInput.result_name_3kb_3rd)
    app.stress_load_files(BhaUserInput.bha_app_name, BhaUserInput.case_list, BhaUserInput.registration_form,
                          BhaUserInput.result_name_3kb_3rd, BhaUserInput.input_file_3kb
                          )
