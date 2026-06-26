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
    
    logger.info("Getting page title")
    def get_current_url(self):
        return self.page.url

    logger.info("Getting current URL")
    def wait_for_page_load(self):
        self.page.wait_for_load_state("networkidle")

    logger.info("Waiting for page to load")
    def click(self, locator):
        locator.click()

    logger.info("Clicking on locator")
    def fill(self, locator, text):
        locator.fill(text)

    logger.info("Filling locator with text")
    def expect_visible(self, locator):
        expect(locator).to_be_visible()