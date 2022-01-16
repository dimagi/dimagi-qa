from HQSmokeTests.testPages.others.home_page import HomePage
from HQSmokeTests.testPages.messaging.messaging_page import MessagingPage


def test_TC_42_dashboard(driver):

    menu = HomePage(driver)
    msg = MessagingPage(driver)
    menu.messaging_menu()
    msg.open_dashboard_page()


def test_TC_43_compose_sms(driver):

    menu = HomePage(driver)
    msg = MessagingPage(driver)
    menu.messaging_menu()
    msg.compose_sms()


def test_TC_44_broadcast(driver):

    menu = HomePage(driver)
    msg = MessagingPage(driver)
    menu.messaging_menu()
    msg.send_broadcast_message()


def test_TC_45_create_cond_alert(driver):

    menu = HomePage(driver)
    msg = MessagingPage(driver)
    menu.messaging_menu()
    msg.create_cond_alert()
    msg.remove_cond_alert()


def test_TC_46_cond_alert_bulk_upload(driver):

    menu = HomePage(driver)
    msg = MessagingPage(driver)
    menu.messaging_menu()
    msg.cond_alert_download()
    msg.cond_alert_upload()


def test_TC_47_keyword_creation(driver):

    menu = HomePage(driver)
    msg = MessagingPage(driver)
    menu.messaging_menu()
    msg.add_keyword_trigger()
    msg.remove_keyword()
    msg.add_structured_keyword_trigger()
    msg.remove_structured_keyword()


def test_TC_48_chats(driver):

    menu = HomePage(driver)
    msg = MessagingPage(driver)
    menu.messaging_menu()
    msg.chat_page()


def test_TC_50_general_settings(driver):

    menu = HomePage(driver)
    msg = MessagingPage(driver)
    menu.messaging_menu()
    msg.general_settings_page()


def test_TC_51_languages(driver):

    menu = HomePage(driver)
    msg = MessagingPage(driver)
    menu.messaging_menu()
    msg.languages_page()


def test_TC_52_translations(driver):

    menu = HomePage(driver)
    msg = MessagingPage(driver)
    menu.messaging_menu()
    msg.msg_trans_download()
    msg.msg_trans_upload()


def test_TC_53_settings_pages(driver):

    msg = MessagingPage(driver)
    msg.project_settings_page()
    msg.current_subscription_page()
