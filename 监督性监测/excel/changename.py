#coding:utf-8
import os

'''
def rename(dirpath, oldext, newext):
    for roots, dirs, files in os.walk(dirpath):        
        for name in files:
            if name.endswith(oldext):      
                curdir = os.getcwd()            
                os.chdir(roots)             
                os.rename(name, os.path.splitext(name)[0] + newext)                
                os.chdir(curdir)

rename('/Users/black3y/Desktop/1/','.txt','.py')
'''

def filerename(filepath,srctype,destype):
    for path,dirlist,filelist in os.walk(filepath):
        for file in filelist:

            #防止文件名中包含.
            fullist = file.split('.')
            namelist = fullist[0:-1]
            filename = ''
            for i in namelist:
                filename = filename + i + '.'
            # print (filename)

            curndir = os.getcwd()    #获取当前路径
            # print (curndir)

            os.chdir(path)            #设置当前路径为目标目录
            newdir = os.getcwd()    #验证当前目录
            # print (newdir)

            filetype = file.split('.')[-1]    #获取目标文件格式

            if filetype == srctype:    #修改目标目录下指定后缀的文件（包含子目录）
                os.rename(file,filename+destype)

            if srctype == '*':        #修改目标目录下所有文件后缀（包含子目录）
                os.rename(file,filename+destype)

            if srctype == 'null':    #修改目标目录下所有无后缀文件（包含子目录）
                if len(fullist) == 1:
                    os.rename(file,file+'.'+destype)

            os.chdir(curndir)    #回到之前的路径


if __name__ == '__main__':
    path = 'D:\IPE_download\jdxjc\excel处理\浙江-text'
    filerename(path,'xls','xml')