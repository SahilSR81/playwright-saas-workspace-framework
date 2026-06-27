from config.settings import (
    BASE_URL,
    TIMEOUT,
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

        self.invalid_credentials_message = page.locator(".oxd-alert-content-text")
        self.required_messages = page.locator("//span[text()='Required']")

    def navigate(self):
        logger.info("Navigating to OrangeHRM login page")
        super().navigate(BASE_URL)

    def enter_username(self, username=USERNAME):
        logger.info("Entering username: %s", username)
        self.fill(self.username_input, username)

    def enter_password(self, password=PASSWORD):
        logger.info("Entering password")
        self.fill(self.password_input, password)

    def click_login(self):
        logger.info("Clicking Login button")
        self.click(self.login_button)

    def login(self, username=USERNAME, password=PASSWORD):
        logger.info("Starting login workflow")

        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

        try:
            self.page.wait_for_url("**/dashboard/**", timeout=TIMEOUT)
        except Exception:
            if self.required_messages.count() >= 1:
                return
            self.invalid_credentials_message.wait_for(state="visible", timeout=TIMEOUT)

    def get_invalid_credentials_text(self):
        return self.invalid_credentials_message.inner_text()

    def required_field_count(self):
        return self.required_messages.count()