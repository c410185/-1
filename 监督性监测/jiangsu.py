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

def get_urls(url):
    response = requests.get(url,params=urls_headers)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text,'lxml')
    files_tag = soup.find_all('a',class_='afont')
    return files_tag

def find_files(url):
    try:
        response = requests.get(url, headers=urls_headers)
        soup = BeautifulSoup(response.content, 'lxml')
        # 附件链接
        files_tag = soup.find_all('a',href=re.compile("(xls|xlsx|doc|docx|pdf)$"))
        return files_tag
    except Exception as e:
        logging.error("解析错误", exc_info=True)

def get_file(url,file_name):
    file_path_head = r'D:\IPE_download\jdxjc\江苏\\'
    try:
       response =  requests.get(url)
       if response.content:
           file_path = file_path_head + file_name
           with open(file_path, 'wb') as f:
               f.write(response.content)
               print('附件:{}下载成功'.format(file_name))
    except:
        print('附件下载失败{}'.format(file_name))

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
    urls_0 = 'http://www.jshb.gov.cn:8080/pub/root14/xxgkcs/889/968/970/list.htm?classid=970'
    urls_1 = 'http://www.jshb.gov.cn:8080/pub/root14/xxgkcs/889/968/970/list_1.htm?classid=970'
    urls_2 = 'http://www.jshb.gov.cn:8080/pub/root14/xxgkcs/889/968/970/list_2.htm?classid=970'
    urls_3 = 'http://www.jshb.gov.cn:8080/pub/root14/xxgkcs/889/968/970/list_3.htm?classid=970'
    run(urls_1)
    run(urls_2)
    run(urls_3)