#encoding=utf-8
import requests
import re
import logging
from time import sleep
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

def get_file(url,file_name):
    file_path_head = r'D:\IPE_download\jdxjc\广西\\'
    try:
       response =  requests.get(url)
       if response.content:
           file_path = file_path_head + file_name
           with open(file_path, 'wb') as f:
               f.write(response.content)
               print('附件:{}下载成功'.format(file_name))
    except:
        print('附件下载失败{}'.format(file_name))

def get_urls(url):
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text,'lxml')
    files_tag = soup.find_all('h1')
    mus = soup.find('div',class_='list-mod-bd')
    list = mus.contents
    file_as = list[3].find_all('a')
    return file_as


if __name__ == '__main__':
    #下载单个页面中的信息
    message_url = ['http://www.gxepb.gov.cn/xxgkml/ztfl/hjglywxx/jcgl/201404/t20140401_18495.html',
                   'http://www.gxepb.gov.cn/xxgkml/ztfl/hjglywxx/jcgl/201410/t20141009_20720.html',
                   'http://www.gxepb.gov.cn/xxgkml/ztfl/hjglywxx/jcgl/201410/t20141009_20719.html',
                   'http://www.gxepb.gov.cn/xxgkml/ztfl/hjglywxx/jcgl/201401/t20140120_19062.html',
                   'http://www.gxepb.gov.cn/xxgkml/ztfl/hjglywxx/jcgl/201310/t20131015_16793.html',
                   'http://www.gxepb.gov.cn/xxgkml/ztfl/hjglywxx/jcgl/201310/t20131015_16793.html',
                   'http://www.gxepb.gov.cn/xxgkml/ztfl/hjglywxx/jcgl/201307/t20130708_15984.html',
                   'http://www.gxepb.gov.cn/xxgkml/ztfl/hjglywxx/jcgl/201304/t20130412_15066.html',
                   'http://www.gxepb.gov.cn/xxgkml/ztfl/hjglywxx/jcgl/201210/t20121009_12653.html',
                   ]
    for i in message_url:
        m = parse_url_to_html(i)
        for s in m:
            url_head = i[:-20]
            url = url_head + s['href'][1:]
            get_file(url,s.text)


    ## 获取单个页面信息后分页面自动下载
    # url1 = 'http://www.gxepb.gov.cn/xxgkml/ztfl/hjjgxxgk/wryjc/wryjcjg/index_2.html'
    # m = get_urls(url1)
    # for i in m:
    #     sign_url = 'http://www.gxepb.gov.cn/xxgkml/ztfl' + i['href'][8:]
    #     m = parse_url_to_html(sign_url)
    #     url_head = sign_url[:-25]
    #     for i in m:
    #         url = url_head + i['href'][1:]
    #         get_file(url,i.text)
    #         sleep(1)