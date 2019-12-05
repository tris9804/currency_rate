from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
import requests

# import ssl
# ssl._create_default_https_context = ssl._create_unverified_context
import json
import os
import schedule
from selenium import webdriver 
from selenium.webdriver.support.ui import Select

# 爬每天匯率
def everyday_rate():
    url = "https://rate.bot.com.tw/xrt?Lang=zh-TW"
    response = urlopen(url)
    html = BeautifulSoup(response)
    rows = html.find("tbody").find_all("tr")
    for r in rows:
        datas = r.find_all("td")
        if "人民幣" in datas[0].text:
            print("人民幣現金匯率:", datas[2].text)
            print('人民幣即期匯率:', datas[4].text)


# 每日排程
routine = '9:30'
schedule.every().day.at(routine).do(everyday_rate)
while True:
    schedule.run_pending()
    time.sleep(1)


# 2018/01~2019/12歷史匯率
driver = webdriver.Chrome()

i = 0
j = 0
for i in range(2):
    for j in range(12):
        url = 'https://rate.bot.com.tw/xrt/history?lang=zh-TW'
        driver.get(url)
        driver.find_element_by_id('month').click()
        year = Select(driver.find_element_by_name('year'))
        year.select_by_index(i)
        
        month = Select(driver.find_element_by_name('month'))
        month.select_by_index(j)
        currency = Select(driver.find_element_by_name('currency'))
        currency.select_by_value('CNY')
        driver.find_element_by_xpath('/html/body/div[1]/main/div[3]/div[2]/form[1]/div[6]/a').click()

        response = driver.page_source

        html = BeautifulSoup(response)
        rows = html.find("tbody").find_all('tr')

        for r in rows:
            datas = r.find_all("td")
            if "人民幣" in datas[1].text:
                day = r.find('td', {'class':'text-center'})
                print('日期:', day.text)
                print('人民幣現金匯率:', datas[3].text)
                print('人民幣即期匯率:', datas[5].text)
        time.sleep(1)
            
        j += 1
    i += 1


