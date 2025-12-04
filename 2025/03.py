#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def get_joltage(bank, current_joltage, count):
    if count == 0:
        return current_joltage
    max1_i, max1 = max(enumerate(bank[:-(count-1)] if count >= 2 else bank), key=lambda x: x[1])
    return get_joltage(bank[max1_i + 1 :], current_joltage + max1, count - 1)


def main():

    banks = open_data("03.data")

    print(sum(int(get_joltage(bank, "", 2)) for bank in banks))
    print(sum(int(get_joltage(bank, "", 12)) for bank in banks))


if __name__ == "__main__":
    main()

# year 2025
# solution for 03.01: 17031
# solution for 03.02: 168575096286051
