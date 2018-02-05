#encoding=utf-8
import requests
import re
import pdfkit

# 设置请求头,后期考虑多请求头自动切换
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}
# 设置wkhtmltopdf的位置，
config = pdfkit.configuration(wkhtmltopdf="C:\Program Files\wkhtmltopdf\\bin\wkhtmltopdf.exe")
com_url_head = 'http://permit.mep.gov.cn/permitExt/xkgkAction!xkgk.action?xkgk=getxxgkContent&dataid='
fb_url_head = 'http://permit.mep.gov.cn/permitExt/syssb/wysb/hpsp/hpsp-company-sewage!showImage.action?dataid='
zb_url_head = 'http://permit.mep.gov.cn/permitExt/upanddown.do?method=download&ewmfile=fbfile&datafileid='
def get_com_name():
    # 如果从数据库获得公司名称的话，此函数的含义会发生变化。

    pass
