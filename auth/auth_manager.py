from pathlib import Path

from config.settings import (
    USERNAME,
    PASSWORD,
)

from pages.login_page import LoginPage


AUTH_PATH = Path("playwright/.auth")

AUTH_FILE = AUTH_PATH / "user.json"


def generate_storage_state(page):

    AUTH_PATH.mkdir(parents=True, exist_ok=True)

    login = LoginPage(page)

    login.navigate()

    login.login(USERNAME, PASSWORD)

    page.context.storage_state(
        path=str(AUTH_FILE)
    )