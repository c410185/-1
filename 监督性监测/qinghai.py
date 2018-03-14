#encoding=utf-8
import requests
import re
import logging
import json
from time import sleep
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_city_url(url):
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text,'lxml')
    files_tag = soup.find('ul',class_="qy_tabs")
    a_list = files_tag.find_all('a')
    city_urls = []
    for a in a_list:
        city_url = urljoin(url,a['href'])
        city_urls.append(city_url)
    return city_urls

def get_urls(url):
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text,'lxml')
    files_tag = soup.find('ul',id='one_con1')
    a_list = files_tag.find_all('a')
    return a_list

def find_files(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'lxml')
        # 附件链接
        files_tag = soup.find_all('a',href=re.compile("(xls|xlsx|doc|docx|pdf)$"))
        return files_tag
    except Exception as e:
        logging.error("解析错误", exc_info=True)

def get_file(url,file_name):
    file_path_head = r'D:\IPE_download\jdxjc\青海\\'
    houzhui = url.split('.')[-1]
    try:
       response =  requests.get(url)
       if response.content:
           file_path = file_path_head + file_name + '.' + houzhui
           with open(file_path, 'wb') as f:
               f.write(response.content)
               print('附件:{}下载成功'.format(file_name))
    except:
        print('附件:{}下载失败'.format(file_name))

def run(url):
    message_list = get_urls(url)
    for message in message_list:
        sign_url = urljoin(url, message['href'])
        files_list = find_files(sign_url)
        for a in files_list:
            file_url = urljoin(sign_url,a['href'])
            get_file(file_url,a.text)
            sleep(1)


if __name__ == '__main__':
    # first_url = 'http://www.qhepb.gov.cn/pub/wryjd/qyxx/hbz/'
    # city_urls = get_city_url(first_url)
    # for url in city_urls:
    #     print(url)
    #     run(url)

    other_urls = [
        'http://www.qhepb.gov.cn/pub/wryjd/qyxx/szg/index_1.html',
        'http://www.qhepb.gov.cn/pub/wryjd/qyxx/xns/index_1.html',
        'http://www.qhepb.gov.cn/pub/wryjd/qyxx/hds/index_1.html',
        'http://www.qhepb.gov.cn/pub/wryjd/qyxx/hds/index_2.html',
        'http://www.qhepb.gov.cn/pub/wryjd/qyxx/hxz/index_1.html',
        'http://www.qhepb.gov.cn/pub/wryjd/qyxx/hxz/index_2.html',
    ]
    for url in other_urls:
        run(url)