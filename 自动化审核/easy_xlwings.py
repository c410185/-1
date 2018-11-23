# encoding=utf-8
import xlwings as xw
from xlwings.constants import DeleteShiftDirection
from time import time
import os
import re
from time import sleep

def get_filenames(dir):
    files = []
    for file in os.listdir(dir):
        file_path = os.path.join(dir, file)
        if os.path.isdir(file_path):
            pass
        else:
            files.append(file_path)
    return files

def run_one(file):
    start = time()
    zj = Doexcel(file)
    zj.format_name()
    zj.format_urls()
    end = time()
    print(file,end - start)

class Doexcel(object):
    def __init__(self,file_path):
        self.file_path = file_path
        self.wb = xw.Book(self.file_path)
        self.sht = self.wb.sheets[0]
        self.max_row = self.sht.api.UsedRange.Rows.count
        self.max_col = self.sht.api.UsedRange.Columns.count
        self.title = self.sht.range('A1').expand('right').value
        self.classify_values = [['其他'] for i in range(self.max_row - 1)]
        # t = datetime.datetime.now()
        # 预先生成一个信息分类列表，之后根据关键词修改对应的分类
        # self.time = '%s/%s/%s %s:00:00' % (t.year,t.month,t.day,t.hour)

    def save(self):
        self.wb.save()

    def format_name(self):
        # 删除名称中的空白符和信用查询等无效信息
        names = self.sht.range('J2:J{}'.format(self.max_row))
        n = []
        m = names.value
        for name in m:
            name = ''.join(name.split())
            name = name.replace('信用查询', '')
            n.append(name)
        s = [[i] for i in n]
        self._write_data('J',s)

    def _write_data(self,col,value):
        p = self.sht.range('{0}2:{0}{1}'.format(col,self.max_row))
        p.value = value

    def format_urls(self):
        contents = self.sht.range('E2:E{}'.format(self.max_row))
        m = contents.value
        n = []
        pattern_img = re.compile(r'<img src="/images/clocicon.png"/>')
        pattern_cf = re.compile(r'<a href="/qygs/xzcf_list.html">行可处罚 </a>/')
        pattern_xy = re.compile(r'<a href=.*>信用查询</a>')
        pattern_sy = re.compile(r'<a href="/index.html">首页</a> /')
        for s in m:
            s = re.sub(pattern_img, '', s)
            s = re.sub(pattern_cf, '', s)
            s = re.sub(pattern_sy, '', s)
            s = re.sub(pattern_xy, '', s)
            s = ' '.join(s.split())
            n.append([s])
        self._write_data('E',n)

    def del_html(self,patterns):
        """
        输入想要删除HTML的正则表达式，多组表达式用管道符|链接 然后删除
        :param patterns: list
        :return: html list
        """
        contents = self.sht.range('E2:E{}'.format(self.max_row))
        m = contents.value
        n = []
        re_pattern = re.compile(patterns)
        for s in m:
            s = re.sub(re_pattern,'',s)
            n.append([s])
        self._write_data('E', n)

    def get_html(self,patterns):
        contents = self.sht.range('E2:E{}'.format(self.max_row))
        m = contents.value
        n = []
        re_pattern = re.compile(patterns)
        for s in m:
            s = re.search(re_pattern,s).group()
            n.append([s])
        self._write_data('E', n)

    def give_citys(self,city):
        citys = [[city] for i in range(self.max_row - 1)]
        self.sht.range('K2').value = citys

    def key_classify(self,col:str,keys:tuple,ipe_classify:str):
        """
        col:关键词所在行，key：关键词
        根据关键词在字符串中返回分类，修改信息分类
        :return: 信息分类多维列表
        """
        p = self.sht.range('{0}2:{0}{1}'.format(col, self.max_row)).value
        for key in keys:
            for i, element in enumerate(p):
                if key in element:
                    self.classify_values[i][0] = ipe_classify
        self.sht.range('O2').value = self.classify_values

    def clear_humen(self):
        c = self.sht.range('J2:J{}'.format(self.max_row)).value
        for i, element in enumerate(c):
            if element == None:
                print('第 %d 行的数据是空' % (int(i)+ 2))
            elif len(element) <= 3:
                print('第 %d 行的数据是人名' % (int(i)+ 2))
                # 先假设Rows是从1开始计数的，这里的c是从第二行2开始从0开始计数
                # 所以中间差了2
                # .xl_range.Delete()
                # 使用win32 api，删除，并指定数据填充的方向。这里删除整行，所以数据剩余数据向上移动
                # 删除行之后 行数会发生变化，导致之后的删除会不准，所以clear会更安全？
                self.sht.range('{0}:{0}'.format(i + 2)).clear()
            elif '*' in element:
                print('第 %d 行的数据包含*号' % (int(i)+ 2))
                self.sht.range('{0}:{0}'.format(i + 2)).clear()

    def del_None(self,col:str):
        self.max_row = self.sht.api.UsedRange.Rows.count
        print('最大行数',self.max_row)
        c = self.sht.range('{0}2:{0}{1}'.format(col,self.max_row)).value
        global num
        for i, element in enumerate(c):
            if element == None:
                num = self._return_none(col,i)
                if num == -1:
                    break
                else:
                    self.sht.range('{0}:{1}'.format(i + 2,i+2+num)).api.Delete(DeleteShiftDirection.xlShiftUp)
                    self.del_None(col)
            # elif i == self.max_row - num:
            #     break

    def _return_none(self,col:str,begin:int):
        c = self.sht.range('{0}2:{0}{1}'.format(col,self.max_row)).value
        if None in c:
            for i, element in enumerate(c[begin:]):
                if element != None:
                    print('切片后的', i)
                    return i - 1
        else:
            print('没有空行',begin)
            return -1


        # b = self.sht.range('J2:J{}'.format(self.max_row)).value
        # 不能使用循环一次删除所有空行，因为删除之后行数就会发生变化，所以会造成有些空行被跳过了
        # for i, element in enumerate(b):
        #     if element == None:
        #         print('清空后第 %d 行的数据呗删除' % (int(i)+ 2))
        #         self.sht.range('{0}:{0}'.format(i + 2)).api.Delete(DeleteShiftDirection.xlShiftUp)

    def self_test(self):
        c = self.sht.range('J2:J{}'.format(self.max_row)).value
        for i in c:
            if i == None:
                print('单位名称有空')
        govs = self.sht.range('N2:N{}'.format(self.max_row)).value
        for gov in govs:
            if ('水利' in gov) or ('水务' in gov):
                print('水利水务出现了')
                # 经济与信息化委员会，使用经济的话，会匹配经济开发区
            elif ('发展' in gov) or ('信息' in gov):
                print('发改委经信委出现了')

    # 	wb.sheets("Page1_1").Rows(1).Delete
    #   删除函数，需要仔细研究