#encoding=utf-8
import requests
import re
import logging
import os
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}


def parse_url_to_html(url):
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'lxml')
        # 附件链接
        files_tag = soup.find_all('a',href=re.compile("(xls|xlsx|doc|docx)$"))
        return files_tag

    except Exception as e:

        logging.error("解析错误", exc_info=True)

def get_file(url_tail,file_name):
    file_path_head = r'D:\IPE_download\jdxjc\浙江\\'
    url_head = 'http://www.zjepb.gov.cn'
    url = url_head + url_tail
    try:
       response =  requests.get(url)
       if response.content:
           file_path = file_path_head + file_name
           with open(file_path, 'wb') as f:
               f.write(response.content)
               print('附件:{}下载成功'.format(file_name))
    except:
        print('附件下载失败{}'.format(file_name))

url1 = 'http://www.zjepb.gov.cn/col/col1201434/index.html?uid=3969356&pageNum=1'
url2 = 'http://www.zjepb.gov.cn/col/col1201434/index.html?uid=3969356&pageNum=2'
url3 = 'http://www.zjepb.gov.cn/col/col1201434/index.html?uid=3969356&pageNum=3'
url4 = 'http://www.zjepb.gov.cn/col/col1201434/index.html?uid=3969356&pageNum=4'

def get_urls(url):
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text,'lxml')
    files_tag = soup.find('div',id="3969356")
    file_a = BeautifulSoup(files_tag.text, 'lxml')
    file_as = file_a.find_all('a')
    return file_as

if __name__ == '__main__':
    #下载单个页面中的信息
    message_url = ['http://www.zjepb.gov.cn/art/2013/12/5/art_1201434_14784357.html',
                   'http://www.zjepb.gov.cn/art/2013/11/22/art_1201434_14784363.html',
                   'http://www.zjepb.gov.cn/art/2013/11/4/art_1201434_14784354.html',
                   'http://www.zjepb.gov.cn/art/2013/5/15/art_1201434_14784351.html']
    for i in message_url:
        m = parse_url_to_html(i)
        for i in m:
            get_file(i['href'],i.text)


    ## 获取单个页面信息后分页面自动下载
    # m = get_urls(url2)
    # print(len(m))
    # for i in m:
    #     sign_url = 'http://www.zjepb.gov.cn/' + i['href']
    #     m = parse_url_to_html(sign_url)
    #     for i in m:
    #         get_file(i['href'],i.text)