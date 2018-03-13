#encoding=utf-8
import requests
import re
import logging
import json
from time import sleep
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_urls(url):
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text,'lxml')
    files_tag = soup.find('div',class_='wr_san')
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
    file_path_head = r'D:\IPE_download\jdxjc\新疆\\'
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
    for i in range(1,10):
        num = i
        url = 'http://124.117.235.205:8099/eportal/ui?pageId=3499&currentPage=' + str(num) + '&moduleId=d1c3df42c3e1416e9df9fc8b2d42546e'
        print(url)
        run(url)