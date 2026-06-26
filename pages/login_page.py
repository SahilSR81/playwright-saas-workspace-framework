from config.settings import (
    BASE_URL,
    USERNAME,
    PASSWORD,
)

from pages.base_page import BasePage
from utils.logger import logger

class LoginPage(BasePage):

    def __init__(self, page):
        super().__init__(page)

        self.username_input = page.get_by_placeholder("Username")
        self.password_input = page.get_by_placeholder("Password")
        self.login_button = page.get_by_role("button", name="Login")

    def navigate(self):
        super().navigate(BASE_URL)

    def enter_username(self, username=USERNAME):
        logger.info("Entering username: %s", username)
        self.fill(self.username_input, username)

    def enter_password(self, password=PASSWORD):
        logger.info("Entering password")
        self.fill(self.password_input, password)

    def click_login(self):
        logger.info("Clicking login button")
        self.click(self.login_button)

    def login(self):
        logger.info("Initiating login process")
        self.enter_username()
        self.enter_password()
        self.click_login()
        self.wait_for_page_load()