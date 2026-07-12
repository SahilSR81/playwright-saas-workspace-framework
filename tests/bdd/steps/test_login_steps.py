from pytest_bdd import given, when, then, scenario

from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

scenario = scenario("login.feature", "Valid login")


@given("the user is on the login page")
def navigate_to_login(page):
    login_page = LoginPage(page)
    login_page.navigate()


@when("the user logs in with valid credentials")
def perform_login(page):
    login_page = LoginPage(page)
    login_page.login()


@then("the dashboard should be displayed")
def verify_dashboard(page):
    dashboard_page = DashboardPage(page)
    assert dashboard_page.is_dashboard_loaded()
