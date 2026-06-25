from config.settings import BASE_URL
from utils.logger import logger

class LoginPage:

    def __init__(self, page):
        self.page = page

    def navigate(self):
        logger.info("Navigating to login page")
        self.page.goto(BASE_URL)

    def get_page_title(self):
        logger.info("Getting page title")
        return self.page.title()

    def get_current_url(self):
        logger.info("Getting current URL")
        return self.page.url