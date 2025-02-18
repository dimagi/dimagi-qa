import time

import pytest

from HQSmokeTests.testPages.home.home_page import HomePage
from HQSmokeTests.testPages.reports.report_page import ReportPage
from USH_Apps.CO_BHA.test_pages.bha_app_pages import BhaWorkflows
from datetime import datetime

from USH_Apps.CO_BHA.user_inputs.bha_user_inputs import BhaUserInput
from common_utilities.selenium.base_page import BasePage


@pytest.mark.skip(reason="Test case fails due to conditional alert delay")
def test_messaging_history_triggers(driver, settings):
    """use case: Check if conditional alerts have been triggred for all workflows"""
    report = HomePage(driver, settings)
    load = ReportPage(driver)
    app = BhaWorkflows(driver)
    base = BasePage(driver)

    now = (datetime.today()).date()
    report.reports_menu()
    time.sleep(60)
    load.messaging_history_report()

    app.view_message_details(alert_type=BhaUserInput.clinic_admission_request)
    driver.close()
    base.switch_back_to_prev_tab()
    try:
        app.check_if_alert_triggered(content=BhaUserInput.clinic_admission_request_content,
                                     date=str(now.strftime("%-m/%-d/%Y")))  # For Linux
    except (AssertionError, ValueError):
        app.check_if_alert_triggered(content=BhaUserInput.clinic_admission_request_content,
                                     date=str(now.strftime("%#m/%#d/%Y")))  # For Windows

    load.messaging_history_report()
    app.view_message_details(alert_type=BhaUserInput.clinic_same_admit_discahrge)
    driver.close()
    base.switch_back_to_prev_tab()
    app.check_if_alert_triggered(content=BhaUserInput.clinic_same_admit_discahrge_content,
                                 date=str(now.strftime("%Y-%m-%d")))
    load.messaging_history_report()
    app.view_message_details(alert_type=BhaUserInput.clinic_update_lock_status)
    driver.close()
    base.switch_back_to_prev_tab()
    try:
        app.check_if_alert_triggered(content=BhaUserInput.clinic_update_lock_status_content,
                                     date=str(now.strftime("%-m/%-d/%Y")))  # For Linux
    except (AssertionError, ValueError):
        app.check_if_alert_triggered(content=BhaUserInput.clinic_update_lock_status_content,
                                     date=str(now.strftime("%#m/%#d/%Y")))  # For Windows

    load.messaging_history_report()
    app.view_message_details(alert_type=BhaUserInput.state_determination_lock_status)
    driver.close()
    base.switch_back_to_prev_tab()
    try:
        app.check_if_alert_triggered(content=BhaUserInput.state_determination_lock_status_content,
                                     date=str(now.strftime("%-m/%-d/%Y")))  # For Linux
    except (AssertionError, ValueError):
        app.check_if_alert_triggered(content=BhaUserInput.state_determination_lock_status_content,
                                     date=str(now.strftime("%#m/%#d/%Y")))  # For Windows
