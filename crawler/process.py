#! /usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import urllib2, urllib
from bs4 import BeautifulSoup
import time
import pandas as pd
import sys


reload(sys)
sys.setdefaultencoding('utf-8')
'https://www.itjuzi.com/user/login'

class crawl(object, max_page, username, password):

    def __init__(self, max_page, username, password):
        self.max_page = max_page
        self.username = username
        self.password = password

    def trade_spider(self):
    columns = ['Investor', 'Investee', 'Industry', 'Date', 'FinancingRound', 'Amount']
    df = pd.DataFrame(columns = columns)
    page_num = int(1)

    while  page_num <= self.max_page:
        try:
            url = 'https://www.itjuzi.com/investfirm?page=%s'% str(page_num)
            hdr = {'User-Agent': 'Mozilla/5.0'}
            request = urllib2.Request(url, headers=hdr)
            page = urllib2.urlopen(request)
            soup = BeautifulSoup(page, "lxml")
            general_data = soup.find_all("ul", {"class": "list-main-investset"})
            data_content = general_data[1].find_all('li')

            for content in data_content:
                'Investor Name:'
                Investor = content.contents[4].text.strip(' ')
                url = content.contents[4].find_all('a')[0].get('href')

                USERNAME = self.username
                PASSWORD = self.passowrd
                session = requests.Session()

                login_data = {'identity':USERNAME, 'password':PASSWORD}
                headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
                response = session.get(url, cookies={'from-my': 'browser'}, headers=headers, data=login_data)
                soup = BeautifulSoup(response.text, 'lxml')

                for i in range(len(soup.find_all('a', {'class': 'c'}))):
                    Investee = soup.find_all('a', {'class': 'c'})[i].text.strip("\n").strip(' ')
                    Industry = soup.find_all('td', {'class': ' mobile-none'})[i].text.strip("\n").strip(' ')
                    Date = soup.find_all('span', {'class': 'verdana'})[i].text.strip("\n").strip(' ')
                    FinancingRound = soup.find_all('td', {'class': None})[2*i].text.strip("\n").strip(' ')
                    Amount = soup.find_all('td', {'class': None})[2*i+1].text.strip("\n").strip(' ')
                    df = df.append(pd.DataFrame([[Investor, Investee, Industry, Date, FinancingRound, Amount]],
                                columns = ['Investor', 'Investee', 'Industry', 'Date', 'FinancingRound', 'Amount']))

            page_num += 1

        except Exception, e:
            error = sys.exc_info()[0]
            print e, error
            page_num += 1

    return df.reset_index(drop=True)


# start = time.time()
# df = trade_spider(300)
# df.to_csv('~/ScrapeData/mydata.csv')

# print '------Running time: %.0f Min %.0f Sec------' % ((time.time() - start) / 60, (time.time() - start) % 60)
