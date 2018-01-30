from urllib.request import urlopen
from urllib.request import Request
from urllib.request import urlretrieve
import pdfkit
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
import lxml

# 设置请求头,后期考虑多请求头自动切换
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}
config = pdfkit.configuration(wkhtmltopdf="C:\Program Files\wkhtmltopdf\\bin\wkhtmltopdf.exe")

# 如果在前一页获得了dataid，那么这一步就不需要获取链接，只需要获取公司名作为验证手段即可
def getben_url(url,headers):
    request = Request(url=url,headers=headers)
    try:
        html = urlopen(request)
        bs0bj = BeautifulSoup(html, 'lxml')
        # 获得证件所在元素
        zhengben = bs0bj.find('a', text='排污许可证正本')
        fuben = bs0bj.find('a', text='排污许可证副本')
        # 获得证件链接
        zb_url = 'http://permit.mep.gov.cn' + zhengben.get('href')
        fb_url = 'http://permit.mep.gov.cn' + fuben.get('href')
        # 获得公司名称，写死的方法
        com_name = bs0bj.find('p').text
        return zb_url, fb_url, com_name
    except URLError as e:
        print(e.reason)

def download_ben(url,headers,download_path):
    zb_url, fb_url, com_name = getben_url(url,headers)
    # 下载许可证,指定下载位置
    zb_local = download_path + com_name + '-排污许可证正本.pdf'
    fb_local = download_path + com_name + '-排污许可证副本.pdf'
    #fb_local = download_path + com_name + '-排污许可证副本.html'

    try:
        urlretrieve(zb_url, zb_local)
        # 只会下载HTML，不能下载其中的图片,所以暂时不用这个方法
        #urlretrieve(fb_url, fb_local)
        pdfkit.from_url(fb_local, fb_local, configuration=config)
    except:
        print('出错了')

if __name__ == '__main__':
    download_text = 'D:\何方辉\排污许可\download\\'
    com_url = 'http://permit.mep.gov.cn/permitExt/xkgkAction!xkgk.action?xkgk=getxxgkContent&dataid=f2cd1a346f1643d283580ad54445cfb3'

    download_ben(com_url,headers,download_text)