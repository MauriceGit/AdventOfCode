#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *

def is_multiple(s, count):
    return len(s) > 1 and len(s) % count == 0 and s == s[:count] * (len(s) // count)


def main():

    ranges = lmap(lambda x: tuple(ints(x.split("-"))), open_data("02.data")[0].split(","))

    invalid_p1, invalid_p2 = 0, 0
    for s, t in ranges:
        for i in range(s, t+1):
            number = str(i)
            for count in range(1, (len(number) + 1) // 2 + 1):
                if is_multiple(number, count):
                    if len(number)%2==0 and is_multiple(number, len(number)//2):
                        invalid_p1 += i
                    invalid_p2 += i
                    break
    print(invalid_p1)
    print(invalid_p2)


if __name__ == "__main__":
    main()

# year 2025
# solution for 02.01: 41294979841
# solution for 02.02: 66500947346
