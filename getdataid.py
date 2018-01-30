from urllib.request import urlopen
from urllib.request import Request
from urllib.request import urlretrieve
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}

m = 10
page = 'http://permit.mep.gov.cn/permitExt/outside/Publicity?pageno=' + str(m)

request = Request(url=page,headers=headers)
html = urlopen(request).read()
# html <class 'http.client.HTTPResponse'>
# bs0bj = BeautifulSoup(html, 'lxml')

#dataid_list = bs0bj.find_all('a',{'href':re.compile('[a-z0-9]{32}$')})
#print(dataid_list,'bs4')
#html_source = urlopen(page).read()
dataid_list2 = re.findall('[a-z0-9]{32}',str(html))
