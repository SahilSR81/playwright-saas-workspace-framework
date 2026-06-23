from configparser import ConfigParser
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = BASE_DIR / "config" / "config.ini"

config = ConfigParser()
config.read(CONFIG_PATH)

BASE_URL = config.get("web", "base_url")