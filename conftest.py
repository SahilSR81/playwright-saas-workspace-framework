import platform
import sys
from datetime import datetime
from pathlib import Path

import pytest
from playwright.sync_api import sync_playwright

from config.settings import (
    BASE_URL,
    BROWSER,
    ENV,
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
        slow_mo=SLOW_MO,
    )

    yield browser

    logger.info("Closing browser")
    browser.close()


@pytest.fixture
def context(browser):

    logger.info("Creating browser context")

    context = browser.new_context()
    context.tracing.start(screenshots=True, snapshots=True)

    yield context

    logger.info("Closing browser context")
    try:
        if not getattr(context, "_trace_stopped", False):
            context.tracing.stop()
    except Exception:
        pass
    context.close()


@pytest.fixture
def page(context):

    logger.info("Opening new page")

    page = context.new_page()
    page.console_logs = []
    page.on("console", lambda msg: page.console_logs.append(
        f"[{msg.type}] {msg.text}"
    ))

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
    context.tracing.start(screenshots=True, snapshots=True)
    page = context.new_page()
    page.console_logs = []
    page.on("console", lambda msg: page.console_logs.append(
        f"[{msg.type}] {msg.text}"
    ))

    page.goto(DASHBOARD_URL)
    page.wait_for_load_state("networkidle")

    yield page

    logger.info("Closing authenticated session")
    try:
        if not getattr(context, "_trace_stopped", False):
            context.tracing.stop()
    except Exception:
        pass
    context.close()


@pytest.fixture(scope="session", autouse=True)
def set_allure_environment():
    reports_dir = Path("reports/allure-results")
    reports_dir.mkdir(parents=True, exist_ok=True)

    try:
        from importlib.metadata import version as _v
        pw_version = _v("playwright")
    except (ImportError, Exception):
        pw_version = "Unknown"

    props = {
        "OS": f"{platform.system()} {platform.release()}",
        "Python": sys.version.split()[0],
        "Browser": BROWSER.capitalize(),
        "Playwright": pw_version,
        "Framework": "Playwright SaaS Framework",
        "Environment": ENV,
        "Execution.Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    env_file = reports_dir / "environment.properties"
    with open(env_file, "w") as f:
        for key, value in props.items():
            f.write(f"{key} = {value}\n")

    logger.info("Allure environment properties written to %s", env_file)
    yield


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield
    report = outcome.get_result()

    if report.when != "call":
        return

    if report.failed:

        page = item.funcargs.get("page") or item.funcargs.get("authenticated_page")

        if page:

            from utils.allure_helper import (
                attach_console_logs,
                attach_html,
                attach_screenshot,
                attach_trace,
                attach_url,
            )

            logger.error("Test failed. Attaching diagnostics for: %s", item.name)

            attach_screenshot(page, f"Screenshot - {item.name}")
            attach_html(page, f"Page HTML - {item.name}")
            attach_url(page, f"Current URL - {item.name}")

            console_logs = getattr(page, "console_logs", [])
            attach_console_logs(console_logs, f"Console Logs - {item.name}")

            try:
                context = page.context
                trace_dir = Path("traces")
                trace_dir.mkdir(exist_ok=True)
                trace_path = trace_dir / f"{item.name}.zip"
                context.tracing.stop(path=str(trace_path))
                context._trace_stopped = True
                attach_trace(str(trace_path), f"Trace - {item.name}")
            except Exception as e:
                logger.warning("Failed to capture trace: %s", e)
