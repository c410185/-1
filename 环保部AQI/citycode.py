# -*- coding: utf-8 -*-
"""
作者：ipe-he
创建时间：2018年2月26日
脚本描述：爬取翻页URL不变的网站--环保部外网中心，获取城市的citycode
"""
import requests
import re
import csv
from time import sleep
from bs4 import BeautifulSoup

url = 'http://datacenter.mep.gov.cn/websjzx/report/list.vm'
form_data = {
    'pageNum': 2,
    'orderby' : '',
    'ordertype' : '',
    'xmlname' : 1512478367400,
    'gisDataJson' : '',
    'queryflag' : 'close',
    'customquery' : 'false',
   'isdesignpatterns' : 'false',
    'roleType' : 'CFCD2084',
    'permission' : 0,
    'AREA' : '',
    'V_DATE' : '2018-02-27',
    'inPageNo' : 1,
}

def update_form_data():
    form_data['pageNum'] += 1
    form_data['inPageNo'] += 1

def get_page_data():
    # 返回值统一到一个列表里
    list = []
    html = requests.post(url,data=form_data).text
    soup = BeautifulSoup(html, 'lxml')
    # table = soup.find('table', id="GridView1")
    list_a = soup.find_all('a', href='javascript:void(0)')
    for i in list_a:
        #print(i['onclick'])
        city_name = (re.search('[\u4e00-\u9fa5]{2,10}', i['onclick']))
        city_code = (re.search('[0-9]{6}', i['onclick']))
        m = [city_name.group(),city_code.group()]
        list.append(m)
    return list

# save to csv
file_path = 'D:\IPE_download\datacenter\citycode.csv'
def save_to_csv(rows):
    with open(file_path,'a',newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

def download_all():
    i = 1
    while i < 38:
        print('正在下载第{}页数据'.format(i))
        all_list = get_page_data()
        update_form_data()
        save_to_csv(all_list)
        i += 1
        sleep(1)

def download_one_page(num):
    form_data['pageNum'] = num
    form_data['inPageNo'] = num - 1
    list = get_page_data()
    save_to_csv(list)
    sleep(2)
    print('休息2秒')

if __name__ == '__main__':
    download_one_page(36)
    download_one_page(37)