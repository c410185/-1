#encoding=utf-8
import requests
import re
import logging
import json
from time import sleep
from bs4 import BeautifulSoup
from urllib.parse import urljoin

urls_headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Host': 'www.jshb.gov.cn',
    'Pragma': 'no-cache',
    'Referer': 'http',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
                }
data_url = 'http://www.lvwang.org.cn/aqi-station-data/get-position-data?zoom=9'
data = {
    'position':'114.755328,36.169742',
    'city':'北京',
    '_csrf':'MnR1aW9qLjdBPwYTXTlEdlMcAD0.XmZ7BDUSOyMZZFxRGD9fF11NTw==',
}
def get_data():
    r = requests.post(url=data_url,data=data)
    print('dd',len(r.json()))
    with open('D:\IPE_download\data.json','a') as f:
        f.writelines(r.json())

if __name__ == '__main__':
    get_data()