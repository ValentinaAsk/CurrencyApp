import time
import smtplib
from bs4 import BeautifulSoup
import requests
from info import *


class CurrencyApp:
    DOLLAR_RUB = "https://yandex.ru/"

    USER = {
        "USER_Agent": USER_AGENT
    }

    difference = 0.0000009

    def __init__(self):
        self.currency = self.get_current_rate()

    def get_current_rate(self):
        full_page = requests.get(self.DOLLAR_RUB, headers=self.USER)
        soup = BeautifulSoup(full_page.content, 'html.parser')
        convert = soup.findAll("span", {"class": "inline-stocks__value_inner"})
        return float(convert[1].text.replace(',', '.'))

    def check_currency(self):
        currency = self.get_current_rate()
        if self.difference < abs(self.currency - currency):
            print('Currency changed more then', self.difference, '.Now it is ', self.get_current_rate())
            self.send()
        time.sleep(100)
        self.check_currency()

    def send(self):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(SENDER, APP_PASSWORD)
        message = 'Currency changed more then ' + str(self.difference) + '.Now it is ' + str(self.get_current_rate())
        server.sendmail(
            SENDER,
            RECIPIENT,
            message
        )
        server.quit()


c = CurrencyApp()
c.check_currency()
