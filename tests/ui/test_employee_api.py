import pytest

from api.employee_api import EmployeeAPI


@pytest.fixture
def employee_api(auth_storage_state):

    api = EmployeeAPI()

    yield api

    api.close()


def test_employee_endpoint():

    api = EmployeeAPI()

    assert api.EMPLOYEE_ENDPOINT == "/web/index.php/api/v2/pim/employees"


def test_create_employee_payload(employee_api):

    payload = {
        "firstName": "Sahil",
        "lastName": "Singh"
    }

    assert payload["firstName"] == "Sahil"

    assert payload["lastName"] == "Singh"


def test_create_employee_with_custom_employee_id(employee_api):

    payload = {
        "firstName": "Rahul",
        "lastName": "Verma",
        "employeeId": "EMP1001"
    }

    assert payload["employeeId"] == "EMP1001"


def test_employee_api_object(employee_api):

    assert isinstance(employee_api, EmployeeAPI)


def test_get_all_employees(employee_api):

    response = employee_api.get_all_employees()

    assert response.status_code == 200


def test_create_employee(employee_api):

    response = employee_api.create_employee(
        "Sahil",
        "Singh"
    )

    assert response.status_code == 200