from urllib.request import urlopen
from urllib.request import Request
from urllib.request import urlretrieve
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
import re
import csv
from time import clock
from time import sleep
file_path = 'D:\paiwuxuke\dataidlist.csv'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}

def getdataid(m=1,n=5):
    request_list = range(m,n + 1)
    for i in request_list:
        page = 'http://permit.mep.gov.cn/permitExt/outside/Publicity?pageno=' + str(i)
        request = Request(url=page,headers=headers)
        html = urlopen(request).read()
        dataid_list2 = re.findall('[a-z0-9]{32}',str(html))
        with open(file_path,'a',newline='') as f1:
            for k in range(10):
                f1.writelines(dataid_list2[k] + '\n')
        print('请求第%s个页面完成' % i)
        sleep(2)
def opencsv():
    with open(file_path,'r') as f1:
        reader = csv.reader(f1)
        for item in reader:
            print(item, end='\n')

if __name__ == '__main__':
    #1237页面无法访问
    getdataid(1238,2121)