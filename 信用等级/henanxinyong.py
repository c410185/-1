# -*- coding: utf-8 -*-
"""
作者：ipe-he
创建时间：2018年2月8日
脚本描述：爬取翻页URL不变的网站,河南环保厅企业信用等级公开
"""

import re
from time import sleep
import sys
import requests
from bs4 import BeautifulSoup

url = 'http://www.hnep.gov.cn:81/xycx.aspx'
html1 = requests.get(url).text
soup1 = BeautifulSoup(html1, 'lxml')
# text = soup1.find('div', 'PageInfo').text
# total_page_num = re.search(u'共(\d+)页', text).group(1)
data_dict = {
    '__EVENTTARGET':'Right$Asp_Data',
    '__EVENTARGUMENT':1,
    '__LASTFOCUS':'',
    '__VIEWSTATE':'',
    '__VIEWSTATEGENERATOR':'867F6B77',
    '__EVENTVALIDATION':'',
    'Right%24txt_EnpName':'输入企业名模糊查询',
    'Right%24ddl_year':2017,
    'Right%24ddl_batch':1,
    'Right%24DropDownList1':'全部',
    'Right%24ddl_regicode':'',
    'Right%24Asp_Data_input':0,
}

def update_data_dict(soup):
    data_dict['__VIEWSTATE'] = soup.find(id='__VIEWSTATE')['value']
    data_dict['__EVENTVALIDATION'] = soup.find(id='__EVENTVALIDATION')['value']
    data_dict['__EVENTARGUMENT'] += 1
    data_dict['Right%24Asp_Data_input'] += 1

def save_data(soup):
    table = soup.find('table', id='tbdata')
    trs = table.find_all('tr')
    trs = trs[1:]
    f = open('D:\何方辉\网站爬取\\result.txt', 'a')
    for i in trs:
        m = re.sub('\s',' ',i.text)
        s = re.sub(' +', ' ', m)
        f.write(s + '\n')
    f.close()

def get_next_page_data():
    html2 = requests.post(url, data=data_dict).text
    soup2 = BeautifulSoup(html2, 'lxml')
    update_data_dict(soup2)
    save_data(soup2)

if __name__ == '__main__':
    update_data_dict(soup1)
    save_data(soup1)
    for i in range(1,48):
        print('正在处理第{}页'.format(i))
        get_next_page_data()
        sleep(1)