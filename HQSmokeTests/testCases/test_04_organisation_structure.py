from HQSmokeTests.testPages.homePage import HomePage
from HQSmokeTests.testPages.organisationStructurePage import OrganisationStructurePage


def test_TC_06_create_location(driver):

    menu = HomePage(driver)
    create = OrganisationStructurePage(driver)
    menu.users_menu()
    create.organisation_menu_open()
    print("Opened Organisation StructurePage Page")
    create.create_location()
    print("Location created")


def test_TC_06_edit_existing_location(driver):

    edit = OrganisationStructurePage(driver)
    edit.edit_location()
    print("Location edited")


def test_TC_07_edit_location_fields(driver):

    edit = OrganisationStructurePage(driver)
    edit.edit_location_fields()
    print("Location field created")


def test_TC_07_visibilty_of_location_fields_in_locations(driver):

    edit = OrganisationStructurePage(driver)
    edit.selection_location_field_for_location_created()
    print("Selected location field created, for the location")


def test_TC_08_creation_organization_level(driver):

    org = OrganisationStructurePage(driver)
    org.create_org_level()


def test_TC_10_download_and_upload_locations(driver):

    menu = HomePage(driver)
    menu.users_menu()
    org = OrganisationStructurePage(driver)
    org.download_locations()
    org.upload_locations()


def test_cleanup_location(driver):
    org = OrganisationStructurePage(driver)
    org.cleanup()
