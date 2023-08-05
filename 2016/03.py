#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def main():

    lines = open_data("03.data")

    valid_1 = 0
    valid_2 = 0
    c1, c2, c3 = [], [], []

    for i, l in enumerate(lines):
        a, b, c = ints(l)
        valid_1 += a+b>c and a+c>b and b+c>a
        c1.append(a)
        c2.append(b)
        c3.append(c)

        count = lambda c: c[-1]+c[-2]>c[-3] and c[-1]+c[-3]>c[-2] and c[-2]+c[-3]>c[-1]
        if i%3 == 2:
            valid_2 += count(c1) + count(c2) + count(c3)

    print(valid_1)
    print(valid_2)


if __name__ == "__main__":
    main()

# year 2016
# solution for 03.01: 983
# solution for 03.02: 1836
