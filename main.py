from urllib.request import urlopen
from bs4 import BeautifulSoup
from openpyxl import load_workbook
import time
import requests

# import ssl
# ssl._create_default_https_context = ssl._create_unverified_context
import json
import os
import schedule
from selenium import webdriver 
from selenium.webdriver.support.ui import Select
import pymysql


db = pymysql.connect("localhost", "root", "P@ssw0rd", "currency_rate")
cursor = db.cursor()

# 爬每天匯率
def everyday_rate(name, currency):
    url = "https://rate.bot.com.tw/xrt?Lang=zh-TW"
    response = urlopen(url)
    html = BeautifulSoup(response, 'html.parser')
    blocks = html.find_all('h1')
    for b in blocks:
        date= ''.join(b.find('span', {'id':'h1_small_id'}).text.split('/'))
    rows = html.find("tbody").find_all("tr")
    
    for r in rows:
        datas = r.find_all("td")
        if name in datas[0].text:
            data = [date , currency, datas[2].text, datas[4].text]
            print(data)
            cursor.execute(
               "INSERT INTO `currency_rate` (`date`, `currency`, `cash_rate`, `spot_rate`) VALUES(%s, %s, %s, %s)",
                data
            )

    db.commit()

def main():
    targets = {'人民幣':'CNY', '美金':'USD', '日圓':'JPY'}
    for name, currency in targets.items():
        everyday_rate(name, currency)

if __name__ == '__main__':
    main()

db.close()
