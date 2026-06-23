class BasePage:

    def __init__(self, page):
        self.page = page

    def get_title(self):
        return self.page.title()

    def get_url(self):
        return self.page.url

    def navigate(self, url):
        self.page.goto(url)