import requests

zb_url_head = 'http://permit.mep.gov.cn/permitExt/upanddown.do?method=download&ewmfile=fbfile&datafileid='
ss = 'http://permit.mep.gov.cn/permitExt/upanddown.do?method=download&ewmfile=fbfile&datafileid=e2c36d39cadb4a1d8ab38e76eb347d36'
s2 = 'http://permit.mep.gov.cn/permitExt/upanddown.do?method=download&ewmfile=fbfile&datafileid=630c91b3b6e94d4ca08d35f716094116'
dataid ='3ecd6806348a4d0a8522ee51e29fb7e2'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}

zb_url = zb_url_head + dataid
# print(zb_url)
# 不清楚是否请求头问题，需要查询
def get_zb_pdf(url):
    response = requests.get(url,headers=headers)
    with open('D:\何方辉\排污许可\download\安徽轶轩表面处理技术有限公司-排污许可证正本2.pdf','wb') as f:
        f.write(response.content)


if __name__ == '__main__':
    get_zb_pdf(zb_url)