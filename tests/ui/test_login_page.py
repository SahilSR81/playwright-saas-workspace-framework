from pages.login_page import LoginPage
from utils.config_reader import BASE_URL


def test_login_page_navigation(page):

    login_page = LoginPage(page)

    login_page.navigate()

    assert BASE_URL in page.url


def test_login_page_title_is_not_empty(page):

    login_page = LoginPage(page)

    login_page.navigate()

    assert login_page.get_page_title() != ""


def test_login_page_title_contains_openproject(page):

    login_page = LoginPage(page)

    login_page.navigate()

    assert "OpenProject" in login_page.get_page_title()

def test_login_page_url_contains_openproject(page):

    login_page = LoginPage(page)

    login_page.navigate()

    assert "openproject" in login_page.get_current_url().lower()