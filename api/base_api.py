import requests

from config.settings import BASE_URL
from utils.logger import logger


class BaseAPI:

    def __init__(self):

        self.base_url = BASE_URL.replace(
            "/web/index.php/auth/login",
            ""
        )

        self.session = requests.Session()

        self.default_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "Playwright-SaaS-Framework"
        }

        self.session.headers.update(self.default_headers)

        logger.info("API Session initialized")

    def get(self, endpoint, **kwargs):

        url = f"{self.base_url}{endpoint}"

        logger.info("GET %s", url)

        response = self.session.get(url, **kwargs)

        logger.info(
            "Response Status: %s",
            response.status_code
        )

        return response

    def post(self, endpoint, payload=None, **kwargs):

        url = f"{self.base_url}{endpoint}"

        logger.info("POST %s", url)

        response = self.session.post(
            url,
            json=payload,
            **kwargs
        )

        logger.info(
            "Response Status: %s",
            response.status_code
        )

        return response

    def put(self, endpoint, payload=None, **kwargs):

        url = f"{self.base_url}{endpoint}"

        logger.info("PUT %s", url)

        response = self.session.put(
            url,
            json=payload,
            **kwargs
        )

        logger.info(
            "Response Status: %s",
            response.status_code
        )

        return response

    def patch(self, endpoint, payload=None, **kwargs):

        url = f"{self.base_url}{endpoint}"

        logger.info("PATCH %s", url)

        response = self.session.patch(
            url,
            json=payload,
            **kwargs
        )

        logger.info(
            "Response Status: %s",
            response.status_code
        )

        return response

    def delete(self, endpoint, **kwargs):

        url = f"{self.base_url}{endpoint}"

        logger.info("DELETE %s", url)

        response = self.session.delete(
            url,
            **kwargs
        )

        logger.info(
            "Response Status: %s",
            response.status_code
        )

        return response

    def close(self):

        logger.info("Closing API session")

        self.session.close()