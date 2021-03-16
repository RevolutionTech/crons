import os
import re
import sys

from scraper import PaginatedWebScraper
from smtp import SimpleSMTPClient


class WebMonitor:

    EMAIL_SUBJECT = "Web Monitor"
    SECTION_HTML_TEMPLATE = """
    <!DOCTYPE html>
    <html lang=\"en\">
      <head>
        <meta charset=\"utf-8\">
        <title>Web Monitor</title>
      </head>
      <body>
        <div align=\"center\">
          <h2>Results from Web Monitor</h2>
        </div>
        <p>The regex {monitor_regex} was found on <a href=\"{found_url}\">{found_url}</a>.</p>
      </body>
    </html>
    """
    SECTION_TEXT_TEMPLATE = "The regex {monitor_regex} was found at:\n{found_url}"

    MONITOR_URL = os.environ["MONITOR_URL"]
    MONITOR_REGEX = os.environ["MONITOR_REGEX"]

    @classmethod
    def monitor_url(cls):
        sys.stdout.write("Searching for regex...")
        sys.stdout.flush()

        scraper = PaginatedWebScraper(url=cls.MONITOR_URL, regex=cls.MONITOR_REGEX)
        found_url = scraper.find_url_containing_regex()
        if found_url:
            content_html = cls.SECTION_HTML_TEMPLATE.format(monitor_regex=cls.MONITOR_REGEX, found_url=found_url)
            content_text = cls.SECTION_TEXT_TEMPLATE.format(monitor_regex=cls.MONITOR_REGEX, found_url=found_url)
            SimpleSMTPClient.send_email(subject=cls.EMAIL_SUBJECT, content_text=content_text, content_html=content_html)
            sys.stdout.write("Regex found and notification email sent successfully!")
        else:
            sys.stdout.write("Regex not found, nothing to notify.")

        sys.stdout.write("\n")
        sys.stdout.flush()


def lambda_handler(_event, _context):
    WebMonitor.monitor_url()
