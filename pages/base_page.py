from utils.logger import logger
class BasePage:

    def __init__(self, page):
        self.page = page

    def get_title(self):
        logger.info("Getting page title")
        return self.page.title()

    def get_url(self):
        logger.info("Getting current URL")
        return self.page.url

    def navigate(self, url):
        logger.info("Navigating to URL")
        self.page.goto(url)