import csv
import os
import smtplib
from email.message import EmailMessage
from typing import List

CURRENT_DIR_PATH = os.path.dirname(os.path.realpath(__file__))
EMAIL_SERVER_HOST = 'email-smtp.us-west-2.amazonaws.com'
EMAIL_SERVER_PORT = 465


class InterestingEmail:
    def __init__(self, to_address: List[str], from_address: str):
        self._msg = EmailMessage()
        self._msg['Subject'] = "Interesting links/news/articles of the day"
        self._msg['From'] = from_address
        self._msg['To'] = to_address

    def create(self, links_csv_file):
        email_content = self._email_content(links_csv_file)
        self._msg.set_content(email_content, subtype='html')

    def send(self, username, password):
        try:
            server = smtplib.SMTP_SSL(EMAIL_SERVER_HOST, EMAIL_SERVER_PORT)
            server.ehlo()
            # server.starttls()
            server.login(username, password)
            print(self._msg)
            server.send_message(self._msg)
            server.close()

            print('Email sent!')
        except Exception as e:
            print('Sending email failed. Error: ', e)

    def _email_content(self, links_csv_file):
        with open(CURRENT_DIR_PATH + "/email.html", 'r') as fr:
            email_template = fr.read()
        links_content = self._create_links_list(links_csv_file)
        email_content = email_template.format(links=links_content)
        return email_content

    def _create_links_list(self, links_csv_file: str) -> str:
        links_content = "<ul>"
        with open(links_csv_file, newline='', encoding="utf8") as csv_file:
            for row in csv.DictReader(csv_file, delimiter=',', quotechar='"'):
                links_content += self._create_link_list_item(row)
        links_content += "</ul>"
        return links_content

    def _create_link_list_item(self, row):
        item_content = "<li>" + row['title'] + ' - ' + row['url']
        if row['body'] is not None or len(row['body']) == 0:
            item_content += "<br/>" + row["body"]
        item_content += "</br>Published At: " + row['published_at']
        item_content += "</li>"
        return item_content
