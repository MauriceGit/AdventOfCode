#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def calc_next_num(num):
    nums = [num]
    while any(nums[-1]):
        nums.append([nums[-1][i]-nums[-1][i-1] for i in range(1,len(nums[-1]))])

    next_num = 0
    for i in range(len(nums)-2, -1, -1):
        next_num = nums[i][-1]+next_num

    return next_num


def main():

    lines = open_data("09.data")
    history = lmap(ints, lines)

    print(sum(calc_next_num(h) for h in history))
    print(sum(calc_next_num(h) for h in lmap(lambda x: list(reversed(x)), history)))


if __name__ == "__main__":
    main()

# year 2023
# solution for 09.01: 1861775706
# solution for 09.02: 1082
