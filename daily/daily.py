#!/usr/bin/env python

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

    EMAIL_FROM = os.environ['EMAIL_FROM']
    EMAIL_TO = os.environ['EMAIL_TO']
    EMAIL_LOGIN = os.environ['EMAIL_LOGIN']
    EMAIL_PASSWORD = os.environ['EMAIL_PASSWORD']
    SMTP_SERVER_ADDRESS = 'smtp.gmail.com'
    SMTP_SERVER_PORT = 587

    @staticmethod
    def latest_xkcd():
        xkcd_api_url = "http://xkcd.com/info.0.json"
        xkcd_api_response = requests.get(xkcd_api_url).json()
        section_xkcd_html = (
            "<h3>Today\'s xkcd: {xkcd_title}</h3>"
            "<img src=\"{xkcd_img}\">"
            "<br/><br/>{xkcd_img_alt}"
            "<br/><br/><hr>"
        ).format(
            xkcd_title=xkcd_api_response['title'],
            xkcd_img=xkcd_api_response['img'],
            xkcd_img_alt=xkcd_api_response['alt'],
        )
        section_xkcd_text = "Visit xkcd.com to view today\'s xkcd\n"
        return section_xkcd_html, section_xkcd_text

    @classmethod
    def send_email_smtp(cls, email_subject, email_content_text, email_content_html):
        email_msg = MIMEMultipart('alternative')
        email_msg['Subject'] = email_subject
        email_msg['From'] = cls.EMAIL_FROM
        email_msg['To'] = cls.EMAIL_TO
        email_msg.attach(MIMEText(email_content_text, 'plain'))
        email_msg.attach(MIMEText(email_content_html, 'html'))
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
        section_begin_html = (
            "<!DOCTYPE html>"
            "<html lang=\"en\">"
            "<head>"
            "   <meta charset=\"utf-8\">"
            "   <title>Daily Roundup</title>"
            "</head>"
            "<body>"
            "<div align=\"center\"><h1>Daily Roundup for {weekday}</h1>"
        ).format(weekday=datetime.datetime.today().strftime("%A"))
        section_end_html = (
            "</div>"
            "</body>"
            "</html>"
        )
        section_xkcd_html, section_xkcd_text = cls.latest_xkcd()

        cls.send_email_smtp(
            email_subject="Daily Roundup",
            email_content_text=section_xkcd_text,
            email_content_html=(section_begin_html + section_xkcd_html + section_end_html)
        )
        sys.stdout.write("Sent successfully!\n")
        sys.stdout.flush()


if __name__ == "__main__":
    if datetime.datetime.today().weekday() in (0, 2, 4):  # Mon / Wed / Fri
        DailyRoundup.send_email()
