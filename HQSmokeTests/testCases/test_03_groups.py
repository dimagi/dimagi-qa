from HQSmokeTests.testPages.groupPage import GroupPage
from HQSmokeTests.testPages.homePage import HomePage


def test_TC_04_create_group_and_assign_user(driver):

    menu = HomePage(driver)
    visible = GroupPage(driver)
    menu.users_menu()
    visible.add_group()
    visible.add_user_to_group()


def test_TC_04_edit_user_groups(driver):

    edit = GroupPage(driver)
    edit.edit_existing_group()
    edit.remove_user_from_group()
