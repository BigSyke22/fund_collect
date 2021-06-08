import math
import  logging
from sys import argv

LOG_LEVEL = logging.INFO

def calc_value(years, investment, salary, salary_growth, inflation, bonus):
    logger = logging.getLogger()
    logger.setLevel(LOG_LEVEL)

    duration_month = years * 12

    value = 0

    grow_monthly = pow(investment + 1, 1/12)
    logger.debug(grow_monthly)
    salary_monthly = salary
    bonus_current = bonus
    for time in range(1, duration_month + 1):
        if 0 == (time - 1) % 12 and 1 != time:
            salary_monthly = salary_monthly * (1 + salary_growth)
            value_this_priod = pow(grow_monthly, duration_month - time) * salary_monthly
            logger.debug(value_this_priod)

        elif 0 == time % 12:
            if time == 12:
                pass
            else:
                bonus_current = bonus_current * (1 + salary_growth)
            value_this_priod = pow(grow_monthly, duration_month - time) * (salary_monthly + bonus_current)
            logger.debug(value_this_priod)
        
        else:
            value_this_priod = pow(grow_monthly, duration_month - time) * salary_monthly
            logger.debug(value_this_priod)

        value += value_this_priod
        logger.debug(value)

    asset = int(value/ pow((1 + inflation), years))
    return asset

if __name__ == '__main__':
    if len(argv) < 6:
        print("Example Insert: 10 20 10000 10 8 8 400000")
        quit()
        
    years = int(argv[1])
    investment = float(argv[2]) / 100
    salary = int(argv[3])
    salary_growth = float(argv[4]) / 100
    inflation = float(argv[5]) / 100
    bonus = salary * float(argv[6])

    if len(argv) == 8:
        base = int(argv[7])
    else:
        base = 0

    print("Considered Inflation")


    asset_this_year = 0
    asset_last_year = base
    for year in range(1, years + 1):
        asset_this_year = calc_value(year, investment, salary, salary_growth, inflation, bonus) + base * pow((1 + investment) / (1 + inflation), year)
        print("Year%d: %d Increasement: %d "%(year, asset_this_year, asset_this_year - asset_last_year))
        asset_last_year = asset_this_year
