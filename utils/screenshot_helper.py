def take_screenshot(page, name):
    page.screenshot(path=f"screenshots/{name}.png")