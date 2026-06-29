from playwright.sync_api import expect

from config.settings import BASE_URL, TIMEOUT
from pages.base_page import BasePage
from utils.logger import logger


ADMIN_URL = BASE_URL.replace("/auth/login", "/admin/viewSystemUsers")


class AdminPage(BasePage):

    def __init__(self, page):
        super().__init__(page)

        self.page_heading = page.locator(".oxd-topbar-header-title")

        self.username_input = page.locator(
            ".oxd-form-row .oxd-grid-item:nth-child(1) input.oxd-input"
        )

        self.employee_name_input = page.locator(
            ".oxd-form-row .oxd-grid-item:nth-child(3) input.oxd-input"
        )

        self.user_role_dropdown = page.locator(
            ".oxd-form-row .oxd-grid-item:nth-child(2) .oxd-select-text"
        )

        self.status_dropdown = page.locator(
            ".oxd-form-row .oxd-grid-item:nth-child(4) .oxd-select-text"
        )

        self.search_button = page.locator("button[type='submit']")
        self.reset_button = page.locator("button[type='button'].oxd-button--ghost")
        self.add_button = page.locator("button:has(i.bi-plus)")

        self.table_header = page.locator(".oxd-table-header")
        self.table_body = page.locator(".oxd-table-body")
        self.table_rows = page.locator(".oxd-table-body .oxd-table-card")

        self.no_records_message = page.locator(
            ".orangehrm-paper-container > div:nth-child(2) span.oxd-text--span",
            has_text="No Records Found",
        )

    def navigate(self):
        logger.info("Navigating to Admin > System Users page")
        super().navigate(ADMIN_URL)
        self.wait_for_page_load()

    def is_admin_page_loaded(self):
        logger.info("Checking System Users page heading")

        expect(self.page_heading).to_be_visible()

        return True

    def wait_for_search_results(self):
        logger.info("Waiting for search results to settle")
        self.page.wait_for_load_state("networkidle", timeout=TIMEOUT)
        self.page.wait_for_function(
            "() => {"
            "  const body = document.querySelector('.oxd-table-body');"
            "  if (!body) return false;"
            "  if (body.querySelector('.oxd-table-card')) return true;"
            "  const noRecords = document.querySelector('div.orangehrm-paper-container > div:nth-child(2) span.oxd-text--span');"
            "  return noRecords && noRecords.textContent.trim() === 'No Records Found';"
            "}",
            timeout=TIMEOUT,
        )

    def search_user(self, username=""):
        logger.info("Searching user: '%s'", username)

        self.fill(self.username_input, username)
        self.click(self.search_button)

        self.wait_for_search_results()

    def reset(self):
        logger.info("Resetting search filters")

        self.click(self.reset_button)

        self.wait_for_search_results()

    def click_add(self):
        logger.info("Clicking Add button")
        self.click(self.add_button)

    def is_add_button_visible(self):
        logger.info("Checking Add button visibility")

        expect(self.add_button).to_be_visible()

        return True

    def get_results(self):
        logger.info("Fetching search result rows")
        return self.table_rows.all_inner_texts()

    def get_results_count(self):
        logger.info("Counting search result rows")
        return self.table_rows.count()

    def is_table_loaded(self):
        logger.info("Checking System Users table header")

        expect(self.table_header).to_be_visible()

        return True

    def is_no_record_found(self):
        logger.info("Checking 'No Records Found' message")
        return self.no_records_message.count() > 0 and self.no_records_message.first.is_visible()

    def get_username_value(self):
        logger.info("Reading current Username filter value")
        return self.username_input.input_value()

    def select_role(self, role_name):
        logger.info("Selecting User Role filter: %s", role_name)

        self.click(self.user_role_dropdown)

        option = self.page.locator(
            ".oxd-select-dropdown span", has_text=role_name
        ).first

        self.expect_visible(option)
        self.click(option)

    def select_status(self, status_name):
        logger.info("Selecting Status filter: %s", status_name)

        self.click(self.status_dropdown)

        option = self.page.locator(
            ".oxd-select-dropdown span", has_text=status_name
        ).first

        self.expect_visible(option)
        self.click(option)