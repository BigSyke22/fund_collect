# coding=utf-8

import xlrd

# 打开文件
data = xlrd.open_workbook('file/demo.xlsx')

# 查看工作表
data.sheet_names()
print("sheets：" + str(data.sheet_names()))

# 通过文件名获得工作表,获取工作表1
table = data.sheet_by_name('工作表1')

# 打印data.sheet_names()可发现，返回的值为一个列表，通过对列表索引操作获得工作表1
# table = data.sheet_by_index(0)

# 获取行数和列数
# 行数：table.nrows
# 列数：table.ncols
print("总行数：" + str(table.nrows))
print("总列数：" + str(table.ncols))

# 获取整行的值 和整列的值，返回的结果为数组
# 整行值：table.row_values(start,end)
# 整列值：table.col_values(start,end)
# 参数 start 为从第几个开始打印，
# end为打印到那个位置结束，默认为none
print("整行值：" + str(table.row_values(0)))
print("整列值：" + str(table.col_values(1)))

# 获取某个单元格的值，例如获取B3单元格值
cel_B3 = table.cell(3,2).value
print("第三行第二列的值：" + cel_B3)



import requests
#from bs4 import BeautifulSoup
import csv
import time
import sys


sFileName=open('基金.csv', "r", encoding="utf-8")
rows=csv.reader(sFileName)

for fund_info in rows:
    print(fund_info)
    
    url="http://gz-fund.10jqka.com.cn/?module=api&controller=index&action=chart&info=vm_fd_"+fund_info[1]+"&start=1100"

    headers={"User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"}
    data=requests.get(url)
    data.encoding="UTF-8"
    datasplit=data.text.split("|")
    datasplit1=datasplit[1].split(";")
    datasplit2=datasplit[1].split(",")
    #print(datasplit2)
    print(float(datasplit2[1]), float(datasplit2[2]))
    mx=float(datasplit2[1])-float(datasplit2[2])
    rata=mx/float(datasplit2[2])*100

    print(rata)
    