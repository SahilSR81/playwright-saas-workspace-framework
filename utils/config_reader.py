from configparser import ConfigParser

config = ConfigParser()
config.read("config/config.ini")

BASE_URL = config.get("web", "base_url")