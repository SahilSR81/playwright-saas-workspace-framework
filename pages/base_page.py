from playwright.sync_api import expect
from utils.logger import logger
class BasePage:

    def __init__(self, page):
        self.page = page
        logger.info("BasePage initialized")

    def navigate(self, url):
        logger.info("Navigating to %s", url)
        self.page.goto(url)

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