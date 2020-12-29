import math
from sys import argv
def calc_value(duration, growth, base):
    duration_month = duration * 12

    value = 0

    grow_monthly = pow(growth + 1, 1/12)
    #print(grow_monthly)
    salary_monthly = base
    for time in range(0, duration_month):
        if 0 == time % 12:
            salary_monthly = salary_monthly * 1.12

        value_this_priod = pow(grow_monthly, duration_month - time) * salary_monthly
        value += value_this_priod

    print("current value considered inflation", int(value/ pow(1.08, duration)))

    print(int(value)/(base * 12 * duration * pow(1.08, duration)), "times difference considered inflation")

if __name__ == '__main__':
    calc_value(int(argv[1]), float(argv[2]), int(argv[3]))