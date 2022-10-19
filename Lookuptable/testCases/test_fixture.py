
import pytest

from HQSmokeTests.testPages.data.data_dictionary_page import DataDictionaryPage
from HQSmokeTests.testPages.data.deduplicate_case_page import DeduplicateCasePage
from HQSmokeTests.testPages.data.export_data_page import ExportDataPage
from common_utilities.Excel.excel_manage import ExcelManager
from HQSmokeTests.testPages.data.manage_forms_page import ManageFormsPage
from HQSmokeTests.testPages.data.import_cases_page import ImportCasesPage
from HQSmokeTests.testPages.data.reassign_cases_page import ReassignCasesPage
from HQSmokeTests.testPages.data.auto_case_update_page import AutoCaseUpdatePage
from HQSmokeTests.testPages.data.lookup_table_page import LookUpTablePage
from common_utilities.generate_random_string import fetch_random_string

""""Contains test cases related to the Data module"""


def test_19_create_lookup_table(driver):
    data = LookUpTablePage(driver)
    export = ExportDataPage(driver)
    export.data_tab()
    data.create_lookup_table()


def test_29_view_lookup_table(driver):
    data = LookUpTablePage(driver)
    export = ExportDataPage(driver)
    export.data_tab()
    data.view_lookup_table()
    data.delete_lookup_table()

def test_01_upload(driver):
    data = LookUpTablePage(driver)
    path = "C:\\Users\\FL_LPT-444\\Desktop\\sam\\Automation\\dimagi-qa-master\\dimagi-qa-master\\HQSmokeTests\\upload_1.xlsx"
    data.upload_1(path)

def test_37_select_deselect(driver):
    data = LookUpTablePage(driver)
    data.selects_deselects()

def test_38_edit_table(driver):
    data = LookUpTablePage(driver)
    data.edit_table()

def test_39_create_dummy_id(driver):
        data = LookUpTablePage(driver)
        data.create_dummyid()

def test_40_edit_dummydata(driver):
        data = LookUpTablePage(driver)
        data.edit_dummy_data()


def test_05_download1(driver):
    export = ExportDataPage(driver)
    export.data_tab()
    data = LookUpTablePage(driver)
    TableId = data.create_lookup_table()
    print("Table name:" + TableId)
    data.download1()
    return TableId

def test_02_Error_upload1(driver):
    Tableid = test_05_download1(driver)
    data = LookUpTablePage(driver)
    excel = ExcelManager(driver)
    Download_path = data.error_upload1()
    print("path is " + Download_path)
    excel.__init__(Download_path)
    col = excel.col_size(Tableid)
    excel.write_excel_data(Tableid,1,col+1,"user 1")
    row = excel.row_size(Tableid)
    data = [(1, 'N', '1' , 'RWS%DTUYIG*&^%'), (2, 'N', '2' , '!#@$%#$RFGH:')]
    excel.write_data(Tableid,data)
    data = LookUpTablePage(driver)
    data.upload_1(Download_path)

def test_03_Error_upload2(driver):
    Tableid = test_05_download1(driver)
    data = LookUpTablePage(driver)
    excel = ExcelManager(driver)
    Download_path = data.error_upload1()
    print("path is " + Download_path)
    excel.__init__(Download_path)
    col = excel.col_size(Tableid)
    excel.write_excel_data(Tableid,1,col+1,"group 1")
    row = excel.row_size(Tableid)
    data = [(1, 'N', '1' , 'dsrebyugu%'), (2, 'N', '2' , '!^*^UGFHJBM')]
    excel.write_data(Tableid,data)
    data = LookUpTablePage(driver)
    data.upload_1(Download_path)

def test_06_download_upload2(driver):
    data = LookUpTablePage(driver)
    file = "C:\\Users\\FL_LPT-444\\Desktop\\sam\\Automation\\dimagi-qa-master\\dimagi-qa-master\\HQSmokeTests\\Hypertension.xlsx"
    data.upload_1(file)

def test_21_Error_upload3(driver):
    Tableid = test_05_download1(driver)
    data = LookUpTablePage(driver)
    excel = ExcelManager(driver)
    Download_path = data.error_upload1()
    print("path is " + Download_path)
    excel.__init__(Download_path)
    ColName = ["user 1", "group 1"]
    for x in ColName:
        for i in range(1,2):
            col = excel.col_size(Tableid)
            excel.write_excel_data(Tableid,1,col+i,x)
            print("Colname is:"+ x)
    for y in range(1,3):
            data = [(1, 'N', '1', str(fetch_random_string()) + 'yugu%', '$RGw%' + str(fetch_random_string())),
            (2, 'N', '2', '!^*^M' + str(fetch_random_string()), '%^*@Whxb' + str(fetch_random_string()))]
            excel.write_data(Tableid, data)
    data = LookUpTablePage(driver)
    data.upload_1(Download_path)



















