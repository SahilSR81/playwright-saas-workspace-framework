import pytest

from config.settings import USERNAME, PASSWORD
from pages.login_page import LoginPage


@pytest.mark.smoke
def test_login_page_load(page):

    login = LoginPage(page)

    login.navigate()

    login.expect_visible(login.username_input)
    login.expect_visible(login.password_input)
    login.expect_visible(login.login_button)


@pytest.mark.smoke
def test_successful_login(page):

    login = LoginPage(page)

    login.navigate()

    login.login()

    assert "dashboard" in page.url.lower()


@pytest.mark.regression
def test_dashboard_heading_visible_after_login(page):

    login = LoginPage(page)

    login.navigate()

    login.login()

    heading = page.get_by_role("heading", name="Dashboard")
    heading.wait_for(state="visible", timeout=30000)

    assert heading.is_visible()


@pytest.mark.regression
def test_invalid_password(page):

    login = LoginPage(page)

    login.navigate()

    login.login(USERNAME, "WrongPassword123")

    assert "Invalid credentials" in login.get_invalid_credentials_text()


@pytest.mark.regression
def test_invalid_username(page):

    login = LoginPage(page)

    login.navigate()

    login.login("WrongUser", PASSWORD)

    assert "Invalid credentials" in login.get_invalid_credentials_text()


@pytest.mark.regression
def test_empty_username(page):

    login = LoginPage(page)

    login.navigate()

    login.login("", PASSWORD)

    assert login.required_field_count() >= 1


@pytest.mark.regression
def test_empty_password(page):

    login = LoginPage(page)

    login.navigate()

    login.login(USERNAME, "")

    assert login.required_field_count() >= 1


@pytest.mark.regression
def test_empty_credentials(page):

    login = LoginPage(page)

    login.navigate()

    login.login("", "")

    assert login.required_field_count() == 2


@pytest.mark.regression
def test_whitespace_credentials(page):

    login = LoginPage(page)

    login.navigate()

    login.login("   ", "   ")

    assert login.required_field_count() >= 1


@pytest.mark.regression
def test_username_case_sensitivity(page):

    login = LoginPage(page)

    login.navigate()

    login.login("admin", PASSWORD)

    assert "dashboard" in page.url.lower()