import os

import pytest

from pages.pim_page import PimPage


SAMPLE_IMAGE_PATH = os.path.join("data", "sample_profile.jpg")
SAMPLE_INVALID_FILE_PATH = os.path.join("data", "sample_invalid.txt")


# ---------- Happy Path: Add Employee ----------

@pytest.mark.smoke
def test_navigate_to_pim(authenticated_page):

    pim = PimPage(authenticated_page)

    pim.navigate()

    assert pim.is_pim_page_loaded()


@pytest.mark.smoke
def test_add_employee_button_visible(authenticated_page):

    pim = PimPage(authenticated_page)

    pim.navigate()

    pim.expect_visible(pim.add_button)


@pytest.mark.smoke
def test_add_employee_success(authenticated_page):

    pim = PimPage(authenticated_page)

    pim.navigate()
    pim.click_add_employee()

    pim.fill_add_employee_form(first_name="Sahil", last_name="Singh")
    pim.set_unique_employee_id()
    pim.save_employee()

    assert pim.is_employee_added()


@pytest.mark.regression
def test_add_employee_with_middle_name(authenticated_page):

    pim = PimPage(authenticated_page)

    pim.navigate()
    pim.click_add_employee()

    pim.fill_add_employee_form(
        first_name="Rahul", middle_name="Kumar", last_name="Verma"
    )
    pim.set_unique_employee_id()
    pim.save_employee()

    assert pim.is_employee_added()


@pytest.mark.regression
def test_employee_id_auto_generated(authenticated_page):

    pim = PimPage(authenticated_page)

    pim.navigate()
    pim.click_add_employee()

    employee_id = pim.get_employee_id_value()

    assert employee_id != ""


# ---------- Employee Search ----------

@pytest.mark.regression
def test_search_employee_by_name(authenticated_page):

    pim = PimPage(authenticated_page)

    pim.navigate()
    pim.search_by_name("Sahil")

    assert pim.get_results_count() >= 1


@pytest.mark.regression
def test_search_employee_by_id(authenticated_page):

    pim = PimPage(authenticated_page)

    pim.navigate()
    pim.search_by_employee_id("0001")

    assert pim.is_table_loaded()


@pytest.mark.regression
def test_search_no_results(authenticated_page):

    pim = PimPage(authenticated_page)

    pim.navigate()
    pim.search_by_employee_id("99999999")

    assert pim.is_no_record_found()


@pytest.mark.regression
def test_reset_search_filters(authenticated_page):

    pim = PimPage(authenticated_page)

    pim.navigate()
    pim.search_by_employee_id("99999999")

    assert pim.is_no_record_found()

    pim.reset_search()

    assert pim.get_results_count() >= 1


# ---------- Edit Employee ----------

@pytest.mark.regression
def test_edit_employee_first_name(authenticated_page):

    pim = PimPage(authenticated_page)

    pim.navigate()
    pim.search_by_employee_id("0558")
    pim.open_employee_by_row(0)

    pim.edit_first_name("Edited")
    pim.save_edit()

    assert pim.get_first_name_value() == "Edited"

    pim.edit_first_name("Sahil")
    pim.save_edit()


@pytest.mark.regression
def test_edit_employee_save_persists(authenticated_page):

    pim = PimPage(authenticated_page)

    pim.navigate()
    pim.search_by_employee_id("0558")
    pim.open_employee_by_row(0)

    pim.edit_first_name("PersistCheck")
    pim.save_edit()

    authenticated_page.reload()
    pim.wait_for_page_load()

    assert pim.get_first_name_value() == "PersistCheck"

    pim.edit_first_name("Sahil")
    pim.save_edit()


# ---------- Delete Employee ----------

@pytest.mark.regression
def test_delete_employee_confirmation_dialog(authenticated_page):

    pim = PimPage(authenticated_page)

    pim.navigate()
    pim.select_row_checkbox(0)
    pim.click_delete_selected()

    assert pim.is_delete_confirmation_visible()


@pytest.mark.regression
def test_delete_employee_success(authenticated_page):

    pim = PimPage(authenticated_page)

    pim.navigate()

    before_count = pim.get_results_count()

    pim.select_row_checkbox(0)
    pim.click_delete_selected()
    pim.confirm_delete()

    after_count = pim.get_results_count()

    assert after_count < before_count


# ---------- Upload Profile Image ----------

@pytest.mark.skipif(
    not os.path.exists(SAMPLE_IMAGE_PATH),
    reason="Sample profile image not found in data/ folder",
)
@pytest.mark.integration
def test_upload_profile_image(authenticated_page):

    pim = PimPage(authenticated_page)

    pim.navigate()
    pim.click_add_employee()

    pim.fill_add_employee_form(first_name="Photo", last_name="Test")
    pim.set_unique_employee_id()
    pim.upload_profile_image(SAMPLE_IMAGE_PATH)
    pim.save_employee()

    assert pim.is_employee_added()


@pytest.mark.skipif(
    not os.path.exists(SAMPLE_INVALID_FILE_PATH),
    reason="Sample invalid file not found in data/ folder",
)
@pytest.mark.integration
def test_upload_invalid_file_type(authenticated_page):

    pim = PimPage(authenticated_page)

    pim.navigate()
    pim.click_add_employee()

    pim.fill_add_employee_form(first_name="BadFile", last_name="Test")
    pim.upload_profile_image(SAMPLE_INVALID_FILE_PATH)

    assert pim.is_upload_error_shown()


# ---------- Validation / Negative Scenarios ----------

@pytest.mark.regression
def test_add_employee_empty_required_fields(authenticated_page):

    pim = PimPage(authenticated_page)

    pim.navigate()
    pim.click_add_employee()

    pim.save_employee()

    assert pim.required_field_count() >= 1


@pytest.mark.regression
def test_add_employee_special_characters_in_name(authenticated_page):

    pim = PimPage(authenticated_page)

    pim.navigate()
    pim.click_add_employee()

    pim.fill_add_employee_form(first_name="@#$%^&*", last_name="!!!")
    pim.set_unique_employee_id()
    pim.save_employee()

    assert pim.required_field_count() >= 1 or pim.is_employee_added()


@pytest.mark.regression
def test_search_special_characters(authenticated_page):

    pim = PimPage(authenticated_page)

    pim.navigate()
    pim.search_by_employee_id("@#$%^&*()_admin!")

    assert pim.is_no_record_found() or pim.is_table_loaded()


# ---------- Edge Cases ----------

@pytest.mark.regression
def test_add_employee_long_name(authenticated_page):

    pim = PimPage(authenticated_page)

    pim.navigate()
    pim.click_add_employee()

    long_name = "A" * 100

    pim.fill_add_employee_form(first_name=long_name, last_name="Edge")
    pim.set_unique_employee_id()
    pim.save_employee()

    assert pim.is_employee_added() or pim.required_field_count() >= 1


@pytest.mark.regression
def test_search_leading_trailing_spaces(authenticated_page):

    pim = PimPage(authenticated_page)

    pim.navigate()
    pim.search_by_name("   Sahil   ")

    assert pim.is_table_loaded()
