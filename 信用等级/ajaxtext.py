#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
作者：昨夜星辰
创建时间：2017年6月23日
脚本描述：爬取翻页URL不变的网站。POST方式
"""

import re
import sys
import requests
from bs4 import BeautifulSoup

def update_data_dict(soup):
    data_dict['__VIEWSTATE'] = soup.find(id='__VIEWSTATE')['value']
    data_dict['__EVENTVALIDATION'] = soup.find(id='__EVENTVALIDATION')['value']
    data_dict['__EVENTARGUMENT'] += 1
    data_dict['AspNetPager1_input'] += 1

def save_data(soup):
    with open('D:\何方辉\网站爬取\\result.txt', 'a') as f:
        for tr in soup('tr', bgcolor='#F5F9FC'):
            f.write(' '.join([td.text for td in tr('td')]) + '\n')

def get_next_page_data():
    html2 = requests.post(url, data=data_dict).text
    soup2 = BeautifulSoup(html2, 'lxml')
    update_data_dict(soup2)
    save_data(soup2)

url = 'http://ris.szpl.gov.cn/bol/index.aspx'
html1 = requests.get(url).text
soup1 = BeautifulSoup(html1, 'lxml')
text = soup1.find('div', 'PageInfo').text
total_page_num = re.search(u'共(\d+)页', text).group(1)
data_dict = dict(
    __EVENTTARGET='AspNetPager1',
    __EVENTARGUMENT=1,
    __VIEWSTATE='',
    __VIEWSTATEGENERATOR='248CD702',
    __VIEWSTATEENCRYPTED='',
    __EVENTVALIDATION='',
    tep_name='',
    organ_name='',
    site_address='',
    AspNetPager1_input=0,
)
update_data_dict(soup1)
save_data(soup1)
for i in range(int(total_page_num)):
    get_next_page_data()