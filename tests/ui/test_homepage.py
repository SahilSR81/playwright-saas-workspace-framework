from pages.home_page import HomePage


def test_homepage_title(page):

    home_page = HomePage(page)

    home_page.navigate()

    assert "Playwright" in home_page.get_title()