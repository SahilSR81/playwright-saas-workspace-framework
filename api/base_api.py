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
        self._load_cookies_from_storage_state()

        logger.info("API Session initialized")

    def _load_cookies_from_storage_state(self):
        from pathlib import Path
        import json

        auth_dir = Path("playwright/.auth")
        storage_path = auth_dir / "user.json"

        if not storage_path.exists():
            candidates = sorted(auth_dir.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
            if candidates:
                storage_path = candidates[0]
                logger.info("user.json not found, using fallback: %s", storage_path)
            else:
                logger.warning("No storage state files found. API session will be unauthenticated.")
                return

        logger.info("Loading cookies from Playwright storage state: %s", storage_path)
        try:
            with open(storage_path, "r") as f:
                state = json.load(f)

            cookies = state.get("cookies", [])
            for cookie in cookies:
                self.session.cookies.set(
                    name=cookie["name"],
                    value=cookie["value"],
                    domain=cookie.get("domain", ""),
                    path=cookie.get("path", "/")
                )
            logger.info("Successfully loaded %d cookies from storage state", len(cookies))
        except Exception as e:
            logger.error("Failed to load cookies from storage state: %s", e)

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