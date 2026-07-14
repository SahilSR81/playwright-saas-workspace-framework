import time

from playwright.sync_api import expect
from playwright._impl._errors import TimeoutError as PlaywrightTimeout

from config.settings import TIMEOUT
from utils.logger import logger


class BasePage:

    def __init__(self, page):
        self.page = page
        logger.info("BasePage initialized")

    def navigate(self, url, attempts=3, backoff_seconds=2):
        for attempt in range(1, attempts + 1):
            try:
                logger.info("Navigating to %s (attempt %d/%d)", url, attempt, attempts)
                self.page.goto(url, wait_until="domcontentloaded", timeout=TIMEOUT)
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

    def get_title(self):
        logger.info("Getting page title")
        return self.page.title()

    def get_current_url(self):
        logger.info("Getting current URL")
        return self.page.url

    def wait_for_page_load(self):
        logger.info("Waiting for page to load")
        self.page.wait_for_load_state("networkidle")

    def click(self, locator):
        logger.info("Clicking on locator")
        locator.click()

    def fill(self, locator, text):
        logger.info("Filling locator with text")
        locator.fill(text)

    def expect_visible(self, locator):
        logger.info("Expecting locator to be visible")
        expect(locator).to_be_visible()