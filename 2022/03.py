#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def priority(t):
    return ord(t)-(38 if t.isupper() else 96)

def main():

    lines = open_data("03.data")

    type_sum = 0
    badge_sum = 0
    for i, line in enumerate(lines):
        type_sum += priority(set(line[:len(line)//2]).intersection(set(line[len(line)//2:])).pop())
        if i%3 == 2:
            badge_sum += priority(set(lines[i-2]).intersection(set(lines[i-1])).intersection(line).pop())

    print(type_sum)
    print(badge_sum)


if __name__ == "__main__":
    main()

# year 2022
# solution for 03.01: 7763
# solution for 03.02: 2569
