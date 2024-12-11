#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def first_n_digits(num, n):
    return num // 10 ** (int(math.log(num, 10)) - n + 1)
def last_n_digits(num, n):
    return num % (10**n)

@lru_cache(maxsize=1000000)
def calc(num, n):
    if n == 0:
        return 1
    if num == 0:
        return calc(1, n-1)
    digits = int(math.log10(num))+1
    if digits%2 == 0:
        return calc(first_n_digits(num, digits//2), n-1) + calc(last_n_digits(num, digits//2), n-1)
    return calc(num*2024, n-1)


def main():

    stones = ints(open_data("11.data")[0])

    print(sum(calc(s, 25) for s in stones))
    print(sum(calc(s, 75) for s in stones))


if __name__ == "__main__":
    main()

# year 2024
# solution for 11.01: 202019
# solution for 11.02: 239321955280205
