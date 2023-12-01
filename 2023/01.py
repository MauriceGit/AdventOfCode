#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *

def find_num(l, part2=False):
    nums = [("one", "1"), ("two", "2"), ("three", "3"), ("four", "4"), ("five", "5"), ("six", "6"), ("seven", "7"), ("eight", "8"), ("nine", "9"), ]
    res = [n[1] for i in range(len(l)) for n in nums if l[i:].startswith(n[1]) or part2 and l[i:].startswith(n[0])]
    return int(res[0] + res[-1])


def main():
    lines = open_data("01.data")

    print(sum(find_num(l) for l in lines))
    print(sum(find_num(l, part2=True) for l in lines))


if __name__ == "__main__":
    main()

# year 2023
# solution for 01.01: 56465
# solution for 01.02: 55902
