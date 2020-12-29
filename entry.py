import os
import time

while (1):
    print(time.strftime("%Y-%m-%d %H:%M", time.localtime()))
    os.system("python ./get_fund_networth.py")
    time.sleep(60)