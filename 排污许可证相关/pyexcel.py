import os
import openpyxl as ox
import download_ben_1 as dben

file_path = r'D:\何方辉\排污许可\排污许可20180516.xlsx'
fail_file = r'D:\何方辉\排污许可\排污许可企业-出错记录.xlsx'
download_path_head = r'D:\何方辉\排污许可\download'

def missions():
    """
    获取到文件中isdown中不为1的数据量
    :return:
    """
    wb = ox.load_workbook(filename=file_path)
    sht = wb.worksheets[0]
    # 获取一个生成器，并且跳过第一行标题行
    row = sht.rows
    cloumn_length = len(list(sht.rows))
    #print(cloumn_length)
    i = 0
    try:
        while i <= cloumn_length:
            row1 = next(row)
            if row1[4].value != 1:
                i += 1
    # 迭代器跑完后，接收异常，防止程序跳出
    except StopIteration:
        return i

def get_file():
    wb = ox.load_workbook(filename=file_path)
    sht = wb.worksheets[0]
    # 获取一个生成器，并且跳过第一行标题行
    row = sht.rows
    # 此处执行了吗？疑问，真正跳过第一行标题行的应该是while语句中的第一个next
    # 如果把下句注释掉，则FileNotFoundError: [WinError 3] 系统找不到指定的路径。:
    # 'D:\\何方辉\\排污许可\\download\\F_ProvinceName\\F_CityName'
    # 所以还是有用的
    row1 = next(row)
    cloumn_length = len(list(sht.rows))
    i = 1
    mission = missions()
    m = 1
    while i <= cloumn_length:
        row1 = next(row)
        province = row1[1].value
        city = row1[2].value
        download_path = download_path_head + '\\' + province + '\\' + city
        if os.path.isdir(download_path):
            pass
        else:
            os.mkdir(download_path)
        dataid = row1[3].value
        # 在此就可以调用获取文件的函数了,调用完再i+1
        # 此处的函数功能没有区分开，获得ID的函数和下载文件的函数混在了一起
        # 添加一个判断功能， 将之前没有下载的文件根据isdown的值再决定是否下载
        # 详情页出现了信息全为空的情况，公司名称和下载链接都为空，没有处理
        if row1[4].value != 1:
            try:
                company_name, zb_url_tail = dben.getNameAndFileid(dataid)
                print(company_name + '------------开始下载------------')
                dben.write_zb(zb_url_tail, company_name,download_path)
                dben.write_fb(dataid, company_name,download_path)
                i += 1
                m += 1
                row1[4].value = 1
                wb.save(filename=file_path)
                last  = ((mission -m) / mission) * 100
                print('第{0}个下载完成，剩余{1} %'.format(m,last))
            except:
                print('出错了')

if __name__ == '__main__':
    get_file()