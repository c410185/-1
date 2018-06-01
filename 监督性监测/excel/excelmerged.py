import xlrd
import xlwt


file_path = r'D:\IPE_download\jdxjc\excel处理\浙江-text\2014年5月份火电厂监督性监测.xlsx'
file_path1 = r'D:\IPE_download\jdxjc\excel处理\浙江-text\2014年6月份火电厂监督性监测数据.xls'




if __name__ == '__main__':
    wb = xlrd.open_workbook(file_path)
    table = wb.sheet_by_index(0)
    colspan = {}
    # 用于保存计算出的合并的单元格，key=(7, 4)合并单元格坐标，value=(7, 2)合并单元格首格坐标
    # table.merged_cells是一个元组的集合，每个元组由4个数字构成(7，8，2，5)
    # 四个数字依次代表：行，合并的范围(不包含)，列，合并的范围(不包含)，类似range()，从0开始计算
    # (7，8，2，5)的意思是第7行的2,3,4列进行了合并
    if table.merged_cells:
        for item in table.merged_cells:
            for row in range(item[0], item[1]):
                for col in range(item[2], item[3]):
                    # 合并单元格的首格是有值的，所以在这里进行了去重
                    if (row, col) != (item[0], item[2]):
                        colspan.update({(row, col): (item[0], item[2])})
                        #(item[0], item[2]) 为合并单元格的第一个值，(row，col)为其他被合并的单元格
    print(colspan)
    # colspan = {(6, 10): (5, 10), (7, 10): (5, 10), (8, 10): (5, 10), (2, 7): (1, 7), (3, 7): (1, 7), (4, 7): (1, 7), (2, 8): (1, 8), (3, 8): (1, 8), (4, 8): (1, 8), (2, 9): (1, 9), (3, 9): (1, 9), (4, 9): (1, 9), (2, 10): (1, 10), (3, 10): (1, 10), (4, 10): (1, 10),...}
    # 尝试将合并单元格的值直接写入到被合并的单元格

