# coding: utf-8
import requests
from bs4 import BeautifulSoup
from time import sleep
import re

my_hearders = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'}

# 代理都不能用
proxies = {
  "http": "http://166.111.80.162:3128",
  "https": "http://121.43.178.58:3128",
}

url_head = 'http://113.57.151.5:8030/HBHB/companyInfo.action'

def get_table(payload):
    # 目前的编码是GBK，如何转换编码，可能是程序没有添加开头的默认编码，已经添加
    # 添加hearders,但是报错，后又去除
    response = requests.get(url_head, params=payload)
    soup = BeautifulSoup(response.text, 'lxml')
    tr = soup.find_all('tr', class_='main_info')
    file_path = 'D:\何方辉\网站爬取\\temp.csv'
    f = open(file_path, 'a', newline='')
    for i in tr:
        m = re.sub('\s',' ',i.text)
        s = re.sub(' +', ' ', m)
        f.write(s + '\n')
    f.close()
    print('第{}页抓取完成'.format(payload['nextPage']))
    sleep(3)
    print('---------------+3秒-----------------')

def set_condition(page,color='0'):
    businessName = ''
    qylx_v = '00'
    color_v = color
    nextPage_v = str(page)
    sz_v = '000000'
    qx_v = '000000'

    payload = {
        'businessName': businessName,
        'qylx': qylx_v,
        'color': color_v,
        'nextPage': nextPage_v,
        'sz': sz_v,
        'qx': qx_v,
    }
    return payload

def get_all(begin_page,maxpage):
    for i in range(begin_page,int(maxpage) + 1):
        payload = set_condition(i)
        get_table(payload)


if __name__ == '__main__':
    get_all(1,2)