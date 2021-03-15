from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from smtplib import SMTP_SSL


class SimpleSMTPClient:

    SMTP_SERVER_ADDRESS = 'smtp.gmail.com'
    EMAIL_FROM = os.environ['EMAIL_FROM']
    EMAIL_TO = os.environ['EMAIL_TO']
    EMAIL_LOGIN = os.environ['EMAIL_LOGIN']
    EMAIL_PASSWORD = os.environ['EMAIL_PASSWORD']

    @classmethod
    def send_email(cls, subject, content_text, content_html):
        email_msg = MIMEMultipart('alternative')
        email_msg['Subject'] = subject
        email_msg['From'] = cls.EMAIL_FROM
        email_msg['To'] = cls.EMAIL_TO
        email_msg.attach(MIMEText(content_text, 'plain'))
        email_msg.attach(MIMEText(content_html, 'html'))
        server = SMTP_SSL(cls.SMTP_SERVER_ADDRESS)
        server.ehlo()
        server.login(cls.EMAIL_LOGIN, cls.EMAIL_PASSWORD)
        server.sendmail(cls.EMAIL_FROM, cls.EMAIL_TO, email_msg.as_string())
        server.close()
