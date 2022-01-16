from HQSmokeTests.testPages.others.home_page import HomePage


def test_TC_01_menu_visibility(driver):

    visible = HomePage(driver)
    visible.reports_menu()
    visible.dashboard_menu()
    visible.data_menu()
    visible.users_menu()
    visible.applications_menu()
    visible.messaging_menu()
    visible.web_apps_menu()
