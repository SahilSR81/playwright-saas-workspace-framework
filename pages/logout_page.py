from playwright.sync_api import expect

from pages.base_page import BasePage
from utils.logger import logger


class LogoutPage(BasePage):

    def __init__(self, page):
        super().__init__(page)

        self.profile_dropdown = page.locator(".oxd-userdropdown-name")

        self.logout_option = page.get_by_role(
            "menuitem",
            name="Logout"
        )

        self.login_button = page.get_by_role(
            "button",
            name="Login"
        )

    def open_user_menu(self):
        logger.info("Opening user dropdown")

        self.profile_dropdown.click()

    def is_logout_option_visible(self):
        logger.info("Checking Logout option visibility")

        expect(self.logout_option).to_be_visible()

        return True

    def logout(self):
        logger.info("Logging out")

        self.open_user_menu()

        self.logout_option.click()

        self.wait_for_page_load()

    def is_login_page_displayed(self):
        logger.info("Verifying Login page")

        expect(self.login_button).to_be_visible()

        return True