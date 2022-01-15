from HQSmokeTests.testPages.homePage import HomePage


def test_TC_01_reports_menu_visibility(driver):

    visible = HomePage(driver)
    visible.reports_menu()


def test_TC_01_dashboard_menu_visibility(driver):

    visible = HomePage(driver)
    visible.dashboard_menu()


def test_TC_01_data_menu_visibility(driver):

    visible = HomePage(driver)
    visible.data_menu()


def test_TC_01_user_menu_visibility(driver):

    visible = HomePage(driver)
    visible.users_menu()


def test_TC_01_application_menu_visibility(driver):

    visible = HomePage(driver)
    visible.applications_menu()


def test_TC_01_messaging_menu_visibility(driver):

    visible = HomePage(driver)
    visible.messaging_menu()


def test_TC_01_web_apps_menu_visibility(driver):

    visible = HomePage(driver)
    visible.web_apps_menu()
