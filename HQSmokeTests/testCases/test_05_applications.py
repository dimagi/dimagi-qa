from HQSmokeTests.testPages.applications.application_page import ApplicationPage


def test_TC_35_create_new_app(driver):

    load = ApplicationPage(driver)
    load.create_new_application()


def test_TC_36_form_builder_explore(driver):

    load = ApplicationPage(driver)
    load.form_builder_exploration()


def test_TC_37_form_xml_download_upload(driver):

    load = ApplicationPage(driver)
    load.form_xml_download_upload()


def test_TC_39_settings_exploration(driver):

    load = ApplicationPage(driver)
    load.app_settings_exploration()
    load.delete_application()
