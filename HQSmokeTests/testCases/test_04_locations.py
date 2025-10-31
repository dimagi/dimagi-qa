import pytest

from HQSmokeTests.testPages.home.home_page import HomePage
from HQSmokeTests.testPages.users.org_structure_page import OrganisationStructurePage

""""Contains test cases related to the User's Locations module"""


@pytest.mark.user
@pytest.mark.organisationStructure
def test_case_07_create_location(driver, settings):
    """
        1. Navigate to Users>Organization Structure.
        2. Create a new location.
        3. Verify user is able to create a new location.
    """
    menu = HomePage(driver, settings)
    menu.users_menu()
    create = OrganisationStructurePage(driver)
    create.organisation_menu_open()
    print("Opened Organisation StructurePage Page")
    create.create_location()
    print("Location created")



@pytest.mark.user
@pytest.mark.organisationStructure
def test_case_07_edit_existing_location(driver, settings):
    """
        1. Navigate to Users>Organization Structure.
        2. Verify user is also able to edit any existing location in the project space.
    """
    menu = HomePage(driver, settings)
    menu.users_menu()
    edit = OrganisationStructurePage(driver)
    edit.edit_location()
    print("Location edited")


@pytest.mark.user
@pytest.mark.organisationStructure
def test_case_56_archive_unarchive_location(driver, settings):
    """
        1. Navigate to Users > Organization Structure
        2. Click on 'Archive' button for any existing location.
        3. A warning pop up appears, click on Archive button.
        4. Verify a success message appears that the location is archived.
        5. Click on 'Show Archived Locations' button
        6. Verify that the location you archived step 2 is present.
        7. Click on Unarchive button for that location.
        8. Click on 'Show Active Location' button and verify that the location is again Active.
    """
    menu = HomePage(driver, settings)
    menu.users_menu()
    location = OrganisationStructurePage(driver)
    location.archive_location()
    print("Location successfully Archived")
    location.unarchive_location(settings)
    print("Location successfully Unarchived")



@pytest.mark.user
@pytest.mark.organisationStructure
def test_case_08_edit_location_fields(driver, settings, rerun_count):
    """
        1. Remaining on the Organization Structure, click 'Edit Location Fields'
        2. Add a new Location Field
        3. Access a newly added location and add a value to the newly created Location Field
    """
    menu = HomePage(driver, settings)
    menu.users_menu()
    edit = OrganisationStructurePage(driver)
    loc_field_name = edit.edit_location_fields(rerun_count)
    print("Location field created")
    edit.selection_location_field_for_location_created(loc_field_name)
    print("Selected location field created, for the location")


@pytest.mark.user
@pytest.mark.organisationLevel
def test_case_09_creation_organization_level(driver, settings):
    """
        1. Access the Organization Levels page
        2. Add a new Organization Level
    """
    menu = HomePage(driver, settings)
    menu.users_menu()
    org = OrganisationStructurePage(driver)
    org.create_org_level()


@pytest.mark.user
@pytest.mark.organisationLevel
@pytest.mark.organisationImport
@pytest.mark.organisationExport
def test_case_11_download_and_upload_locations(driver, settings):
    """
        1. Navigate to Users section.
        2. Go to Organization Structure
        3. User should be able to download each of these as excel sheet
        4. Make note of the download names, they are to be uploaded next
        5. Return to the Organization Structure page
        6. Without editing the downloaded locations file, select Bulk Upload
        7. Import the file and ensure there are no errors
    """
    menu = HomePage(driver, settings)
    menu.users_menu()
    org = OrganisationStructurePage(driver)
    org.download_locations()
    org.upload_locations()


@pytest.mark.user
@pytest.mark.organisationStructure
def test_cleanup_items_in_locations_menu(driver, settings):
    """
        1. Go to Organisation Structure Page
        2. Delete all test locations
    """
    menu = HomePage(driver, settings)
    menu.users_menu()
    clean4 = OrganisationStructurePage(driver)
    clean4.cleanup_location()
    print("Deleted the location and location field")
