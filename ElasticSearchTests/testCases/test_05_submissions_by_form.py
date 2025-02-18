import pytest


from HQSmokeTests.testPages.email.email_verification import EmailVerification
from HQSmokeTests.testPages.home.home_page import HomePage
from ElasticSearchTests.userInputs.user_inputs import UserData
from ElasticSearchTests.testPages.submissions_by_forms.submissions_by_form_page import SubmissionsByFormPage

""""Contains all test cases that aren't specifically related any menu modules"""


@pytest.mark.login
@pytest.mark.reports
def test_case_01_sub_by_form_report_fields_filters_columns(driver, settings):
    report = HomePage(driver, settings)
    report.reports_menu()
    activity = SubmissionsByFormPage(driver)
    activity.verify_sub_by_form_page_fields()
    activity.hide_filters()
    activity.show_filters()
    activity.verify_table_columns()
    activity.verify_users_in_the_group()



@pytest.mark.login
@pytest.mark.reports
def test_case_02_pagination(driver, settings):
    report = HomePage(driver, settings)
    report.reports_menu()
    activity = SubmissionsByFormPage(driver)
    activity.sub_by_form_pagination_list()
    activity.verify_pagination_dropdown()
    activity.verify_sorted_list()


@pytest.mark.login
@pytest.mark.reports
def test_case_03_save_report_and_favorite(driver, settings):
    report = HomePage(driver, settings)
    report.reports_menu()
    activity = SubmissionsByFormPage(driver)
    activity.sub_by_form_save_report()

@pytest.mark.login
@pytest.mark.reports
def test_case_04_export_to_excel(driver, settings):
    home = HomePage(driver, settings)
    home.reports_menu()
    activity = SubmissionsByFormPage(driver)
    web_data = activity.export_sub_by_form_to_excel()
    activity.compare_sbf_with_email(web_data)

@pytest.mark.login
@pytest.mark.reports
def test_case_05_email_report(driver, settings):
    home = HomePage(driver, settings)
    home.reports_menu()
    activity = SubmissionsByFormPage(driver)
    web_data, subject = activity.export_sub_by_form_email()
    email = EmailVerification(settings)
    table_data = email.get_email_body_from_latest_email(subject, settings['url'])
    activity.compare_sbf_with_html_table(table_data, web_data)

@pytest.mark.login
@pytest.mark.reports
def test_case_06_user_type_filter_by(driver, settings):
    home = HomePage(driver, settings)
    home.reports_menu()
    activity = SubmissionsByFormPage(driver)
    activity.sub_by_form_users_active()
    activity.sub_by_form_users_deactivated()
    activity.filter_dates_and_verify(UserData.filter_dates_by[0])
    # activity.filter_dates_and_verify(UserData.filter_dates_by[1])

def test_case_07_advanced_options(driver, settings):
    home = HomePage(driver, settings)
    home.reports_menu()
    activity = SubmissionsByFormPage(driver)
    activity.advanced_options()
    activity.form_column_verification(UserData.reassign_cases_application,
                                          list(UserData.reasign_modules_forms.keys())[1],
                                          UserData.reasign_modules_forms[
                                              list(UserData.reasign_modules_forms.keys())[1]][0])
    activity.form_column_verification(UserData.reassign_cases_application)
    activity.form_column_verification(UserData.reassign_cases_application,
                                      list(UserData.reasign_modules_forms.keys())[1])
    activity.form_column_verification(UserData.reassign_cases_application,
                                      list(UserData.reasign_modules_forms.keys())[0])

