#encoding=utf-8
import requests
import re
from bs4 import BeautifulSoup
from lxml import etree

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}

begin_url = 'http://www.zjepb.gov.cn/col/col1201434/index.html'

def get_url(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    zb_fileid = soup.find('div',id="3969356")
    return zb_fileid


def get_url_1(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    zb_fileid = soup.find('div',id="3969356")
    return zb_fileid

if __name__ == '__main__':
    all_url = get_url(begin_url)
    print(all_url)