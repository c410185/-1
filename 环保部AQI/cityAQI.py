# -*- coding: utf-8 -*-
"""
作者：ipe-he
创建时间：2018年2月26日
脚本描述：爬取翻页URL不变的网站--环保部外网中心，通过城市的citycode获取城市的AQI
"""
import requests
import re
import csv
from time import sleep
from bs4 import BeautifulSoup

url = 'http://datacenter.mep.gov.cn/websjzx/report/list.vm'
form_data = {
    'pageNum': 1,
    'orderby' : '',
    'ordertype' : '',
    'xmlname' : '1513844769596kqzllb',
    'gisDataJson' : '',
    'queryflag' : 'close',
    'customquery' : 'false',
   'isdesignpatterns' : 'false',
    'citytime' : '2017-01-01',
    'citycodes' : 110000,
    'inPageNo' : 1,
}

def get_page_data(city_name):
    # 返回值统一到一个列表里
    list = []
    html = requests.post(url,data=form_data).text
    soup = BeautifulSoup(html, 'lxml')
    table = soup.find('table', id="GridView1")
    #list_a = soup.find_all('a', href='javascript:void(0)')
    # print(table.text)
    trs = table.find_all('tr')
    trs = trs[1:]
    # 使用正则去掉多余空格，只保留一个，这样会使没有值的单元格忽略
    # f = open('D:\IPE_download\datacenter\{}.txt'.format(city_name), 'a')
    # for i in trs:
    #     m = re.sub('\s',' ',i.text)
    #     s = re.sub(' +', ' ', m)
    #     f.write(s + '\n')
    # f.close()
    rows = []
    for row in trs:
        rows.append([val.text for val in row.find_all('td')])
    with open('D:\IPE_download\datacenter\{}.csv'.format(city_name), 'a',newline='') as f:
        writer = csv.writer(f)
        writer.writerows(row for row in rows if row)

def update_form_data():
    form_data['pageNum'] += 1
    form_data['inPageNo'] += 1

def download_all(city_name):
    i = 1
    # 写死了抓取的页面数量
    while i < 17:
        print('正在下载第{}页数据'.format(i))
        get_page_data(city_name)
        update_form_data()
        i += 1
        sleep(1)

file_path = 'D:\IPE_download\datacenter\citycode.csv'
def return_code():
    with open(file_path,newline='') as f:
        reader = csv.reader(f)
        # 此处应有越界判断
        row1 = next(reader)
        return row1


if __name__ == '__main__':
    city_name = '北京市'
    #download_all(city_name)