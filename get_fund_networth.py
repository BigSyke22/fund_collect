import xlrd
import requests
import time
import json
import re
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
class Fund():
    def __init__(self, name, code):
        self.name = name
        self.code = code
        self.worth_today = 0
        self.worth_yesterday = 0
        self.amplitude = 0

    def set_amplitude(self):
        mx = float(self.worth_today) - float(self.worth_yesterday)
        self.amplitude = mx / float(self.worth_yesterday) * 100

    def print_info(self):
        basic_info = "%s "%(self.name)
        if fund.amplitude > 0:
            amplitude = "\033[31m%f%%\033[0m"%fund.amplitude
        else:
            amplitude = "\033[32m%f%%\033[0m"%fund.amplitude

        info = basic_info + amplitude
        
        logging.info(info)

data = xlrd.open_workbook("fund.xlsx", encoding_override = "utf-8")
table = data.sheet_by_index(0)

length = table.nrows
list_fund = []

for index in range (length):
    rows = table.row_values(index)
    fund = Fund(rows[0], rows[1])

    current_hour = time.strftime("%H", time.localtime())
    current_minute = time.strftime("%M", time.localtime())
    
    current_time = ""

    if int(current_hour) >= 15:
        current_time = "1500"
    else:
        current_time = current_hour + current_minute

    url = 'http://fundgz.1234567.com.cn/js/%s.js' % fund.code

    try:
        data = requests.get(url, timeout = 1)
        data = json.loads(re.match(".*?({.*}).*", data.text, re.S).group(1))
    except:
        logging.info("网络错误:%s %s", fund.name, url)
        continue
    

    worth_today         = data['gsz']
    worth_yesterday     = data['dwjz']

    fund.worth_today = float(worth_today)
    fund.worth_yesterday = float(worth_yesterday)

    fund.set_amplitude()
    #fund.logging.info_info()
    
    index = 0
    flag = 0
    for fund_in_list in list_fund:
        if fund.amplitude > fund_in_list.amplitude:    
            list_fund.insert(index, fund)
            flag = 1
            break
        else:
            index += 1
    
    if 0 == flag:
        list_fund.append(fund)



for fund in list_fund:
    fund.print_info()

