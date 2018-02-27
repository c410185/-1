# -*- coding: utf-8 -*-
"""
作者：ipe-he
创建时间：2018年2月26日
脚本描述：爬取翻页URL不变的网站--环保部外网中心，获取城市的citycode
"""
import requests
import re
from bs4 import BeautifulSoup

url = 'http://datacenter.mep.gov.cn/websjzx/report/list.vm'
form_data = {
    'pageNum' : 2,
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
    'V_DATE' : '2018-02-25',
    'inPageNo' : 1,
}

def get_page_data():
    # 希望把返回值统一到一个列表里
    list = []
    city_code = []
    city_name = []
    html = requests.post(url,data=form_data).text
    soup = BeautifulSoup(html, 'lxml')
    # table = soup.find('table', id="GridView1")
    list_a = soup.find_all('a', href='javascript:void(0)')
    for i in list_a:
        print(i['onclick'])
        city_name.append(re.search('[\u4e00-\u9fa5]{3,10}', i['onclick']))
        city_code.append(re.search('[0-9]{6}', i['onclick']))
    return city_name,city_code


if __name__ == '__main__':
    m = get_page_data()