#encoding=utf-8
import requests
import re
import logging
from time import sleep
from bs4 import BeautifulSoup
from urllib.parse import urljoin


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
'Host': 'pub.gdepb.gov.cn',
'Connection': 'keep-alive',
'Pragma': 'no-cache',
'Cache-Control': 'no-cache',
'Upgrade-Insecure-Requests': '1',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Referer': 'http://pub.gdepb.gov.cn/pub/pubcatalogwry/extranet_pub_documents_list_left.jsp?page=2&catalog=8132b393-0140-1000-e000-0001a9fe9b9d&memo=%E6%B1%A1%E6%9F%93%E6%BA%90%E7%9B%91%E6%B5%8B',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.9',
'Cookie': '232EEEB3723FE823C8CEA7D4A0C5D575.jvm1',
}

file_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
'Host': 'www.gdep.gov.cn',
'Connection': 'keep-alive',
'Pragma': 'no-cache',
'Cache-Control': 'no-cache',
'Upgrade-Insecure-Requests': '1',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Referer': 'http://pub.gdepb.gov.cn/pub/pubcatalogwry/extranet_pub_documents_list_left.jsp?page=2&catalog=8132b393-0140-1000-e000-0001a9fe9b9d&memo=%E6%B1%A1%E6%9F%93%E6%BA%90%E7%9B%91%E6%B5%8B',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.9',
'Cookie': '232EEEB3723FE823C8CEA7D4A0C5D575.jvm1',
}

data_dict = {
    'page' : 1,
    'catalog' : '8132b393-0140-1000-e000-0001a9fe9b9d',
    'memo' : '污染源监测',
}

def updata_data_dict():
    data_dict['page'] += 1

def get_urls(url):
    response = requests.get(url,params=data_dict,headers=headers)
    # response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text,'lxml')
    mus = soup.find_all('td',id='SLC')
    # file_as = mus.find_all('a')
    # 定义re模块匹配规则
    my_pattern = '[0-9]{6}'
    #将信息代码存在一个字典中，因为要获取文件名，所以尝试
    code = {}
    for i in mus:
        # 使用re.search 返回单条文件的docId，在循环中使用，并且使用group取出值
        # 使用split分割字符串，并用空值来链接字符串以去掉其中的空格和换行符
        key = re.search(my_pattern,str(i)).group()
        value = "".join(i.text.split())
        code[key] = value
    return code

message_dict = {
    'docId' : 0,
    'kwStr' : '',
}

def find_files(message_url_head,message_dict):
    try:
        response = requests.get(message_url_head,params=message_dict)
        soup = BeautifulSoup(response.content, 'lxml')
        # 附件链接
        # files_tag = soup.find_all('a',href=re.compile("(xls|xlsx|doc|docx|pdf|rar)$"))
        files_tag = soup.find_all('a',text='点击查看文件')
        return files_tag

    except Exception as e:

        logging.error("解析错误", exc_info=True)

def get_file(file_url, file_name,houzhui):
    file_path_head = r'D:\IPE_download\jdxjc\广东\\'
    try:
       response =  requests.get(file_url,headers=file_headers)
       print(response.url,'请求的附件链接')
       if response.content:
           file_path = file_path_head + file_name + houzhui
           with open(file_path, 'wb') as f:
               f.write(response.content)
               print('附件:{}下载成功'.format(file_name))
    except:
        print('附件下载失败{}'.format(file_name))

def return_fujian(old_name):
    my_pattern = '\.[^.\\/:*?"<>|\r\n]+$'
    m = re.search(my_pattern,old_name).group()
    return m


if __name__ == '__main__':
    url = 'http://pub.gdepb.gov.cn/pub/pubcatalogwry/extranet_pub_documents_list_left.jsp?page=1&catalog=8132b393-0140-1000-e000-0001a9fe9b9d'
    message_url_head = 'http://pub.gdepb.gov.cn/pub/pubcatalogwry/extranet_pub_document_view.jsp'
    page_url_head = 'http://pub.gdepb.gov.cn/pub/pubcatalogwry/extranet_pub_documents_list_left.jsp'
    page = 1
    while page < 83:
        s = get_urls(page_url_head)
        for key,value in s.items():
            print(key,':',value,end='\n')
            message_dict['docId'] = key
            tag_a = find_files(message_url_head=message_url_head,message_dict=message_dict)
            if len(tag_a) == 1:
                # 获取文件下载链接，不需要处理
                file_url = tag_a[0]['href']
                print(file_url,'找到的附件链接')
                houzhui = return_fujian(file_url)
                get_file(file_url,value,houzhui)
            elif len(tag_a) > 1:
                print('docId为{}的页面下载文件多于一个'.format(key))
            sleep(3)
        updata_data_dict()
        page += 1

    # message_url1 = 'http://pub.gdepb.gov.cn/pub/pubcatalogwry/extranet_pub_document_view.jsp?docId=235016&kwStr='
    # def one_url():
    #     response = requests.get(message_url1)
    #     soup = BeautifulSoup(response.content, 'lxml')
    #     # 附件链接
    #     files_tag = soup.find_all('a',href=re.compile("(xls|xlsx|doc|docx|pdf|rar)$"))
    #     # files_tag = soup.find_all('a', text='点击查看文件')
    #     return files_tag
    # print(one_url()[0]['href'])