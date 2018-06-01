# -*- coding: utf-8 -*-
"""
作者：ipe-he
创建时间：2018年3月2日
脚本描述：爬取www.aqistudy.cn，获取城市的AQI历史数据，数据的载入是使用JS方式，
读取HTML的方法不能读到表格中的内容
"""
import requests
import re
import csv
from time import sleep
from bs4 import BeautifulSoup

payload = {
    'city': '北京',
    'month': '201701',
}
headers = ''
url = 'https://www.aqistudy.cn/historydata/daydata.php'

def get_page_data(payload):
    # 返回值统一到一个列表里
    html = requests.post(url,data=payload).text
    soup = BeautifulSoup(html, 'lxml')
    table = soup.find('th',text='日期')
    # print(table.parent.parent)
    # trs = table.find_all('tr')
    # trs = trs[1:]
    # rows = []
    # for row in trs:
    #     rows.append([val.text for val in row.find_all('td')])
    # with open('D:\IPE_download\\aqistudy\{}.csv'.format(payload['city']), 'a',newline='') as f:
    #     writer = csv.writer(f)
    #     writer.writerows(row for row in rows if row)


if __name__ == '__main__':
    get_page_data(payload)