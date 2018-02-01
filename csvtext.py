import csv
import os
import time
from sys import getsizeof

list0 =['0a0a23ea4b214df5bef3f74df3525162', '5572771cf2f94fb99e4171570a76248c', '4d7f8c29a9184ec88ea3b3740696d0e1', '1782c9b53d8c4f42966b65a2e3e343bc', 'baabdacf716f4311ae6e10f97c6a0f88', 'f131e12838654132948dfce885ceba4d', '63c18722be8e47fcb7ade66bcac44854', 'e9f5192b17d245d78c3fcaf9dab8d97d', '22446ba7c1c84d949b694f35df49ab5b', 'c69c858db48b4bbb87df3bd0008c639c']


list = ['4d7f8c29a9184ec88ea3b3740696d0e1',
        '1782c9b53d8c4f42966b65a2e3e343bc',
        'baabdacf716f4311ae6e10f97c6a0f88',
        'e9f5192b17d245d78c3fcaf9dab8d97d',
        '39ec2d52ee504db69d351d4a66f83912',
        'ba030e025f3049cd9f0b134bae32b94b',
        'c43381de96d84e7c9d4f9de2b7fa4499',
        'ea372436c2034a22a3ec39089863147f',
        'c56b9835a30341fbb31729423d5d8b06',
        '3080e85941c3480bbb11aa5c20dd6e5c']
print(type(list[1]))
# csv_file = open('D:\paiwuxuke\dataidlist.csv', 'a',newline='')
# writer = csv_file
# writer.write("index","a_name","b_name")
# csv_file.close()
# time.sleep(1)
# csv_file.close()

list1 = [['3080e85941c3480bbb11aa5c20dd6e5c', '0'],
         ['4d7f8c29a9184ec88ea3b3740696d0e1', '0'],
         ['1782c9b53d8c4f42966b65a2e3e343bc', '0'],
         ['baabdacf716f4311ae6e10f97c6a0f88', '0'],
         ['e9f5192b17d245d78c3fcaf9dab8d97d', '0'],
         ['39ec2d52ee504db69d351d4a66f83912', '0'],
         ['ba030e025f3049cd9f0b134bae32b94b', '0'],
         ['c43381de96d84e7c9d4f9de2b7fa4499', '0'],
         ['ea372436c2034a22a3ec39089863147f', '0'],
         ['c56b9835a30341fbb31729423d5d8b06', '0']]

file_path = 'D:\paiwuxuke\dataidlist.csv'
print('写入前清空文件')
# 测试打开
csv_file1 = open(file_path, 'w')
f = csv.writer(csv_file1)
f.writerow('')
csv_file1.close()

print('清空文件完毕')
print('确认为空')
csv_file1 = open(file_path, 'w')
reader = csv.reader(csv_file1)
print(getsizeof(reader))
csv_file1.close()
time.sleep(2)

# with open(file_path,'w',newline='') as f:
#     f.writelines(['dataid,isdown'])
list00 = [line for line in list0]
print(list00)
with open(file_path,'a',newline='') as f1:
   # f1_csv = csv.writer(f1)
        #f1.write([list[i],str(0)]+','+'\n')
    for i in range(10):
        f1.writelines(list00[i-1] + '\n')

print('写入后，打开文件')
# 测试打开
csv_file1 = open(file_path, 'r')
reader = csv.reader(csv_file1)
for item in reader:
    print(item,end='\n')
csv_file1.close()
print('写入后，读取第一列')
csv_file1 = open(file_path, 'r')
reader = csv.reader(csv_file1)
for item in reader:
    print(item[0])

print('写入后，读取第一列后，修改第二列')
# 没有完成
csv_file1 = open(file_path, 'r')
reader = csv.reader(csv_file1)
for item in reader:
    print(item[0])