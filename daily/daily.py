"""
The Daily Roundup
Gathers information across the web that I am interested in and
sends me an email with that information.

:Created: 18 March 2015
:Author: Lucas Connors

"""

import datetime
import sys

from smtp import SimpleSMTPClient
from xkcd import XKCDFetcher


class DailyRoundup(object):

    EMAIL_SUBJECT = "Daily Roundup"

    SECTION_HTML_BEGIN_TEMPLATE = """
    <!DOCTYPE html>
    <html lang=\"en\">
      <head>
        <meta charset=\"utf-8\">
        <title>Daily Roundup</title>
      </head>
      <body>
        <div align=\"center\"><h1>Daily Roundup for {weekday}</h1>
    """
    SECTION_HTML_END = """
        </div>
      </body>
    </html>
    """

    @classmethod
    def send_email(cls):
        sys.stdout.write("Sending email... ")
        sys.stdout.flush()

        section_xkcd_html, section_xkcd_text = XKCDFetcher.latest_xkcd()
        content_html = (
            cls.SECTION_HTML_BEGIN_TEMPLATE.format(weekday=datetime.datetime.today().strftime("%A"))
            + section_xkcd_html
            + cls.SECTION_HTML_END
        )
        SimpleSMTPClient.send_email(
            subject=cls.EMAIL_SUBJECT, content_text=section_xkcd_text, content_html=content_html
        )

        sys.stdout.write("Sent successfully!\n")
        sys.stdout.flush()


def lambda_handler(_event, _context):
    if datetime.datetime.today().weekday() in (0, 2, 4):  # Mon / Wed / Fri
        DailyRoundup.send_email()
