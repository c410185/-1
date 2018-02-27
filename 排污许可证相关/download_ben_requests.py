#encoding=utf-8
import requests
import re
import pdfkit
from bs4 import BeautifulSoup


# 设置请求头,后期考虑多请求头自动切换
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}

# 设置wkhtmltopdf的位置，
config = pdfkit.configuration(wkhtmltopdf="C:\Program Files\wkhtmltopdf\\bin\wkhtmltopdf.exe")
options = {
    # 设置PDF的质量，因为都为图片，所以其他格式不做设置
    # 参考来自https://www.jianshu.com/p/4d65857ffe5e
    # 'image-quality':'40',
    'lowquality':'',
}

com_url_head = 'http://permit.mep.gov.cn/permitExt/xkgkAction!xkgk.action?xkgk=getxxgkContent&dataid='
fb_url_head = 'http://permit.mep.gov.cn/permitExt/syssb/wysb/hpsp/hpsp-company-sewage!showImage.action?dataid='
zb_url_head = 'http://permit.mep.gov.cn'

# 本意是想在请求一个公司许可证的详情页时，同时获得公司名称和正副本ID，只请求一次网址，不要重复请求，但是发现
# 水平有限，写出的类不管用。所以先搁置，修改自己的函数吧
class company(object):

    com_url_head = 'http://permit.mep.gov.cn/permitExt/xkgkAction!xkgk.action?xkgk=getxxgkContent&dataid='
    fb_url_head = 'http://permit.mep.gov.cn/permitExt/syssb/wysb/hpsp/hpsp-company-sewage!showImage.action?dataid='
    zb_url_head = 'http://permit.mep.gov.cn'

    def __init__(self,dataid):
        self.dataid = dataid

    def get_com_html(self,dataid):
        com_url = com_url_head + dataid
        response = requests.get(com_url)
        soup = BeautifulSoup(response.text, 'lxml')
        return soup

    def get_com_name(self,dataid):
        soup = self.get_com_html(dataid)
        com_name = soup.find('p').text
        return com_name

def get_com_name(dataid):
    # 如果从数据库获得公司名称的话，此函数的含义会发生变化。
    com_url = com_url_head + dataid
    response = requests.get(com_url)
    soup = BeautifulSoup(response.text,'lxml')
    com_name = soup.find('p').text
    return com_name

def get_zb_fileurl(dataid):
    com_url = com_url_head + dataid
    response = requests.get(com_url)
    soup = BeautifulSoup(response.text,'lxml')
    zb_fileid = soup.find('a',text='排污许可证正本')
    return zb_fileid['href']

def getNameAndFileid(dataid):
    com_url = com_url_head + dataid
    response = requests.get(com_url)
    soup = BeautifulSoup(response.text, 'lxml')
    com_name = soup.find('p').text
    zb_fileid = soup.find('a', text='排污许可证正本')
    return com_name,zb_fileid['href']

def get_zben(dataid):
    zb_url_tail = get_zb_fileurl(dataid)
    zb_url = zb_url_head + zb_url_tail
    try:
       response =  requests.get(zb_url)
       if response.text == '未找到对应文件！':
           print('出错了')
       else:
           return response.content
    except:
        print('正本链接无响应')

def write_zb(dataid,com_name,down_path='D:\何方辉\排污许可\download'):
    re_content = get_zben(dataid)
    assert len(re_content) > 200
    file_path = down_path +  '\\' +com_name + '-排污许可证正本.pdf'
    with open(file_path,'wb') as f:
        f.write(re_content)

def write_fb(dataid,com_name,down_path='D:\何方辉\排污许可\download'):
    fb_url = fb_url_head + dataid
    fb_local = down_path + '\\' + com_name + '-排污许可证副本.pdf'
    pdfkit.from_url(fb_url,fb_local, configuration=config,options=options)


if __name__ == '__main__':

    dataid = '453727f1cd534cfc93f9d3cefb6f7b61'
    dataid1 = '6d81f721277c48f6aa62b92f0233e48d'
    company_name = get_com_name(dataid1)
    # print(company_name)
    write_zb(dataid1, company_name)
    # write_fb(dataid,company_name)

