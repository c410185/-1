from urllib.request import urlopen
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
import re

num = 1
n = 2118
page_url_head = 'http://permit.mep.gov.cn/permitExt/outside/Publicity?pageno='
page_url = page_url_head + str(num)

html = urlopen(page_url)
bs0bj = BeautifulSoup(html,'lxml')

# 使用正则匹配dataID后的32位数字
com_list = bs0bj.find_all(re.match(r'[a-z0-9]{32}'))
print(com_list)
