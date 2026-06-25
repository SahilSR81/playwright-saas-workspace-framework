from pages.base_page import BasePage
from config.settings import BASE_URL


def test_base_page_navigation(page):

    base_page = BasePage(page)

    base_page.navigate(BASE_URL)

    assert BASE_URL.split("/")[2] in base_page.get_url()


def test_base_page_title(page):

    base_page = BasePage(page)

    base_page.navigate(BASE_URL)

    assert len(base_page.get_title()) > 0