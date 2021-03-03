import math
from sys import argv
def calc_value(years, investment, salary, salary_growth, inflation, bonus):
    duration_month = years * 12

    value = 0

    grow_monthly = pow(investment + 1, 1/12)
    #print(grow_monthly)
    salary_monthly = salary
    bonus_current = bonus
    for time in range(1, duration_month + 1):
        if 0 == (time - 1) % 12 and 1 != time:
            salary_monthly = salary_monthly * (1 + salary_growth)
            value_this_priod = pow(grow_monthly, duration_month - time) * salary_monthly

        elif 0 == time % 12:
            if time == 12:
                pass
            else:
                bonus_current = bonus_current * (1 + salary_growth)
            value_this_priod = pow(grow_monthly, duration_month - time) * (salary_monthly + bonus_current)
        
        else:
            value_this_priod = pow(grow_monthly, duration_month - time) * salary_monthly

        value += value_this_priod
        #print(value)

    asset = int(value/ pow((1 + inflation), years))
    return asset

if __name__ == '__main__':
    if len(argv) < 6:
        print("Example Insert: 10 25 10000 11 8 400000")
        quit()
        
    years = int(argv[1])
    investment = float(argv[2]) / 100
    salary = int(argv[3])
    salary_growth = float(argv[4]) / 100
    inflation = float(argv[5]) / 100
    bonus = salary * 8

    if len(argv) == 7:
        base = int(argv[6])
    else:
        base = 0

    print("Considered Inflation")


    asset_this_year = 0
    asset_last_year = base
    for year in range(1, years + 1):
        asset_this_year = calc_value(year, investment, salary, salary_growth, inflation, bonus) + base * pow((1 + investment) / (1 + inflation), year)
        print("Year%d: %d Increasement: %d "%(year, asset_this_year, asset_this_year - asset_last_year))
        asset_last_year = asset_this_year
