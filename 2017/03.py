#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *

def num(n):
    s = 0
    while n > 0:
        s += 4*2*n
        n -= 1
    return s+2

def find(start_n, incr, target):
    i = 0
    while True:
        if start_n+i*incr > target:
            return abs(target-(start_n+(i)*incr)+1)
        i += 1

    return 0

def main():

    lines = open_data("03.data")

    #print(num(1))
    #print(num(2))
    #print(num(3))
    #print(num(4))
    #print(num(5))

    a = num(15)
    b = num(16)
    diff = (b-a)//4


    print(a)
    print(b)
    print(diff)

    print(15*2-find(a, diff, 1024))



    a = num(2)
    b = num(3)
    diff = (b-a)//4
    print(2*2-find(a, diff, 23), find(a, diff, 23))






if __name__ == "__main__":
    main()

# year 2017
# solution for 03.01: ?
# solution for 03.02: ?
