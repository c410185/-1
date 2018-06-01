import datetime
import xlwings as xw

i = datetime.datetime.now()

print('%s/%s/%s %s:00:00' % (i.year,i.month,i.day,i.hour))
m = '%s/%s/%s %s:00:00' % (i.year,i.month,i.day,i.hour)
print(m)
file = 'D:\IPE_download\jdxjc\excel处理\浙江-text\\xls\\0已导入\测试火电厂数据.xlsx'
wb = xw.Book(file)
sht = wb.sheets[0]
sht[4,4].value = m
print(sht[4,4].value)