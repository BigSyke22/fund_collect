import xlrd
import requests
import time
import json
import re
import logging

data = xlrd.open_workbook("../config/fund.xlsx", encoding_override = "utf-8")
table = data.sheet_by_index(0)
length = table.nrows

fund_list = []

total_amount = 0
total_increasement = 0

class Fund():
    def __init__(self, name, code, amount):
        self.name = name
        self.code = code
        self.amount = int(amount)
        self.worth_today = 0
        self.worth_yesterday = 0
        self.amplitude = 0

    def set_amplitude(self):
        mx = float(self.worth_today) - float(self.worth_yesterday)
        self.amplitude = mx / float(self.worth_yesterday) * 100

    def print_info(self):
        if self.amplitude > 0:
            amplitude = "\033[31m+%.2f%%\033[0m"%self.amplitude + " \033[31m+%.2fk\033[0m"%(self.amount * self.amplitude / 100000)
        else:
            amplitude = "\033[32m%.2f%%\033[0m"%self.amplitude + " \033[32m%.2fk\033[0m"%(self.amount * self.amplitude / 100000)

        info = amplitude + " " + self.name
        
        logging.info(info)

    def include_in_total(self):
        global total_amount, total_increasement
        total_amount = total_amount + self.amount
        total_increasement = total_increasement + self.amount * self.amplitude / 100

def insert_fund_info(fund, list_fund):
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
    
def refresh_fund_networth():
    list_fund = []

    for fund in fund_list:
        url = 'http://fundgz.1234567.com.cn/js/%s.js' % fund.code

        try:
            data = requests.get(url, timeout = 1)
            data = json.loads(re.match(".*?({.*}).*", data.text, re.S).group(1))
        except:
            logging.info("网络错误:%s %s", fund.name, url)
            continue
    
        fund.worth_today      = float(data['gsz'])
        fund.worth_yesterday  = float(data['dwjz'])

        fund.set_amplitude()
        insert_fund_info(fund, list_fund)

    for fund in list_fund:
        fund.print_info()
        fund.include_in_total()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(message)s')

    for index in range (length):
        rows = table.row_values(index)
        fund = Fund(rows[0], rows[1], rows[2])
        fund_list.append(fund)

    while 1:
        print(time.strftime("%Y-%m-%d %H:%M", time.localtime()))
        refresh_fund_networth()
        if total_increasement > 0:
            print("\nTotal revenue : \033[31m+%.2fk\033[0m"%(total_increasement / 1000))
        else:
            print("\nTotal revenue : \033[32m%.2fk\033[0m"%(total_increasement / 1000))

        total_amount = 0
        total_increasement = 0
        time.sleep(60)
