#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def main():

    lines = open_data("03.data")

    p1 = 0
    p2 = 0
    enabled = True
    for l in lines:
        p1 += sum(map(lambda x: x[0]*x[1] , map(ints, re.findall(r"mul\(-?\d\d?\d?,-?\d\d?\d?\)", l))))

        for m in re.findall(r"(mul\(-?\d\d?\d?,-?\d\d?\d?\))|(do\(\))|(don't\(\))", l):
            if m[2] != "":
                enabled = False
            if m[1] != "":
                enabled = True
            if m[0] != "" and enabled:
                p2 += reduce(operator.mul, ints(m[0]))
    print(p1)
    print(p2)

if __name__ == "__main__":
    main()

# year 2024
# solution for 03.01: 183380722
# solution for 03.02: 82733683
