from pathlib import Path

import pytest
from playwright.sync_api import sync_playwright

from config.settings import (
    BROWSER,
    HEADLESS,
    SLOW_MO,
)
from utils.logger import logger


AUTH_FILE = Path("playwright/.auth/user.json")


@pytest.fixture(scope="session")
def playwright_instance():
    logger.info("Starting Playwright")
    with sync_playwright() as playwright:
        yield playwright
    logger.info("Stopping Playwright")


@pytest.fixture(scope="session")
def browser(playwright_instance):

    logger.info("Launching %s browser", BROWSER)

    browser_launcher = getattr(playwright_instance, BROWSER)

    browser = browser_launcher.launch(
        headless=HEADLESS,
        slow_mo=SLOW_MO
    )

    yield browser

    logger.info("Closing browser")
    browser.close()


@pytest.fixture
def context(browser):

    logger.info("Creating browser context")

    context = browser.new_context()

    yield context

    logger.info("Closing browser context")
    context.close()


@pytest.fixture
def page(context):

    logger.info("Opening new page")

    page = context.new_page()

    yield page

    logger.info("Closing page")
    page.close()


@pytest.fixture
def authenticated_page(browser):

    if not AUTH_FILE.exists():
        pytest.fail(
            "Authentication state not found. Generate storage_state first."
        )

    logger.info("Launching authenticated browser context")

    context = browser.new_context(
        storage_state=str(AUTH_FILE)
    )

    page = context.new_page()

    yield page

    logger.info("Closing authenticated session")

    context.close()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield
    report = outcome.get_result()

    if report.when != "call":
        return

    if report.failed:

        page = item.funcargs.get("page") or item.funcargs.get("authenticated_page")

        if page:

            Path("screenshots").mkdir(exist_ok=True)

            screenshot_path = (
                Path("screenshots") / f"{item.name}.png"
            )

            logger.error(
                "Test failed. Capturing screenshot: %s",
                screenshot_path
            )

            page.screenshot(path=str(screenshot_path), full_page=True)