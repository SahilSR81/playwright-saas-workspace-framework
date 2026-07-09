import pytest

from pages.logout_page import LogoutPage


@pytest.mark.smoke
def test_logout_option_visible(authenticated_page):

    logout = LogoutPage(authenticated_page)

    logout.open_user_menu()

    assert logout.is_logout_option_visible()


@pytest.mark.smoke
def test_successful_logout(authenticated_page):

    logout = LogoutPage(authenticated_page)

    logout.logout()

    assert logout.is_login_page_displayed()


@pytest.mark.regression
def test_logout_redirects_to_login(authenticated_page):

    logout = LogoutPage(authenticated_page)

    logout.logout()

    assert "login" in authenticated_page.url.lower()


@pytest.mark.regression
def test_dashboard_not_accessible_after_logout(authenticated_page):

    logout = LogoutPage(authenticated_page)

    logout.logout()

    authenticated_page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/dashboard/index")
    authenticated_page.wait_for_load_state("networkidle")

    assert logout.is_login_page_displayed()


@pytest.mark.regression
def test_refresh_after_logout(authenticated_page):

    logout = LogoutPage(authenticated_page)

    logout.logout()

    authenticated_page.reload()

    assert "login" in authenticated_page.url.lower()