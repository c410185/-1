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
        files_tag = soup.find_all('a',href=re.compile("(xls|xlsx|doc|docx|pdf)$"))
        return files_tag
    except Exception as e:
        logging.error("解析错误", exc_info=True)

def get_file(url_tail,file_name):
    file_path_head = r'D:\IPE_download\jdxjc\北京\\'
    url_head = 'http://www.bjepb.gov.cn'
    url = url_head + url_tail
    try:
        #因为要下载二进制流文件，将stream参数置为True stream=True
       response =  requests.get(url,stream=True)
       if response.content:
           file_path = file_path_head + file_name + '.pdf'
           with open(file_path, 'wb') as f:
               for chunk in response.iter_content(1024):
                   f.write(chunk)
           print('附件:{}下载成功'.format(file_name))
    except:
        print('附件下载失败{}'.format(file_name))

def get_urls(url):
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text,'lxml')
    files_tag = soup.find('div', class_="h_wz_m")
    #print('files_tag 长度：',len(files_tag))
    # print(files_tag)
    file_as = files_tag.find_all('a')
    return file_as

if __name__ == '__main__':
    #下载单个页面中的信息
    # message_url = ['http://www.bjepb.gov.cn/bjhrb/xxgk/ywdt/hjjc/gkwryjdxjcjg/827653/index.html']
    # for i in message_url:
    #     m = parse_url_to_html(i)
    #     for i in m:
    #         get_file(i['href'],i.text)
    # text_url = '/bjhrb/xxgk/ywdt/hjjc/gkwryjdxjcjg/827653/2018010908323370982.pdf'
    # text_name = '2017年第四季度国控工业企业监督性监测结果汇总公开数据表-测试'
    # get_file(text_url,text_name)

    url1 = 'http://www.bjepb.gov.cn/bjhrb/ztzl/wryhjjgxx/wryjc/012cbce7-1.html'
    url2 = 'http://www.bjepb.gov.cn/bjhrb/ztzl/wryhjjgxx/wryjc/012cbce7-2.html'
    url3 = 'http://www.bjepb.gov.cn/bjhrb/ztzl/wryhjjgxx/wryjc/012cbce7-3.html'

    # 获取单个页面信息后分页面自动下载
    m = get_urls(url3)
    print(len(m))
    for i in m:
        sign_url = 'http://www.bjepb.gov.cn' + i['href']
        m = parse_url_to_html(sign_url)
        for i in m:
            get_file(i['href'],i.text)