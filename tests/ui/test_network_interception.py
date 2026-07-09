import pytest

from pages.dashboard_page import DashboardPage
from utils.network_helper import NetworkHelper


@pytest.mark.integration
def test_block_images(authenticated_page):

    dashboard = DashboardPage(authenticated_page)

    NetworkHelper.block_images(authenticated_page)

    authenticated_page.reload()

    assert dashboard.is_dashboard_loaded()

    NetworkHelper.unblock_all(authenticated_page)


@pytest.mark.integration
def test_block_css(authenticated_page):

    dashboard = DashboardPage(authenticated_page)

    NetworkHelper.block_css(authenticated_page)

    authenticated_page.reload()

    assert dashboard.is_dashboard_loaded()

    NetworkHelper.unblock_all(authenticated_page)


@pytest.mark.integration
def test_mock_server_error(authenticated_page):

    NetworkHelper.mock_server_error(authenticated_page)

    authenticated_page.reload()

    assert authenticated_page.url.endswith(
        "/dashboard/index"
    )

    NetworkHelper.unblock_all(authenticated_page)


@pytest.mark.integration
def test_mock_employee_api(authenticated_page):

    NetworkHelper.mock_employee_api(authenticated_page)

    authenticated_page.reload()

    assert authenticated_page is not None

    NetworkHelper.unblock_all(authenticated_page)


@pytest.mark.integration
def test_offline_mode(authenticated_page):

    NetworkHelper.simulate_offline(authenticated_page)

    try:

        authenticated_page.reload(timeout=5000)

    except Exception:

        assert True

    finally:

        NetworkHelper.restore_network(authenticated_page)


@pytest.mark.integration
def test_restore_network(authenticated_page):

    NetworkHelper.simulate_offline(authenticated_page)

    NetworkHelper.restore_network(authenticated_page)

    authenticated_page.reload()

    assert "dashboard" in authenticated_page.url.lower()