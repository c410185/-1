#encoding=utf-8
'''
需要解决合并单元格问题，pandas无法解决问题需要自己找解决方案
'''
import requests
import logging
import os
from bs4 import BeautifulSoup
import pandas as pd

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}

def parse_url_to_html(url):
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'lxml')
        # 定位表格
        tr = soup.find('td',text='行政区')
        html_table = tr.parent.parent.parent
        pd_table = pd.read_html(str(html_table))
        print(type(pd_table))
        print(pd_table[0])
    except Exception as e:

        logging.error("解析错误", exc_info=True)


if __name__ == '__main__':
    url = 'http://xxgk.sdein.gov.cn/wryhjjgxxgk/wryjc/fsjcsj/201802/t20180209_1178919.html'
    parse_url_to_html(url)