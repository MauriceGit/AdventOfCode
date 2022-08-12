#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def run(numbers, part2):
    i = 0
    c = 0
    while i >= 0 and i < len(numbers):
        offset = 1
        if part2 and numbers[i] >= 3:
            offset = -1
        numbers[i] += offset
        i += numbers[i]-offset
        c += 1
    return c


def main():

    numbers = ints(open_data("05.data"))

    print(run(numbers.copy(), False))
    print(run(numbers.copy(), True))


if __name__ == "__main__":
    main()

# year 2017
# solution for 05.01: 339351
# solution for 05.02: 24315397
