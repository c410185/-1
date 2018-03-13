#encoding=utf-8
import requests
import re
import logging
import json
from time import sleep
from bs4 import BeautifulSoup
from urllib.parse import urljoin


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}
json_headers = {
'Accept':'application/json',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'zh-CN,zh;q=0.9',
'Cache-Control':'no-cache',
'Connection':'keep-alive',
'Content-Length':0,
'Content-Type':'application/json',
'Cookie':'JSESSIONID=7EFB97F66A689600CB2855ABDC3B4CFC',
'Host':'218.60.147.155:8080',
'Origin':'http://218.60.147.155:8080',
'Pragma':'no-cache',
'Referer':'http://218.60.147.155:8080/mzsl/importantPollution/setImportantPollution',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
'X-Requested-With':'XMLHttpRequest',
}

json_dict = {
    'pageIndex':0,
    'limit':20,
}

def find_files(url):
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'lxml')
        # 附件链接
        files_tag = soup.find_all('a',href=re.compile("(xls|xlsx|doc|docx|pdf|rar)$"))
        return files_tag

    except Exception as e:

        logging.error("解析错误", exc_info=True)

def get_file(url,file_name):
    file_path_head = r'D:\IPE_download\jdxjc\辽宁\\'
    try:
       response =  requests.get(url, headers=headers)
       if response.content:
           file_path = file_path_head + file_name
           with open(file_path, 'wb') as f:
               f.write(response.content)
               print('附件:{}下载成功'.format(file_name))
    except:
        print('附件下载失败{}'.format(file_name))

def get_urls(url,json_dict):
    response = requests.post(url, headers=headers,data=json_dict)
    response.encoding = 'utf-8'
    json_list = response.json()
    return json_list['rows']
# json_list['rows']例子，只取了一个值
# [{'id': '77235', 'title': '关于发布2017年5月辽宁省重点源监督性监测结果的公告', 'dateT': '2017-06-21'},...]



if __name__ == '__main__':
    #下载单个页面中的信息
    # message_url = [
    #                'http://www.gzqyjpjc.com/trshb/yxxsh/201601/t20160113_44644.html',
    #                ]
    # for i in message_url:
    #     m = parse_url_to_html(i)
    #     if len(m) == 0:
    #         print(message_url,'此页面无附件')
    #     else:
    #         for s in m:
    #             url_head = i[:-20]
    #             url = url_head + s['href'][1:]
    #             get_file(url,s.text)


    # 获取单个页面信息后分页面自动下载
    url1 = 'http://218.60.147.155:8080/mzsl/importantPollution/pageControl'
    message_url_head = 'http://218.60.147.155:8080/mzsl/vmdetail/polutionDetail?id='
    for num in range(0,7):
        json_dict['pageIndex'] = num
        message_list = get_urls(url1,json_dict)
        for i in message_list:
            message_url = message_url_head + i['id']
            file_urls = find_files(message_url)
            for a in file_urls:
                file_name = i['dateT'] + '发布' + a.text
                # print(a['href'],file_name)
                get_file(a['href'],file_name)
                sleep(2)


    # 多页面下载
    # for i in range(13,23):
    #     url = 'http://www.gzqyjpjc.com/hbtxxfb/jdxjc/index_{}.html'.format(i)
    #     message_list = get_urls(url)
    #     for i in message_list:
    #         sign_url = urljoin(url,i['href'])
    #         # print(sign_url)
    #         files_list = parse_url_to_html(sign_url)
    #         if len(files_list) == 0:
    #             print(i.text, '此页面无附件')
    #         else:
    #             for i in files_list:
    #                 file_url = urljoin(sign_url,i['href'])
    #                 print(file_url)
    #                 get_file(file_url,i.text)
    #                 sleep(1)

# headers格式转换函数
#     s = '''Accept:application/json
# Accept-Encoding:gzip, deflate
# Accept-Language:zh-CN,zh;q=0.9
# Cache-Control:no-cache
# Connection:keep-alive
# Content-Length:0
# Content-Type:application/json
# Cookie:JSESSIONID=7EFB97F66A689600CB2855ABDC3B4CFC
# Host:218.60.147.155:8080
# Origin:http://218.60.147.155:8080
# Pragma:no-cache
# Referer:http://218.60.147.155:8080/mzsl/importantPollution/setImportantPollution
# User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36
# X-Requested-With:XMLHttpRequest'''
#     s = s.strip().split('\n')
#     s = {x.split(':')[0]: x.split(':')[1] for x in s}
#     print(s)
