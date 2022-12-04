#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def main():

    lines = open_data("04.data")

    subsets = 0
    overlap = 0
    for l in lines:
        a, b = l.split(",")
        left  = set(range(*add(tuple(map(int, a.split("-"))), (0,1))))
        right = set(range(*add(tuple(map(int, b.split("-"))), (0,1))))
        subsets += left.issubset(right) or right.issubset(left)
        overlap += left.intersection(right) != set()
    print(subsets)
    print(overlap)


if __name__ == "__main__":
    main()

# year 2022
# solution for 04.01: 538
# solution for 04.02: 792
