# -*- coding: utf-8 -*-
# Created by IPE_he on 3/28

import re
from bs4 import BeautifulSoup
from mytools import buildfilepath
import requests
import sqlite3

def open_file(filename):
    with open(filename,'r',encoding='utf-8') as f:
        m =f.read()
    return m

jbxx_head = 'http://58.30.229.134/monitor-pub/org_jbxx/'
jcfa_head = 'http://58.30.229.134/monitor-pub/org_jcfa/'
zdjc_head = 'http://58.30.229.134/monitor-pub/org_zdjc/'
sdjc = 'http://58.30.229.134/monitor-pub/org_sdjc/'
wjcyy = 'http://58.30.229.134/monitor-pub/org_wjcyy/'
ndbg = 'http://58.30.229.134/monitor-pub/org_ndbg/'
hbxzxk = 'http://58.30.229.134/monitor-pub/org_hbxzxk/'
hjyjya = 'http://58.30.229.134/monitor-pub/org_hjyjya/'

def jichuxinxi(html):
    r = open_file(html)
    soup = BeautifulSoup(r,'lxml')
    jichu = soup.find('table',class_='tb_dotline')
    tds = jichu.find_all('td')
    # 信息存在可能为空的情况
    Name = tds[1].text.strip()
    # EnName
    # ShortName
    Address = tds[7].text.strip()
    # AddTime
    Lat = tds[9].text.strip()
    Lng = tds[11].text.strip()
    #SpaceId  地区外键，北京
    #AreaId 区县id，没有
    Code = tds[5].text.strip()
    #UnifiedSocietyCreditCode 统一社会信用代码
    #PlatFormId 平台ID
    法人 = tds[13].text.strip()
    联系人 = tds[17].text.strip()
    联系电话 = tds[19].text.strip()
    投运时间 = tds[21].text.strip()
    所属行业 = tds[15].text.strip()
    主要产品 = tds[31].text.strip()
    主要生产工艺 = tds[33].text.strip()
    生产周期 = tds[37].text.strip()
    污染源类型 = tds[3].text.strip()
    # 管理级别
    排放污染物名称 = tds[29].text.strip()
    自动监测运维方式 = re.sub(r'\n|\t','',tds[25].text)
    # 第三方运行公司
    自行监测方式 = re.sub(r'\n|\t','',tds[23].text)
    手工监测方式 = re.sub(r'\n|\t','',tds[27].text)
    治理设施 = tds[35].text.strip()
    # 排放去向
    # 排放方式
    企业官网对外信息公开网址 = tds[39].text.strip()
    # PersonId 录入人


def jiancefangan(html):
    r = open_file(html)
    soup = BeautifulSoup(r, 'lxml')
    company = soup.find('div',class_='com_tit_new f_22 clr_3').text
    table = soup.find('table',class_='tb_ls')
    pdf_urls = table.find_all('a')
    for url in pdf_urls:
        print(url['href'],url.text)
        download_pdf(url=url['href'],filename=url.text,company=company)


def download_pdf(url,filename,company,path=r'D:\IPE_download\历史监测数据\北京'):
    download_url = 'http://58.30.229.134' + url
    # 检测并创建公司目录
    file_path = path + '\\' + company
    # 可能有文件名字重复问题
    download_name = file_path + '\\' +filename + '.pdf'
    buildfilepath.path_exist(file_path)
    try:
        r = requests.get(download_url)
        with open(download_name, 'wb') as f:
            f.write(r.content)
    except Exception as e:
        print(e)

def zidongjiance(url,time):
    # 如何存储---按公司名称创建一个表并存入数据sqlite3
    headers = {
        'User-Agent':'后期做随机选择'
    }
    data = {
        'startTime':time,  #格式：2018-03-29
        'pageIndex':'1'
    }
    # 获取第一页，获得pageIndex信息,因为已经获取了，所以数据一并取出，页面也不再循环
    r = requests.post(url,data=data)
    # r = open_file('自动监测数据.html')
    # soup = BeautifulSoup(r, 'lxml')
    max_page = re.search('1/([0-9]*)页',r.text).group(1)

    序号, 监测点位, 监测时间, 监测项目, 监测结果, 标准限值, 单位, 是否达标, 超标倍数, 评价标准, 排放去向, 排放方式, 备注 = _jianceshuju(r.text)
        # 1,1号烟气排口,2018-03-29 23:00:00,二氧化硫,一,50,mg/m3,是,,锅炉大气污染物排放标准(DB11/139-2015),排入环境空气,集中排放,
    if int(max_page) > 1:
        for i in range(2,int(max_page)+1):
            headers = {
                'User-Agent': '后期做随机选择'
            }
            data = {
                'startTime': time,  # 格式：2018-03-29
                'pageIndex': str(i)
            }
            r = requests.post(url, data=data)
            序号, 监测点位, 监测时间, 监测项目, 监测结果, 标准限值, 单位, 是否达标, 超标倍数, 评价标准, 排放去向, 排放方式, 备注 = _jianceshuju(r.text)


def _jianceshuju(html):
    soup = BeautifulSoup(html, 'lxml')
    table = soup.find('table',class_='tb_ls')
    trs = table.find_all('tr')
    for tr in trs[1:]:
        tds = tr.find_all('td')
        序号 = tds[0].text
        监测点位 = tds[1]['title']
        监测时间 = tds[2].text
        监测项目 = tds[3]['title']
        监测结果 = re.sub(r'[\n\t\s]','',tds[4].text)
        标准限值 = re.sub(r'[\n\t\s]','',tds[5].text)
        单位 = tds[6].text
        是否达标 = re.sub(r'[\n\t]','',tds[7].text)
        超标倍数 = re.sub(r'[\n\t]','',tds[8].text)
        评价标准 = tds[9]['title']
        排放去向 = tds[10]['title']
        排放方式 = tds[11]['title']
        备注 = tds[12]['title']
    return (序号,监测点位,监测时间,监测项目,监测结果,标准限值,单位,是否达标,超标倍数,评价标准,排放去向,排放方式,备注)
# 手工监测数据 分日，周,月，季度，年,关注按月，季度和年的数据，主要是月和季度

def _tingchantable(html):
    r = open_file(html)
    soup = BeautifulSoup(r, 'lxml')
    max_page = re.search('1/([0-9]*)页', r).group(1)
    table = soup.find('table', class_='tb_ls')
    trs = table.find_all('tr')
    for tr in trs[1:]:
        tds = tr.find_all('td')
        序号 = tds[0].text
        类别 = tds[1].text
        监测点位 = tds[2].text
        停产原因 = tds[3].text
        开始时间 = tds[4].text
        结束时间 = tds[5].text
        附件名 = re.sub(r'[\n\t\s]', '', tds[6].text)
        if 附件名 != '':
            附件链接 = tds[6].a.get('href')
        else:
            附件链接 = ''

        print(序号,类别,监测点位,停产原因,开始时间,结束时间,附件名,附件链接,sep=',')
    return (序号,类别,监测点位,停产原因,开始时间,结束时间,附件名,附件链接)

def _tablelist(html):
    r = open_file(html)
    soup = BeautifulSoup(r, 'lxml')
    max_page = re.search('1/([0-9]*)页', r).group(1)
    table = soup.find('table', class_='tb_ls')
    trs = table.find_all('tr')
    name_list = []
    name_ths = trs[0].find_all('th')
    len_name = len(name_ths)
    for th in name_ths:
        name_list.append(th.text)
    print(name_list)
    for tr in trs[1:]:
        tds = tr.find_all('td')
        序号 = tds[0].text
        报告名称 = tds[1].text
        创建时间 = tds[2].text
        if 报告名称 != '':
            报告链接 = tds[2].a.get('href')
        else:
            报告链接 = ''

        print(序号, 报告名称,报告链接, sep=',')
    return (序号, 报告名称,报告链接)

def niandubaogao(url):
    r = requests.get(url)
    # r = open_file('自动监测数据.html')
    # soup = BeautifulSoup(r, 'lxml')
    # max_page = re.search('1/([0-9]*)页', r.text).group(1)
    序号, 报告名称, 报告链接 = _tablelist(r.text)

def weijiance(url):
    # 如何存储---按公司名称创建一个表并存入数据sqlite3
    headers = {
        'User-Agent':'后期做随机选择'
    }

    # 获取第一页，获得pageIndex信息,因为已经获取了，所以数据一并取出，页面也不再循环
    r = requests.get(url)
    # r = open_file('自动监测数据.html')
    # soup = BeautifulSoup(r, 'lxml')
    max_page = re.search('1/([0-9]*)页',r.text).group(1)
    序号, 类别, 监测点位, 停产原因, 开始时间, 结束时间, 附件名, 附件链接 = _tingchantable(r.text)
        # 1,1号烟气排口,2018-03-29 23:00:00,二氧化硫,一,50,mg/m3,是,,锅炉大气污染物排放标准(DB11/139-2015),排入环境空气,集中排放,
    if int(max_page) > 1:
        for i in range(2,int(max_page)+1):
            headers = {
                'User-Agent': '后期做随机选择'
            }
            r = requests.get(url)
            序号, 类别, 监测点位, 停产原因, 开始时间, 结束时间, 附件名, 附件链接 = _tingchantable(r.text)

class savedate():
    def __init__(self):
        self.db = sqlite3.connect('beijing_history_data.db')



if __name__ == '__main__':
    html = '停产.html'
    # jichuxinxi(html)
    # print(html.replace('\n|\t',''))
    # m = re.sub('\n|\t','',html)
    # print(m)
    # fangan = '监测方案.html'
    # jiancefangan(fangan)
    # zidongjiance()
    url = 'http://58.30.229.134/monitor-pub/org_zdjc/f982e493-f5f1-44fc-8f00-ed19b2809cef.do'
    time = '2018-01-01'
    zidongjiance(url,time)
