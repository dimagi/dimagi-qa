import datetime

from imap_tools import MailBox
from imap_tools import AND, OR, NOT
from bs4 import BeautifulSoup
import re
import pandas as pd

from HQSmokeTests.userInputs.user_inputs import UserData

""""Contains test page elements and functions related to the app installation and form submission on mobile"""


class EmailVerification:

    def __init__(self, settings):
        self.imap_host = "imap.gmail.com"
        self.imap_user = settings['login_username']
        self.imap_pass = settings['imap_password']

    def get_hyperlink_from_latest_email(self, subject, url):
        if 'www' in url:
            from_email = UserData.from_email_prod
        elif 'india' in url:
            from_email = UserData.from_email_india
        else:
            from_email = UserData.from_email

        with MailBox(self.imap_host).login(self.imap_user, self.imap_pass, 'INBOX') as mailbox:
            bodies = [msg.html for msg in
                      mailbox.fetch(AND(subject=subject, from_ =from_email, date=datetime.date.today()))]
        soup = BeautifulSoup(str(bodies[len(bodies)-1]), "html.parser")
        links = []
        for link in soup.findAll('a', attrs={'href': re.compile("^https://")}):
            links.append(link.get('href'))
            # print("link: ", link)
        # links  # in this you will have to check the link number starting from 0.
        print(len(links))
        print(links[0])
        return str(links[0])

    def get_email_body_from_latest_email(self, subject, url):
        if 'www' in url:
            from_email = UserData.from_email_prod
        elif 'india' in url:
            from_email = UserData.from_email_india
        else:
            from_email = UserData.from_email
        print(subject)
        with MailBox(self.imap_host).login(self.imap_user, self.imap_pass, 'INBOX') as mailbox:
            bodies = [msg.html for msg in
                      mailbox.fetch(AND(subject=subject, from_=from_email,  date=datetime.date.today()))]
        print(len(bodies))
        n = ''
        end = -1
        if "Worker Activity" in subject or "Case Activity" in subject:
            n = 2
        else:
            n = 1
        if "Application Status" in subject or "Device Log" in subject or "Case List" in subject:
            end = None
        else:
            end = -1
        soup = BeautifulSoup(str(bodies[len(bodies)-1]), "html.parser")
        tr = []
        table = []

        for row in soup.select("tr")[n:end]:
            for td in row.select("td"):
                td = td.get_text()
                td = str(td).replace("\\r", '')
                td = str(td).replace("\\n", '')
                td = re.sub("\r\n+", "", td)
                tr.append(td.strip())
            table.append(tr)
        print(len(table))
        print(table[-1])
        return table[-1]

    def get_email_body_from_latest_email_proj_perf(self, subject, url):
        if 'www' in url:
            from_email = UserData.from_email_prod
        elif 'india' in url:
            from_email = UserData.from_email_india
        else:
            from_email = UserData.from_email
        print(subject)
        with MailBox(self.imap_host).login(self.imap_user, self.imap_pass, 'INBOX') as mailbox:
            bodies = [msg.html for msg in
                      mailbox.fetch(AND(subject=subject, from_=from_email, date=datetime.date.today()))]
        soup = BeautifulSoup(str(bodies[len(bodies)-1]), "html.parser")
        tr = []
        td = []
        table = []
        tab_low = []
        tab_inactive = []
        tab_high = []
        for tables in soup.findAll('table'):
            table.append(tables)
        table_low = table[0]
        table_inactive = table[1]
        table_high = table[2]

        if len(table_low.findAll('td')) > 0:
            print(len(table_low.findAll('td')))
            for row in table_low.select("tr"):
                tr = []
                for cells in row.select("td"):
                    td = []
                    text = cells.get_text()
                    text = str(text).replace("\\r", '')
                    text = str(text).replace("\\n", '')
                    text = re.sub("\r\n+", "", text)
                    text = str(text).replace(u'\xa0', u'')
                    text = str(text).strip()
                    text = re.sub(" +", "--", text)
                    if text == '':
                        td.append("No data available in table")
                    else:
                        td.append(text)
                    tr.extend(td)
                if tr == []:
                    print("empty row")
                else:
                    tab_low.extend(tr)
        else:
            tab_low = ['No data available in table']

        print("tab low", tab_low)


        if len(table_inactive.findAll('td')) > 0:
            print(len(table_inactive.findAll('td')))
            for row in table_inactive.select("tr"):
                tr = []
                for cells in row.select("td"):
                    td = []
                    text = cells.get_text()
                    text = str(text).replace("\\r", '')
                    text = str(text).replace("\\n", '')
                    text = re.sub("\r\n+", "", text)
                    text = str(text).replace(u'\xa0', u'')
                    text = str(text).strip()
                    text = re.sub(" +", "--", text)
                    if text == '':
                        td.append("No data available in table")
                    else:
                        td.append(text)
                    tr.extend(td)
                if tr == []:
                    print("empty row")
                else:
                    tab_inactive.extend(tr)
        else:
            tab_inactive = ['No data available in table']

        print("tab inactive", tab_inactive)

        if len(table_high.findAll('td')) > 0:
            print(len(table_high.findAll('td')))
            for row in table_high.select("tr"):
                tr = []
                for cells in row.select("td"):
                    td = []
                    text = cells.get_text()
                    text = str(text).replace("\\r", '')
                    text = str(text).replace("\\n", '')
                    text = re.sub("\r\n+", "", text)
                    text = str(text).replace(u'\xa0', u'')
                    text = str(text).strip()
                    text = re.sub(" +", "--", text)
                    if text == '':
                        td.append("No data available in table")
                    else:
                        td.append(text)
                    tr.extend(td)
                if tr == []:
                    print("empty row")
                else:
                    tab_high.extend(tr)
        else:
            tab_high = ['No data available in table']

        print("tab high", tab_high)
        table_data = [tab_low + tab_inactive + tab_high]
        return table_data