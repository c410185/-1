import requests

proxies = {
  "http": "http://139.129.166.68:3128",
    "https": "http:/61.4.184.180:3128",
}
# 试了几个，都不能用
url = 'http://113.57.151.5:8030/HBHB/companyInfo.action?businessName=&qylx=00&color=0&nextPage=1&sz=000000&qx=000000'
url1 = 'http://www.hnep.gov.cn:81/xycx.aspx'
url2 = 'https://www.baidu.com/'
try:
    requests.get(url2,proxies=proxies)
except:
    print('no')
else:
    print('done!')