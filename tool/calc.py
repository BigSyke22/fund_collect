import math
import argparse
import logging
from sys import argv

LOG_LEVEL = logging.DEBUG

def calc_value(years, investment, salary, bonus, salary_growth, inflation, base):
    grow_monthly = pow(investment + 1, 1/12)

    assets = (base * (1 + investment) + salary * bonus + salary / (1 - grow_monthly) * (1 - pow(grow_monthly, 12))) / (1 + inflation)

    if 1 == years:
        print(format(int(assets), ','))
    else:
        calc_value(years - 1, investment, salary * (1 + salary_growth) / (1 + inflation), bonus, salary_growth, inflation, assets)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("years")
    parser.add_argument("investment")
    parser.add_argument("salary")
    parser.add_argument("bonus")
    parser.add_argument("salary_growth")
    parser.add_argument("inflation")
    parser.add_argument("-b", "--base", help = "add base")

    args = parser.parse_args()
        
    years = int(args.years)
    investment = float(args.investment) / 100
    salary = int(args.salary)
    bonus = float(args.bonus)
    salary_growth = float(args.salary_growth) / 100
    inflation = float(args.inflation) / 100

    if args.base:
        base = int(args.base) * 10000
    else:
        base = 0

    calc_value(years, investment, salary, bonus, salary_growth, inflation, base)
    
