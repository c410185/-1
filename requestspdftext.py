import requests

zb_url_head = 'http://permit.mep.gov.cn/permitExt/upanddown.do?method=download&ewmfile=fbfile&datafileid='

dataid ='8cd9f334f98e444d86fdec5aac2afff6'
zb_url = zb_url_head + dataid

response = requests.get(zb_url)
with open('D:\何方辉\排污许可\download\东莞市金田纸业有限公司-排污许可证正本.pdf','wb') as f:
    f.write(response.content)