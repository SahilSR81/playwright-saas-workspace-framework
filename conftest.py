from pathlib import Path

import pytest
from playwright.sync_api import sync_playwright

from config.settings import (
    BASE_URL,
    BROWSER,
    HEADLESS,
    SLOW_MO,
)
from pages.login_page import LoginPage
from utils.logger import logger


AUTH_FILE = Path("playwright/.auth/user.json")
DASHBOARD_URL = BASE_URL.replace("/auth/login", "/dashboard/index")


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


@pytest.fixture(scope="session")
def auth_storage_state(browser):
    """
    Session-scoped fixture to perform login once and save the storage state.
    All tests requiring authentication will reuse this state.
    """
    logger.info("Setting up authenticated session storage state")
    AUTH_FILE.parent.mkdir(parents=True, exist_ok=True)

    context = browser.new_context()
    page = context.new_page()

    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login()

    context.storage_state(path=str(AUTH_FILE))
    logger.info("Saved storage state to %s", AUTH_FILE)

    context.close()
    yield AUTH_FILE


@pytest.fixture
def authenticated_page(browser, auth_storage_state):

    logger.info("Launching authenticated browser context using cached storage state")

    context = browser.new_context(storage_state=str(auth_storage_state))
    page = context.new_page()

    page.goto(DASHBOARD_URL)
    page.wait_for_load_state("networkidle")

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