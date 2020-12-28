import math
from sys import argv
def calc_value(duration, growth, base):
    duration_month = duration * 12

    value = 0

    grow_monthly = pow(growth + 1, 1/12)
    #print(grow_monthly)
    for time in range(0, duration_month):
        value_this_priod = pow(grow_monthly, duration_month - time) * base
        value += value_this_priod
        #print("month:",time + 1, value_this_priod)
    #print("current value:", int(value))
    print("current value considered inflation", int(value/ pow(1.08, duration)))
    #print("original value", base * 12 * duration)
    #print("original value considered inflation", int(base * 12 * duration* pow(1.08, duration)))
    #print(int(value)/(base * 12 * duration), "times difference")

    print(int(value)/(base * 12 * duration * pow(1.08, duration)), "times difference considered inflation")

if __name__ == '__main__':
    calc_value(int(argv[1]), float(argv[2]), int(argv[3]))