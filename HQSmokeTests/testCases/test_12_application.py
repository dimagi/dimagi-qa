from HQSmokeTests.testPages.applicationPage import ApplicationPage


def test_TC_34_create_new_app(driver):

    load = ApplicationPage(driver)
    load.create_new_application()


def test_TC_35_form_builder_explore(driver):

    load = ApplicationPage(driver)
    load.form_builder_exploration()


def test_TC_36_form_xml_download_upload(driver):

    load = ApplicationPage(driver)
    load.form_xml_download_upload()


def test_TC_38_settings_exploration(driver):

    load = ApplicationPage(driver)
    load.app_settings_exploration()


def test_delete_app(driver):

    load = ApplicationPage(driver)
    load.delete_application()
