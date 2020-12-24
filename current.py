import xlrd
import requests
import time

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
        print("%s %s %s %f%%"%(self.code, self.worth_today, self.worth_yesterday, self.amplitude))

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

    url = "http://gz-fund.10jqka.com.cn/?module=api&controller=index&action=chart&info=vm_fd_" + fund.code + "&start=" + current_time

    try:
        headers = {"User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"}
        data = requests.get(url, timeout=0.1)
    except:
        print("Net Error:", fund.name)
        data.encoding = "UTF-8"
    
    if len(data.text.split("|")) > 1:
        datasplit = data.text.split("|")[1].split(",")
    else:
        print("Data Splited by | Error", fund.name)
        continue

    if len(datasplit) > 2:
        #print (fund.name, url, datasplit)
        worth_today         = datasplit[1]
        worth_yesterday     = datasplit[2]

        fund.worth_today = worth_today
        fund.worth_yesterday = worth_yesterday

        fund.set_amplitude()
        #fund.print_info()
        
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
        #print(fund.worth_today, fund.worth_yesterday, fund.amplitude)
    else:
        print("Data of Worth Missed:", fund.code)


for fund in list_fund:
    fund.print_info()

