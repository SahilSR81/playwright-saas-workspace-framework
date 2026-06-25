import os

from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")

BROWSER = os.getenv("BROWSER", "chromium")

HEADLESS = os.getenv("HEADLESS", "False").lower() == "true"

SLOW_MO = int(os.getenv("SLOW_MO", 0))

TIMEOUT = int(os.getenv("TIMEOUT", 30000))

ENV = os.getenv("ENV", "QA")