import os
import platform
import sys
import time
from datetime import datetime
from pathlib import Path

import pytest
from playwright.sync_api import sync_playwright
from playwright._impl._errors import TimeoutError as PlaywrightTimeout

from config.settings import (
    BASE_URL,
    BROWSER,
    BROWSERS,
    ENV,
    HEADLESS,
    PARALLEL_WORKERS,
    SLOW_MO,
    TIMEOUT,
)
from pages.login_page import LoginPage
from utils.logger import logger


AUTH_DIR = Path("playwright/.auth")
DASHBOARD_URL = BASE_URL.replace("/auth/login", "/dashboard/index")


def _get_worker_id():
    worker = os.environ.get("PYTEST_XDIST_WORKER", None)
    if worker:
        return worker
    return "master"


def _get_worker_auth_path(worker_id):
    AUTH_DIR.mkdir(parents=True, exist_ok=True)
    return AUTH_DIR / f"{worker_id}.json"


def _navigate_with_retry(page, url, attempts=3, backoff_seconds=2):
    for attempt in range(1, attempts + 1):
        try:
            logger.info("Navigating to %s (attempt %d/%d)", url, attempt, attempts)
            page.goto(url, wait_until="domcontentloaded", timeout=TIMEOUT)
            return
        except PlaywrightTimeout:
            if attempt == attempts:
                logger.error("Navigation failed after %d attempts: %s", attempts, url)
                raise
            wait = backoff_seconds * attempt
            logger.warning(
                "Navigation timeout on attempt %d/%d, retrying in %ds: %s",
                attempt, attempts, wait, url,
            )
            time.sleep(wait)


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
    context.set_default_navigation_timeout(TIMEOUT)
    context.set_default_timeout(TIMEOUT)
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


def _perform_login(browser, auth_path):
    """Helper: perform a fresh login, save storage state, return (context, page)."""
    context = browser.new_context()
    context.set_default_navigation_timeout(TIMEOUT)
    context.set_default_timeout(TIMEOUT)
    page = context.new_page()

    login_page = LoginPage(page)
    _navigate_with_retry(page, BASE_URL)
    login_page.login()

    context.storage_state(path=str(auth_path))
    logger.info("Saved storage state to %s", auth_path)

    return context, page


def _copy_storage_state(src_path, dst_path):
    """Copy a storage state file so both worker-specific and user.json stay in sync."""
    import shutil
    try:
        shutil.copy2(str(src_path), str(dst_path))
        logger.info("Synced storage state to %s", dst_path)
    except Exception as e:
        logger.warning("Failed to sync storage state: %s", e)


@pytest.fixture(scope="session")
def auth_storage_state(browser):
    """
    Session-scoped fixture that performs login once per worker and saves
    a separate storage state file per xdist worker to avoid conflicts.
    """
    worker_id = _get_worker_id()
    auth_path = _get_worker_auth_path(worker_id)
    user_json_path = AUTH_DIR / "user.json"

    if auth_path.exists():
        logger.info("Removing stale storage state for worker %s", worker_id)
        auth_path.unlink(missing_ok=True)

    logger.info("Setting up authenticated session for worker %s", worker_id)

    context, page = _perform_login(browser, auth_path)
    _copy_storage_state(auth_path, user_json_path)

    context.close()
    yield auth_path


@pytest.fixture
def authenticated_page(browser, auth_storage_state):
    auth_path = auth_storage_state
    user_json_path = AUTH_DIR / "user.json"

    logger.info("Launching authenticated browser context using cached storage state")

    context = browser.new_context(storage_state=str(auth_path))
    context.set_default_navigation_timeout(TIMEOUT)
    context.set_default_timeout(TIMEOUT)
    context.tracing.start(screenshots=True, snapshots=True)
    page = context.new_page()
    page.console_logs = []
    page.on("console", lambda msg: page.console_logs.append(
        f"[{msg.type}] {msg.text}"
    ))

    _navigate_with_retry(page, DASHBOARD_URL)
    page.wait_for_load_state("networkidle")

    if "/auth/login" in page.url.lower():
        logger.warning("Storage state expired — re-authenticating")
        context.close()

        new_context, new_page = _perform_login(browser, auth_path)
        _copy_storage_state(auth_path, user_json_path)
        new_context.close()

        context = browser.new_context(storage_state=str(auth_path))
        context.set_default_navigation_timeout(TIMEOUT)
        context.set_default_timeout(TIMEOUT)
        context.tracing.start(screenshots=True, snapshots=True)
        page = context.new_page()
        page.console_logs = []
        page.on("console", lambda msg: page.console_logs.append(
            f"[{msg.type}] {msg.text}"
        ))
        _navigate_with_retry(page, DASHBOARD_URL)
        page.wait_for_load_state("networkidle")

    yield page

    logger.info("Closing authenticated session")
    try:
        if not getattr(context, "_trace_stopped", False):
            context.tracing.stop()
    except Exception:
        pass
    context.close()


def pytest_configure(config):
    config.addinivalue_line("markers", "smoke: Quick sanity checks for critical paths")
    config.addinivalue_line("markers", "regression: Full regression test suite")
    config.addinivalue_line("markers", "api: API-only tests")
    config.addinivalue_line("markers", "integration: UI + API hybrid tests")


def pytest_collection_modifyitems(config, items):
    if PARALLEL_WORKERS > 0:
        for item in items:
            if "authenticated_page" in item.fixturenames:
                item.add_marker(pytest.mark.serial)


@pytest.fixture(scope="session", autouse=True)
def set_allure_environment():
    reports_dir = Path("reports/allure-results")
    reports_dir.mkdir(parents=True, exist_ok=True)

    try:
        from importlib.metadata import version as _v
        pw_version = _v("playwright")
    except (ImportError, Exception):
        pw_version = "Unknown"

    worker_id = _get_worker_id()

    props = {
        "OS": f"{platform.system()} {platform.release()}",
        "Python": sys.version.split()[0],
        "Browser": BROWSER.capitalize(),
        "Playwright": pw_version,
        "Framework": "Playwright SaaS Framework",
        "Environment": ENV,
        "Worker": worker_id,
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
