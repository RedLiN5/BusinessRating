__author__ = 'Leslie'

import requests
from bs4 import BeautifulSoup


session = requests.Session()

url = 'https://www.itjuzi.com/investfirm/6510'
USERNAME = '4372125@qq.com'
PASSWORD = '4372125'
login_data = {'identity':USERNAME, 'password':PASSWORD}
headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
response = session.get(url, cookies={'from-my': 'browser'}, headers=headers, data=login_data)
soup = BeautifulSoup(response.text, 'lxml')
print soup.find_all('span', {'class': 'verdana'})[0].text
print soup.find_all('a', {'class': 'c'})[0].text
print soup.find_all('td', {'class': None})[0].text
print soup.find_all('td', {'class': None})[1].text
print soup.find_all('td', {'class': ' mobile-none'})