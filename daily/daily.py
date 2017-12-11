"""
The Daily Roundup
Gathers information across the web that I am interested in and
sends me an email with that information.

:Created: 18 March 2015
:Author: Lucas Connors

"""

import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from smtplib import SMTP
import sys

import requests


class DailyRoundup(object):

    SMTP_SERVER_ADDRESS = 'smtp.gmail.com'
    SMTP_SERVER_PORT = 587
    EMAIL_FROM = os.environ['EMAIL_FROM']
    EMAIL_TO = os.environ['EMAIL_TO']
    EMAIL_LOGIN = os.environ['EMAIL_LOGIN']
    EMAIL_PASSWORD = os.environ['EMAIL_PASSWORD']
    EMAIL_SUBJECT = "Daily Roundup"

    XKCD_API_URL = 'http://xkcd.com/info.0.json'

    HTML_SECTION_BEGIN = """
    <!DOCTYPE html>
    <html lang=\"en\">
      <head>
        <meta charset=\"utf-8\">
        <title>Daily Roundup</title>
      </head>
      <body>
        <div align=\"center\"><h1>Daily Roundup for {weekday}</h1>
    """
    HTML_SECTION_END = """
        </div>
      </body>
    </html>
    """
    HTML_SECTION_XKCD = """
    <h3>Today\'s xkcd: {xkcd_title}</h3>
    <img src=\"{xkcd_img}\" />
    <br /><br />{xkcd_img_alt}
    <br /><br /><hr />
    """
    TEXT_SECTION_XKCD = "Visit xkcd.com to view today\'s xkcd\n"

    @classmethod
    def latest_xkcd(cls):
        xkcd_api_response = requests.get(cls.XKCD_API_URL).json()
        section_xkcd_html = cls.HTML_SECTION_XKCD.format(
            xkcd_title=xkcd_api_response['title'],
            xkcd_img=xkcd_api_response['img'],
            xkcd_img_alt=xkcd_api_response['alt'],
        )
        return section_xkcd_html, cls.TEXT_SECTION_XKCD

    @classmethod
    def send_email_smtp(cls, content_text, content_html):
        email_msg = MIMEMultipart('alternative')
        email_msg['Subject'] = cls.EMAIL_SUBJECT
        email_msg['From'] = cls.EMAIL_FROM
        email_msg['To'] = cls.EMAIL_TO
        email_msg.attach(MIMEText(content_text, 'plain'))
        email_msg.attach(MIMEText(content_html, 'html'))
        server = SMTP(cls.SMTP_SERVER_ADDRESS, cls.SMTP_SERVER_PORT)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(cls.EMAIL_LOGIN, cls.EMAIL_PASSWORD)
        server.sendmail(cls.EMAIL_FROM, cls.EMAIL_TO, email_msg.as_string())
        server.close()

    @classmethod
    def send_email(cls):
        sys.stdout.write("Sending email... ")
        sys.stdout.flush()

        section_xkcd_html, section_xkcd_text = cls.latest_xkcd()
        content_html = (
            cls.HTML_SECTION_BEGIN.format(weekday=datetime.datetime.today().strftime("%A"))
            + section_xkcd_html
            + cls.HTML_SECTION_END
        )
        cls.send_email_smtp(content_text=section_xkcd_text, content_html=content_html)

        sys.stdout.write("Sent successfully!\n")
        sys.stdout.flush()


def lambda_handler(event, context):
    if datetime.datetime.today().weekday() in (0, 2, 4):  # Mon / Wed / Fri
        DailyRoundup.send_email()
