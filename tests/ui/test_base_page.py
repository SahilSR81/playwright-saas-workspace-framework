import pytest

from pages.base_page import BasePage
from config.settings import BASE_URL


@pytest.mark.smoke
def test_base_page_navigation(page):

    base = BasePage(page)

    base.navigate(BASE_URL)

    assert "orangehrmlive" in base.get_current_url().lower()


@pytest.mark.smoke
def test_base_page_title(page):

    base = BasePage(page)

    base.navigate(BASE_URL)

    assert "OrangeHRM" in base.get_title()