from playwright.sync_api import expect

from pages.base_page import BasePage
from utils.logger import logger


class DashboardPage(BasePage):

    def __init__(self, page):
        super().__init__(page)

        self.dashboard_heading = page.get_by_role(
            "heading",
            name="Dashboard"
        )

        self.user_dropdown = page.locator(".oxd-userdropdown-name")

        self.logout_option = page.get_by_role(
            "menuitem",
            name="Logout"
        )

        self.side_menu = page.locator(".oxd-sidepanel-body")

        self.quick_launch = page.get_by_text("Quick Launch")

        self.time_at_work = page.get_by_text("Time at Work")

        self.my_actions = page.get_by_text("My Actions")

    def is_dashboard_loaded(self):
        logger.info("Checking Dashboard page")

        expect(self.dashboard_heading).to_be_visible()

        return True

    def is_side_menu_visible(self):
        logger.info("Checking side navigation")

        return self.side_menu.is_visible()

    def is_quick_launch_visible(self):
        return self.quick_launch.is_visible()

    def is_time_at_work_visible(self):
        return self.time_at_work.is_visible()

    def is_my_actions_visible(self):
        return self.my_actions.is_visible()

    def logout(self):

        logger.info("Logging out")

        self.user_dropdown.click()

        self.logout_option.click()