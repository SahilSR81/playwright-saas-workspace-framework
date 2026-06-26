from pages.login_page import LoginPage


def test_login_page_load(page):

    login = LoginPage(page)

    login.navigate()

    login.expect_visible(login.username_input)
    login.expect_visible(login.password_input)
    login.expect_visible(login.login_button)


def test_successful_login(page):

    login = LoginPage(page)

    login.navigate()

    login.login()

    assert "dashboard" in page.url.lower()


def test_dashboard_heading_visible_after_login(page):

    login = LoginPage(page)

    login.navigate()

    login.login()

    heading = page.get_by_role("heading", name="Dashboard")

    assert heading.is_visible()