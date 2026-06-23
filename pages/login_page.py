from utils.config_reader import BASE_URL


class LoginPage:

    def __init__(self, page):
        self.page = page

    def navigate(self):
        self.page.goto(BASE_URL)

    def get_page_title(self):
        return self.page.title()

    def get_current_url(self):
        return self.page.url