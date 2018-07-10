#encoding=utf-8
import xlwings as xw
import json
from multiprocessing import Process
from time import clock
import datetime

'''
增加城市，修改是否达标为是否超标
其他目标
1.自动取消合并单元格
2.增加列，修改列的顺序----必须要做出来
3.增加平台信息，固定值--完成
4.增加污染源类型，固定值--完成，但是并不能保证污染源正确
5.增加录入时间--完成
6.修改城镇表来对应数据表中的特例，其中绍兴‘高新区’可能会有重名，对于这种需要在其他省份去掉
1.污水处理厂
2.废水
3.废气
4.重金属废气
5.重金属废水
6.危废废气
7.危废废水
8.规模养殖场
9.30KW以上火力发电厂
10.其他
'''

template = ['省', '行政区（市）', '行政区', '企业名称', '监测点名称', '执行标准名称', '执行标准条件名称', '监测日期', '录入时间', '工况负荷（%）', '流量（m3/h)', '烟气温度(℃)', '含氧量(%)', '监测项目名称', '实测浓度(mg/m3)', '折算浓度(mg/m3)', '标准限值(mg/m3)', '排放单位', '是否超标', '超标倍数', '受纳水体', '备注', '污染源类型']
suo = ['行政区', '企业名称', '行业名称', '受纳水体', '监测点名称', '执行标准名称', '执行标准条件名称', '监测日期', '生产负荷(%)', '监测点流量(吨/天)', '监测项目名称', '污染物浓度', '标准限值', '单位', '是否达标', '超标倍数', '备注']

myChr = 'ABCDEFGHIJKLMNOPQRSTUVWX'
# range 的index方式仍不明确
# county = sht.range('A2:T204')
# 插入行操作暂缓
# def insert():
#     sht[2,:].api.InsertAfter()
class Doexcel(object):
    def __init__(self,file_path):
        self.file_path = file_path
        self.wb = xw.Book(self.file_path)
        self.sht = self.wb.sheets[0]
        self.max_row = self.sht.api.UsedRange.Rows.count
        self.max_col = self.sht.api.UsedRange.Columns.count
        self.title = self.sht.range('A1').expand('right').value
        t = datetime.datetime.now()
        self.time = '%s/%s/%s %s:00:00' % (t.year,t.month,t.day,t.hour)

    def save(self):
        self.wb.save()

    def get_citys(self,province):
        city_path = 'D:\何方辉\全国省市数量统计分类\pcas.json'
        with open(city_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            one_province = data[province]
            return one_province

    def new_title(self):
        """
        获取标题行，一个list，并且根据模板处理好格式，插入空行和删除等
        返回处理好的列表，后续函数读取到的是处理后的列表，
        感觉还是有很多特例，先写死
        """
        self.title = self.sht.range('A1').expand('right').value
        return self.title

    def insert(self):
        rng = self.sht.range('A1').expand('down')
        rng.api.Insert()
        rng.api.Insert()
        # print(self.title,'未刷新')
        self.sht[0,0].value = '省'
        self.sht[0,1].value = '市'
        self.title = self.new_title()
        #插入空列后，使用expand方法就无法获取到空格加有数据的行，使用手动控制，每次计算偏移量
        # A ASCII --65，C:67，
        for index,item in enumerate(self.title):
            if item == '监测日期':
                self.sign_insert(index, '录入时间')
            elif '监测项目' in item:
                if '烟气温度(℃)' not in self.title:
                    # 似乎需要改为+1.现在的插入位置并不在监测项目之前，而是差了一个位置
                    self.sign_insert(index,'烟气温度(℃)')
                    self.sign_insert(index + 1,'含氧量(%)')
            elif item == '备注':
                self.sign_insert(index,'受纳水体')

    def sign_insert(self,index,str):
        input_loc = chr(65 + index + 1)
        rng = self.sht.range('{}1'.format(input_loc), '{0}{1}'.format(input_loc, self.max_row))
        rng.api.Insert()
        self.sht.range('{}1'.format(input_loc)).value = str

    def add_else(self):
        self.title = self.new_title()
        # print(self.title)
        old = len(self.title)
        if self.sht[0,old].value is None:
            self.sht[0, old].value = '污染源类型'

    def insert_data(self,begin,end,str='废水'):
        # self.title = self.new_title()
        self.title = self.new_title()
        sheng = self.title.index('省')
        shi = self.title.index('市')
        qu = self.title.index('行政区')
        input_time = self.title.index('录入时间')
        waste_type = self.title.index('污染源类型')
        one_province = self.get_citys('浙江省')
        global dabiao
        dabiao = ''
        if '是否达标' in self.title:
            dabiao = self.title.index('是否达标')
            self.sht[0,dabiao].value = '是否超标'
        elif '是否超标' in self.title:
            dabiao = self.title.index('是否超标')

        for i in range(begin, end):
            self.sht[i, sheng].value = '监督性监测浙江导入'
            self.sht[i, waste_type].value = str
            self.sht[i, input_time].value = self.time
            if dabiao:
                self.sht[i, dabiao].value = true_to_flase(self.sht[i, dabiao].value)
            m = self.sht[i, qu].value
            for k, v in one_province.items():
                if m in v:
                    self.sht[i, shi].value = k
                    if self.sht[i, shi - 1].value is None:
                        print(m, ':第{}行区县不在行政区中'.format(i))

    def change_flow(self,begin,end):
        self.title = self.new_title()
        for index, item in enumerate(self.title):
            if '流量' and '吨' in item:
                self.sht[0,index].value = '监测点流量(吨/小时)'
                for i in range(begin,end):
                    try:
                        if self.sht[i, index].value is not "":
                            self.sht[i, index].value = str(float(self.sht[i, index].value) / 24)
                        else:
                            pass
                    except:
                        print('流量第{}行出错'.format(i + 1))

            elif '流量' and '小时' in item:
                for i in range(begin,end):
                    try:
                        if self.sht[i, index].value is not '':
                            self.sht[i, index].value = str(float(self.sht[i, index].value) / 24)
                        else:
                            pass
                    except:
                        print('第{}行出错'.format(i + 1))
            # if内嵌在for循环中，对title中的每一个元素进行了判断，所以会有多个else出现
            else:
                print('未找到流量/小时字段')

    def change_yesno(self,begin,end):
        self.title = self.new_title()
        if '是否达标' in self.title:
            dabia = self.title.index('是否达标')
            self.sht[0,dabia].value = '是否超标'
        for i in range(begin, end):
            self.sht[i, 18].value = true_to_flase(self.sht[i, 18].value)

    def run(self):
        begin = 1
        end  = self.max_row
        print('最大行数：{}'.format(end))
        # self.insert()
        # self.add_else()
        self.insert_data(begin,end,str='30KW以上火力发电厂')
        self.change_flow(begin,end)
        # self.change_yesno(begin,end)

    def get_null(self):
        # 判断excel的空单元格的值，并不是None，也不是Null，而是‘’,不懂
        print(self.sht[337,14].value)
        if self.sht[337,14].value is not '':
            print('不为空')

# 将是否达标改为是否超标
def true_to_flase(val):
    if val == '是':
        return '否'
    elif val == '否':
        return '是'
    else:
        return val

def text():
    m = '是'
    n = '否'
    l = ''
    k = 'fsfsdf'
    assert true_to_flase(m) == '否'
    assert true_to_flase(n) == '是'
    assert true_to_flase(l) == ''
    assert true_to_flase(k) == k

def runclass(file):
    clock()
    zj = Doexcel(file)
    zj.run()
    print(clock())

def my_process():
    file_path1 = r'D:\IPE_download\jdxjc\excel处理\浙江-text\\xls\\xls8.xls'
    file_path2 = r'D:\IPE_download\jdxjc\excel处理\浙江-text\\xls\\xls附表3  2016年第2季度污水厂监测数据.xls'
    file_path3 = r'D:\IPE_download\jdxjc\excel处理\浙江-text\\xls\\xls附表3  2016年第3季度污水处理厂监督性监测数据.xls'

    clock()

    p1 = Process(target=runclass,args=(file_path1,))
    p2 = Process(target=runclass,args=(file_path2,))
    p3 = Process(target=runclass,args=(file_path3,))
    # zj.get_null()
    p1.start()
    p2.start()
    p3.start()
    p1.join()
    p2.join()
    p3.join()
    print(clock())

class Sewage_plant(Doexcel):
    pass


if __name__ == '__main__':
    file_path1 = r'D:\IPE_download\jdxjc\excel处理\浙江-text\\xls\\xls浙江省2016年第4季度30万千瓦以上火电厂废气监测数据.xls'
    runclass(file_path1)
    # my_process()
    # zj = Doexcel(file_path1)
    # zj.insert_data(1,zj.max_row,str='废气')
    # zj.change_flow(1,zj.max_row)
