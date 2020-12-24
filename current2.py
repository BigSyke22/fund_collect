import xlrd
import requests
import time
import logging

class Fund():
    def __init__(self, name, code):
        self.name = name
        self.code = code
        self.worth_today = 0
        self.worth_yesterday = 0
        self.amplitude = 0

    def print_info(self):
        mx = float(self.worth_today) - float(self.worth_yesterday)
        self.amplitude = mx / float(self.worth_yesterday) * 100

        logging.info("%s 今日净值：%s 昨日净值：%s 涨跌：%f%%"%(self.name, self.worth_today, self.worth_yesterday, self.amplitude))

data = xlrd.open_workbook("fund.xlsx")
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

    url = "http://gz-fund.10jqka.com.cn/?module=api&controller=index&action=chart&info=vm_fd_" + fund.code + "&start=" + current_time

    headers = {"User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"}
    data = requests.get(url)
    data.encoding = "UTF-8"
    datasplit = data.text.split("|")[1].split(",")

    if len(datasplit) < 3:
        continue

    worth_today         = datasplit[1]
    worth_yesterday     = datasplit[2]

    fund.worth_today = worth_today
    fund.worth_yesterday = worth_yesterday

    #fund.logging.info_info()

    list_fund.append(fund)
    #logging.info(fund.worth_today, fund.worth_yesterday, fund.amplitude)

for fund in list_fund:
    fund.logging.info_info()

