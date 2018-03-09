#encoding=utf-8
import requests
import re
import logging
from time import sleep
from bs4 import BeautifulSoup
from urllib.parse import urljoin


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}


def parse_url_to_html(url):
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'lxml')
        # 附件链接
        files_tag = soup.find_all('a',href=re.compile("(xls|xlsx|doc|docx|pdf|rar)$"))
        return files_tag

    except Exception as e:

        logging.error("解析错误", exc_info=True)

def get_file(url,file_name):
    file_path_head = r'D:\IPE_download\jdxjc\河北\\'
    try:
       response =  requests.get(url, headers=headers)
       if response.content:
           file_path = file_path_head + file_name + '.pdf'
           with open(file_path, 'wb') as f:
               for chunk in response.iter_content(2048):
                   f.write(chunk)
           print('附件:{}下载成功'.format(file_name))
    except:
        fail_urls.append(url)
        print('附件下载失败{}'.format(file_name))

def get_urls(url):
    response = requests.get(url, headers=headers)
    response.encoding = 'GBK'
    soup = BeautifulSoup(response.text,'lxml')
    mus = soup.find('ul',class_='erjilist')
    file_as = mus.find_all('a')
    return file_as


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
    # url1 = 'http://www.gzqyjpjc.com/hbtxxfb/jdxjc/index.html'

    # url = 'http://www.hb12369.net/hjzw/hjjcyyj/jdxjc/index.html'
    # 不需要进入详情页即可下载，下载时会有获取不到的情况，只做了记录，后来根据log手动处理
    fail_urls = []
    for num in range(5,11):
        urls = 'http://www.hb12369.net/hjzw/hjjcyyj/jdxjc/index_{}.html'.format(num)
        message_list = get_urls(urls)
        for i in message_list:
            sign_url = urljoin(urls,i['href'])
            print(sign_url)
            get_file(sign_url,i.text)
            sleep(2)