from pages.dashboard_page import DashboardPage


def test_dashboard_load(authenticated_page):

    dashboard = DashboardPage(authenticated_page)

    assert dashboard.is_dashboard_loaded()


def test_dashboard_url(authenticated_page):

    assert "dashboard" in authenticated_page.url.lower()


def test_side_navigation_visible(authenticated_page):

    dashboard = DashboardPage(authenticated_page)

    assert dashboard.is_side_menu_visible()


def test_quick_launch_widget(authenticated_page):

    dashboard = DashboardPage(authenticated_page)

    assert dashboard.is_quick_launch_visible()


def test_time_at_work_widget(authenticated_page):

    dashboard = DashboardPage(authenticated_page)

    assert dashboard.is_time_at_work_visible()


def test_my_actions_widget(authenticated_page):

    dashboard = DashboardPage(authenticated_page)

    assert dashboard.is_my_actions_visible()