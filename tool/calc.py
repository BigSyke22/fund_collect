import math
from sys import argv
def calc_value(years, investment, salary, salary_growth, inflation):
    duration_month = years * 12

    value = 0

    grow_monthly = pow(investment + 1, 1/12)
    #print(grow_monthly)
    salary_monthly = salary
    for time in range(0, duration_month):
        if 0 == time % 12 and 0 != time:
            salary_monthly = salary_monthly * (1 + salary_growth)

        value_this_priod = pow(grow_monthly, duration_month - time) * salary_monthly
        value += value_this_priod
        #print(value)

    print("current value considered inflation", int(value/ pow((1 + inflation), years)))

if __name__ == '__main__':
    if len(argv) < 6:
        print("Example Insert: 10 0.2 15000 0.12 0.08")
        quit()
        
    years = int(argv[1])
    investment = float(argv[2])
    salary = int(argv[3])
    salary_growth = float(argv[4])
    inflation = float(argv[5])
    calc_value(years, investment, salary, salary_growth, inflation)