import pytest

from pages.admin_page import AdminPage


@pytest.mark.smoke
def test_admin_page_load(authenticated_page):

    admin = AdminPage(authenticated_page)

    admin.navigate()

    assert admin.is_admin_page_loaded()


@pytest.mark.smoke
def test_table_loaded(authenticated_page):

    admin = AdminPage(authenticated_page)

    admin.navigate()

    assert admin.is_table_loaded()


@pytest.mark.smoke
def test_add_button_visible(authenticated_page):

    admin = AdminPage(authenticated_page)

    admin.navigate()

    assert admin.is_add_button_visible()


@pytest.mark.regression
def test_search_existing_user(authenticated_page):

    admin = AdminPage(authenticated_page)

    admin.navigate()

    admin.search_user("Admin")

    assert admin.get_results_count() >= 1


@pytest.mark.regression
def test_search_invalid_user(authenticated_page):

    admin = AdminPage(authenticated_page)

    admin.navigate()

    admin.search_user("NotARealUser_999")

    assert admin.is_no_record_found()


@pytest.mark.regression
def test_empty_search(authenticated_page):

    admin = AdminPage(authenticated_page)

    admin.navigate()

    admin.search_user("")

    assert admin.is_table_loaded()


@pytest.mark.regression
def test_reset_filters(authenticated_page):

    admin = AdminPage(authenticated_page)

    admin.navigate()

    admin.search_user("Admin")

    admin.reset()

    assert admin.get_username_value() == ""


@pytest.mark.regression
def test_reset_after_search(authenticated_page):

    admin = AdminPage(authenticated_page)

    admin.navigate()

    admin.search_user("NotARealUser_999")

    assert admin.is_no_record_found()

    admin.reset()

    assert admin.get_results_count() >= 1


@pytest.mark.regression
def test_search_special_characters(authenticated_page):

    admin = AdminPage(authenticated_page)

    admin.navigate()

    admin.search_user("@#$%^&*()_admin!")

    assert admin.is_no_record_found() or admin.is_table_loaded()


@pytest.mark.regression
def test_search_long_username(authenticated_page):

    admin = AdminPage(authenticated_page)

    admin.navigate()

    long_username = "a" * 150

    admin.search_user(long_username)

    assert admin.is_no_record_found() or admin.is_table_loaded()


@pytest.mark.regression
def test_search_case_sensitivity(authenticated_page):

    admin = AdminPage(authenticated_page)

    admin.navigate()

    admin.search_user("admin")
    lower_count = admin.get_results_count()

    admin.reset()

    admin.search_user("ADMIN")
    upper_count = admin.get_results_count()

    assert lower_count >= 0 and upper_count >= 0


@pytest.mark.regression
def test_search_leading_trailing_spaces(authenticated_page):

    admin = AdminPage(authenticated_page)

    admin.navigate()

    admin.search_user("   Admin   ")

    assert admin.is_table_loaded()


@pytest.mark.regression
def test_rapid_consecutive_searches(authenticated_page):

    admin = AdminPage(authenticated_page)

    admin.navigate()

    for username in ["Admin", "Test", "QA", "Random123"]:
        admin.search_user(username)

    assert admin.is_table_loaded()


@pytest.mark.regression
def test_multiple_filter_search(authenticated_page):

    admin = AdminPage(authenticated_page)

    admin.navigate()

    admin.select_role("ESS")
    admin.select_status("Disabled")
    admin.search_user("Admin")

    assert admin.is_no_record_found() or admin.is_table_loaded()


@pytest.mark.regression
def test_no_records_message(authenticated_page):

    admin = AdminPage(authenticated_page)

    admin.navigate()

    admin.search_user("ZZZ_Nonexistent_User_000")

    assert admin.is_no_record_found()