import pytest
from utils.logger import logger
from playwright.sync_api import sync_playwright


@pytest.fixture
def page():
    with sync_playwright() as p:
        logger.info("Launching browser")

        browser = p.chromium.launch(headless=False)

        page = browser.new_page()

        yield page
        logger.info("Closing browser")

        browser.close()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:

        page = item.funcargs.get("page")

        if page:
            page.screenshot(
                path=f"screenshots/{item.name}.png"
            )