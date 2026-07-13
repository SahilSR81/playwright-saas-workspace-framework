from uuid import uuid4

from playwright.sync_api import expect

from config.settings import BASE_URL
from pages.base_page import BasePage
from utils.logger import logger


PIM_URL = BASE_URL.replace("/auth/login", "/pim/viewEmployeeList")


class PimPage(BasePage):

    def __init__(self, page):
        super().__init__(page)

        self.page_heading = page.get_by_role("heading", name="PIM")
        self.employee_list_heading = page.get_by_role(
            "heading", name="Employee Information"
        )

        # --- Add Employee form ---
        self.add_button = page.get_by_role("button", name="Add")

        self.first_name_input = page.locator("input[name='firstName']")
        self.middle_name_input = page.locator("input[name='middleName']")
        self.last_name_input = page.locator("input[name='lastName']")

        self.employee_id_input = page.locator(
            "//label[text()='Employee Id']/following::input[1]"
        )

        self.file_input = page.locator("input[type='file']")

        self.save_button = page.get_by_role("button", name="Save").first

        self.personal_details_heading = page.get_by_role(
            "heading", name="Personal Details"
        )

        self.required_messages = page.locator(
            "//span[contains(@class,'oxd-input-field-error-message')]"
        )

        # --- Employee List / Search ---
        self.search_name_input = page.locator(
            "//label[text()='Employee Name']/following::input[1]"
        )

        self.search_id_input = page.locator(
            "//label[text()='Employee Id']/following::input[1]"
        )

        self.search_button = page.get_by_role("button", name="Search")
        self.reset_button = page.get_by_role("button", name="Reset")

        self.table = page.locator(".oxd-table")
        self.table_rows = page.locator(".oxd-table-body .oxd-table-row")

        self.no_records_message = page.get_by_text("No Records Found")

        self.row_checkboxes = page.locator(
            ".oxd-table-body .oxd-checkbox-wrapper"
        )

        self.delete_selected_button = page.get_by_role(
            "button", name="Delete Selected"
        )

        self.confirm_delete_button = page.get_by_role(
            "button", name="Yes, Delete"
        )

        self.success_toast = page.locator(".oxd-toast-content")

    # ---------- Helpers ----------

    def _expand_search_filter(self):
        toggle = self.page.locator(".oxd-icon-button").first
        form = self.page.locator(".oxd-form").first
        if not form.is_visible():
            toggle.click()
            form.wait_for(state="visible", timeout=5000)

    # ---------- Navigation ----------

    def navigate(self):
        logger.info("Navigating to PIM > Employee List page")
        super().navigate(PIM_URL)
        self.wait_for_page_load()

    def is_pim_page_loaded(self):
        logger.info("Checking PIM page heading")

        expect(self.page_heading).to_be_visible()

        return True

    # ---------- Add Employee ----------

    def click_add_employee(self):
        logger.info("Clicking Add Employee button")
        self.click(self.add_button)
        self.wait_for_page_load()

    def fill_add_employee_form(self, first_name, last_name, middle_name=""):
        logger.info(
            "Filling Add Employee form: first='%s' middle='%s' last='%s'",
            first_name, middle_name, last_name,
        )

        self.fill(self.first_name_input, first_name)

        if middle_name:
            self.fill(self.middle_name_input, middle_name)

        self.fill(self.last_name_input, last_name)

    def set_unique_employee_id(self):
        unique_id = str(uuid4().int)[:8]
        logger.info("Setting unique Employee Id: %s", unique_id)
        self.employee_id_input.fill("")
        self.fill(self.employee_id_input, unique_id)

    def get_employee_id_value(self):
        logger.info("Reading auto-generated Employee Id")
        return self.employee_id_input.input_value()

    def save_employee(self):
        logger.info("Saving employee record")
        self.click(self.save_button)
        self.wait_for_page_load()

    def is_employee_added(self):
        logger.info("Verifying employee was added (Personal Details page)")

        try:
            self.page.wait_for_url(
                "**/viewPersonalDetails/**", timeout=5000
            )
            expect(self.personal_details_heading).to_be_visible()
            return True
        except Exception:
            return False

    def required_field_count(self):
        logger.info("Counting required field error messages")
        try:
            self.page.wait_for_selector(
                ".oxd-input-field-error-message", state="visible", timeout=3000
            )
            return self.required_messages.count()
        except Exception:
            return 0

    def upload_profile_image(self, file_path):
        logger.info("Uploading profile image: %s", file_path)
        self.file_input.set_input_files(file_path)

    def is_upload_error_shown(self):
        logger.info("Checking for upload error toast")
        return self.success_toast.count() == 0

    # ---------- Employee Search ----------

    def search_by_name(self, name=""):
        logger.info("Searching employee by name: '%s'", name)

        self._expand_search_filter()

        self.fill(self.search_name_input, name)

        self.click(self.search_button)
        self.wait_for_page_load()

    def search_by_employee_id(self, employee_id=""):
        logger.info("Searching employee by id: '%s'", employee_id)

        self._expand_search_filter()

        self.fill(self.search_id_input, employee_id)
        self.click(self.search_button)
        self.wait_for_page_load()

    def reset_search(self):
        logger.info("Resetting employee search filters")

        self._expand_search_filter()

        self.click(self.reset_button)
        self.wait_for_page_load()

    def get_results_count(self):
        logger.info("Counting employee search results")
        return self.table_rows.count()

    def is_table_loaded(self):
        logger.info("Checking employee table")

        expect(self.table).to_be_visible()

        return True

    def is_no_record_found(self):
        logger.info("Checking 'No Records Found' message")
        try:
            self.no_records_message.wait_for(state="visible", timeout=5000)
            return True
        except Exception:
            return False

    # ---------- Edit Employee ----------

    def open_employee_by_row(self, row_index=0):
        logger.info("Opening employee at row index %s", row_index)

        self.table_rows.nth(row_index).click()

        self.wait_for_page_load()

    def edit_first_name(self, new_first_name):
        logger.info("Editing first name to: %s", new_first_name)

        self.first_name_input.fill("")
        self.fill(self.first_name_input, new_first_name)

    def save_edit(self):
        logger.info("Saving edited employee details")
        self.click(self.save_button)
        self.wait_for_page_load()

    def get_first_name_value(self):
        logger.info("Reading current first name value")
        return self.first_name_input.input_value()

    # ---------- Delete Employee ----------

    def select_row_checkbox(self, row_index=0):
        logger.info("Selecting checkbox for row index %s", row_index)
        self.row_checkboxes.nth(row_index).click()

    def click_delete_selected(self):
        logger.info("Clicking Delete Selected button")
        self.click(self.delete_selected_button)

    def is_delete_confirmation_visible(self):
        logger.info("Checking delete confirmation dialog visibility")

        expect(self.confirm_delete_button).to_be_visible()

        return True

    def confirm_delete(self):
        logger.info("Confirming employee deletion")

        self.click(self.confirm_delete_button)

        self.wait_for_page_load()
