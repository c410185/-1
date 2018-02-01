#encoding=utf-8
import pyodbc

def get_dataid():
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=IPE-PC;DATABASE=pwxk;UID=sa;PWD=20171016')
    cursor = cnxn.cursor()
    cursor.execute('select dataid from pwxk_zbfb')
    rows = cursor.fetchall()
    cnxn.close()
    # 获取数据后，即使关闭了数据库的查询，对象仍然存在
    dataid_list = []
    if rows:
        for i in rows:
            # rows的每一个元素都是一个包含所有列的元祖，所以需要指定要去的列，
            # 如果要取dataid,则需要取i[0]
            dataid_list.append(i[0])
    return dataid_list

if __name__ == '__main__':
    datalist = get_dataid()
    print(datalist)