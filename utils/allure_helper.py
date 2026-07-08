import json
from pathlib import Path

import allure
from allure_commons.types import AttachmentType


def attach_screenshot(page, name="Screenshot"):
    screenshot = page.screenshot(full_page=True)
    allure.attach(screenshot, name=name, attachment_type=AttachmentType.PNG)


def attach_html(page, name="Page HTML"):
    html = page.content()
    allure.attach(html, name=name, attachment_type=AttachmentType.HTML)


def attach_url(page, name="Current URL"):
    url = page.url
    allure.attach(url, name=name, attachment_type=AttachmentType.TEXT)


def attach_console_logs(logs, name="Console Logs"):
    text = "\n".join(logs) if logs else "No console logs captured."
    allure.attach(text, name=name, attachment_type=AttachmentType.TEXT)


def attach_json(data, name="JSON Data"):
    allure.attach(
        json.dumps(data, indent=2, default=str),
        name=name,
        attachment_type=AttachmentType.JSON,
    )


def attach_trace(trace_path, name="Browser Trace"):
    path = Path(trace_path)
    if path.exists():
        allure.attach.file(
            str(path),
            name=name,
            attachment_type="application/zip",
            extension="zip",
        )
