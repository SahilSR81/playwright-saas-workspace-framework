import os
from dotenv import load_dotenv

load_dotenv(override=True)

BASE_URL = os.getenv(
    "BASE_URL",
    "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login",
)

BROWSER = os.getenv("BROWSER", "chromium")

HEADLESS = os.getenv("HEADLESS", "False").lower() == "true"

SLOW_MO = int(os.getenv("SLOW_MO", "0"))

TIMEOUT = int(os.getenv("TIMEOUT", "30000"))

ENV = os.getenv("ENV", "QA")

USERNAME = os.getenv("USERNAME", "Admin")

PASSWORD = os.getenv("PASSWORD", "admin123")