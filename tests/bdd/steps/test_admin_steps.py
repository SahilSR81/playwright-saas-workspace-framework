from pytest_bdd import given, when, then, scenario

from pages.admin_page import AdminPage
from pages.dashboard_page import DashboardPage

scenario = scenario("admin.feature", "Search existing user")


@given("the user is logged in")
def verify_logged_in(page):
    dashboard_page = DashboardPage(page)
    assert dashboard_page.is_dashboard_loaded()


@when('the user searches for "Admin"')
def search_admin_user(page):
    admin_page = AdminPage(page)
    admin_page.navigate()
    admin_page.search_user("Admin")


@then("search results should be displayed")
def verify_search_results(page):
    admin_page = AdminPage(page)
    assert admin_page.is_table_loaded()
    assert admin_page.get_results_count() > 0
