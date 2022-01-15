import pytest

from HQSmokeTests.testPages.homePage import HomePage


@pytest.mark.order(1)
def test_reports_menu_visibility(driver):
    visible = HomePage(driver)
    visible.reports_menu()


@pytest.mark.order(2)
def test_dashboard_menu_visibility(driver):
    visible = HomePage(driver)
    visible.dashboard_menu()


@pytest.mark.order(3)
def test_data_menu_visibility(driver):
    visible = HomePage(driver)
    visible.data_menu()


@pytest.mark.order(4)
def test_user_menu_visibility(driver):
    visible = HomePage(driver)
    visible.users_menu()


@pytest.mark.order(5)
def test_application_menu_visibility(driver):
    visible = HomePage(driver)
    visible.applications_menu()


@pytest.mark.order(6)
def test_messaging_menu_visibility(driver):
    visible = HomePage(driver)
    visible.messaging_menu()


@pytest.mark.order(7)
def test_web_apps_menu_visibility(driver):
    visible = HomePage(driver)
    visible.web_apps_menu()
