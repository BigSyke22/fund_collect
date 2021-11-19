import math
import  logging
import copy
from sys import argv
dict_host = {}
if __name__ == '__main__':
    a = [1, "hello", [2, 3], {"key": "123"}] 

    b = copy.copy(a) 

    print(id(a) == id(b)) 

    print(id(a[2]) == id(b[2])) 

    
    
    