import requests

zb_url_head = 'http://permit.mep.gov.cn/permitExt/upanddown.do?method=download&ewmfile=fbfile&datafileid='
ss = 'http://permit.mep.gov.cn/permitExt/upanddown.do?method=download&ewmfile=fbfile&datafileid=e2c36d39cadb4a1d8ab38e76eb347d36'
s2 = 'http://permit.mep.gov.cn/permitExt/upanddown.do?method=download&ewmfile=fbfile&datafileid=630c91b3b6e94d4ca08d35f716094116'
dataid ='453727f1cd534cfc93f9d3cefb6f7b61'
# 正本的ID不是dataid，而是新的datafileid，所以要重新获取

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}

zb_url = zb_url_head + dataid
# print(zb_url)
# 不清楚是否请求头问题，需要查询
def get_zb_pdf(url):
    response = requests.get(url,headers=headers)
    print(response.url)
    with open('D:\何方辉\排污许可\download\晋江市永和晋发线带有限公司1.pdf','wb') as f:
        f.write(response.content)

if __name__ == '__main__':
    get_zb_pdf(zb_url)

s = 'http://permit.mep.gov.cn/permitExt/upanddown.do?method=download&ewmfile=fbfile&datafileid=03dac3b634f54d8e95070100ae829a28'
b = 'http://permit.mep.gov.cn/permitExt/syssb/wysb/hpsp/hpsp-company-sewage!showImage.action?dataid=453727f1cd534cfc93f9d3cefb6f7b61'