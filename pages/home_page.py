from utils.logger import logger
class HomePage:

    def __init__(self, page):
        self.page = page

    def navigate(self):
        self.page.goto("https://playwright.dev/")

    def get_title(self):
        logger.info("Getting page title")
        return self.page.title()