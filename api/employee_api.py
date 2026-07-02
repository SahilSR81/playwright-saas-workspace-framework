from api.base_api import BaseAPI
from utils.logger import logger


class EmployeeAPI(BaseAPI):

    EMPLOYEE_ENDPOINT = "/web/index.php/api/v2/pim/employees"

    def __init__(self):
        super().__init__()

    def get_all_employees(self):

        logger.info("Fetching all employees")

        return self.get(
            self.EMPLOYEE_ENDPOINT
        )

    def get_employee(self, employee_id):

        logger.info(
            "Fetching employee %s",
            employee_id
        )

        return self.get(
            f"{self.EMPLOYEE_ENDPOINT}/{employee_id}"
        )

    def create_employee(
        self,
        first_name,
        last_name,
        employee_id=None
    ):

        logger.info(
            "Creating employee %s %s",
            first_name,
            last_name
        )

        payload = {
            "firstName": first_name,
            "lastName": last_name
        }

        if employee_id:
            payload["employeeId"] = employee_id

        return self.post(
            self.EMPLOYEE_ENDPOINT,
            payload
        )

    def update_employee(
        self,
        employee_id,
        payload
    ):

        logger.info(
            "Updating employee %s",
            employee_id
        )

        return self.put(
            f"{self.EMPLOYEE_ENDPOINT}/{employee_id}",
            payload
        )

    def delete_employee(
        self,
        employee_id
    ):

        logger.info(
            "Deleting employee %s",
            employee_id
        )

        return self.delete(
            f"{self.EMPLOYEE_ENDPOINT}/{employee_id}"
        )