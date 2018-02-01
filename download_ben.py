from urllib.request import urlopen
from urllib.request import Request
from urllib.request import urlretrieve
import pdfkit
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
from pySQLtext import get_dataid

# 设置请求头,后期考虑多请求头自动切换
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}
config = pdfkit.configuration(wkhtmltopdf="C:\Program Files\wkhtmltopdf\\bin\wkhtmltopdf.exe")

# 如果在前一页获得了dataid，那么这一步就不需要获取链接，
# 希望获取公司名作为验证手段和文件存储的信息，所以还是要解析详情页


def get_com_name(dataid,headers):
    com_url_head = 'http://permit.mep.gov.cn/permitExt/xkgkAction!xkgk.action?xkgk=getxxgkContent&dataid='
    url = com_url_head + dataid
    request = Request(url=url,headers=headers)
    try:
        html = urlopen(request)
        bs0bj = BeautifulSoup(html, 'lxml')
        com_name = bs0bj.find('p').text
        return com_name
    except URLError as e:
        print(e.reason)

def download_ben(dataid,headers,download_path):

    com_name = get_com_name(dataid,headers)
    # 下载许可证,指定下载位置
    fb_url_head = 'http://permit.mep.gov.cn/permitExt/syssb/wysb/hpsp/hpsp-company-sewage!showImage.action?dataid='
    zb_url_head = 'http://permit.mep.gov.cn/permitExt/upanddown.do?method=download&ewmfile=fbfile&datafileid='
    zb_url = zb_url_head + dataid
    fb_url = fb_url_head + dataid
    zb_local = download_path + com_name + '-排污许可证正本.pdf'
    fb_local = download_path + com_name + '-排污许可证副本.pdf'
    #fb_local = download_path + com_name + '-排污许可证副本.html'

    try:
        urlretrieve(zb_url, zb_local)
        # 只会下载HTML，不能下载其中的图片,所以暂时不用这个方法
        #urlretrieve(fb_url, fb_local)
        pdfkit.from_url(fb_url, fb_local, configuration=config)
    except:
        print('出错了')

if __name__ == '__main__':
    download_text = 'D:\何方辉\排污许可\download\\'
    com_url_head = 'http://permit.mep.gov.cn/permitExt/xkgkAction!xkgk.action?xkgk=getxxgkContent&dataid='
    dataid_list = get_dataid()
    for i in dataid_list:
        download_ben(i,headers,download_text)