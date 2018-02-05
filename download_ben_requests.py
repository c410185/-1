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
    #'image-quality':'40',
    'lowquality':'',
}

com_url_head = 'http://permit.mep.gov.cn/permitExt/xkgkAction!xkgk.action?xkgk=getxxgkContent&dataid='
fb_url_head = 'http://permit.mep.gov.cn/permitExt/syssb/wysb/hpsp/hpsp-company-sewage!showImage.action?dataid='
zb_url_head = 'http://permit.mep.gov.cn/permitExt/upanddown.do?method=download&ewmfile=fbfile&datafileid='
te = 'http://permit.mep.gov.cn/permitExt/upanddown.do?method=download&ewmfile=fbfile&datafileid=e2c36d39cadb4a1d8ab38e76eb347d36'
def get_com_name(dataid):
    # 如果从数据库获得公司名称的话，此函数的含义会发生变化。
    com_url = com_url_head + dataid
    response = requests.get(com_url)
    soup = BeautifulSoup(response.text,'lxml')
    com_name = soup.find('p').text
    return com_name

def get_zben(dataid):
    zb_url = zb_url_head + dataid
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
    print(len(re_content))
    #assert len(re_content) > 200 and isinstance(com_name,str)
    file_path = down_path +  '\\' +com_name + '-排污许可证正本.pdf'
    with open(file_path,'wb') as f:
        f.write(re_content)

def write_fb(dataid,com_name,down_path='D:\何方辉\排污许可\download'):
    fb_url = fb_url_head + dataid
    fb_local = down_path + '\\' + com_name + '-排污许可证副本.pdf'
    pdfkit.from_url(fb_url,fb_local, configuration=config,options=options)


if __name__ == '__main__':

    dataid = '1c38b1548e2d41089e25335ec228f126'
    dataid1 = '6d81f721277c48f6aa62b92f0233e48d'
    company_name = get_com_name(dataid1)
    print(company_name)
    write_zb(dataid1, company_name)
    #write_fb(dataid,company_name)
