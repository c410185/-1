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
        the_div = soup.find('div', id='zoomfont')
        pattern = re.compile("<a.*?href=[\"']?((https?://)?/?[^\"']+)[\"']?.*?>(.+)</a>")
        files_tag = pattern.search(str(the_div))
        if files_tag is not None:
            files_tag = BeautifulSoup(files_tag.group(),'lxml')
            files_url = files_tag.find_all('a')
            # BS4会给元素加上完整的HTML标签，所以需要再次取出a标签
        else:
            files_url = []
        return files_url

    except Exception as e:

        logging.error("解析错误", exc_info=True)

def get_file(url,file_name,num):
    file_path_head = r'D:\IPE_download\jdxjc\内蒙古\\'
    try:
       response =  requests.get(url, headers=headers)
       if response.content:
           file_path = file_path_head + '第{}页_'.format(num + 1) + file_name
           with open(file_path, 'wb') as f:
               f.write(response.content)
               print('附件:{}下载成功'.format(file_name))
    except:
        print('附件下载失败{}'.format(file_name))

def get_urls(url):
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text,'lxml')
    mus = soup.find('div',class_='font_lan18')
    mus = mus.next_sibling.next_sibling
    file_as = mus.find_all('a')
    return file_as


if __name__ == '__main__':
    # 下载单个页面中的信息
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
    url1 = 'http://www.nmgepb.gov.cn/wryhjjg/wryjc/gkjcjg/index.html'
    for i in range(1,31):
        url = 'http://www.nmgepb.gov.cn/wryhjjg/wryjc/gkjcjg/index_{}.html'.format(i)
        message_list = get_urls(url)
        for message in message_list:
            sign_url = urljoin(url,message['href'])
            # print(sign_url)
            files_list = parse_url_to_html(sign_url)
            if len(files_list) == 0:
                print(message.text, '此页面无附件')
            else:
                for file in files_list:
                    file_url = file['href']
                    print(file_url)
                    get_file(file_url,file.text,i)
                    sleep(1)


    # message_url = 'http://www.nmgepb.gov.cn/wryhjjg/wryjc/gkjcjg/201802/t20180202_1558513.html'
    # m = parse_url_to_html(message_url)
    # print(m)