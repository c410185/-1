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
    files_ta = soup.find('ul')
    files_tag = files_ta.find_all('a')
    return files_tag

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
    file_path_head = r'D:\IPE_download\jdxjc\云南\\'
    try:
       response =  requests.get(url)
       if response.content:
           file_path = file_path_head + file_name + '.pdf'
           with open(file_path, 'wb') as f:
               f.write(response.content)
               print('附件:{}下载成功'.format(file_name))
    except:
        print('附件下载失败{}'.format(file_name))

def run(url):
    a_lists = get_urls(url)
    for message in a_lists:
        file_url = urljoin(url, message['href'])
        print(file_url)
        if file_url[-1] == 'f':
            get_file(file_url,message.text)
        elif file_url[-1] == 'l':
            file_list = find_files(file_url)
            for a in file_list:
                real_file_url = urljoin(file_url,a['href'])
                get_file(real_file_url,a.text)
        sleep(1)

if __name__ == '__main__':
    url_0 = 'http://www.ynepb.gov.cn/hjjc1/wryjc/jdxjcjb/index.html'
    url_1 = 'http://www.ynepb.gov.cn/hjjc1/wryjc/jdxjcjb/index_1.html'
    url_2 = 'http://www.ynepb.gov.cn/hjjc1/wryjc/jdxjcjb/index_2.html'
    run(url_0)
    run(url_1)
    run(url_2)
