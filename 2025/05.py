#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def reduce_ranges(fresh):
    fresh.sort(key=lambda x: x[0])
    ranges = [fresh[0]]
    for start, end in fresh[1:]:
        if start <= ranges[-1][1]+1 and end > ranges[-1][1]:
            ranges[-1][1] = end
        elif start > ranges[-1][1]+1:
            ranges.append([start, end])
    return sum(map(lambda x: x[1]-x[0]+1, ranges))


def main():

    fresh, ids = open_data_groups("05.data")
    fresh = [[int(f[0]), int(f[1])] for f in map(lambda x: x.split("-"), fresh)]

    print(len({i for i in ints(ids) for l,h in fresh if l <= i <= h}))
    print(reduce_ranges(fresh))


if __name__ == "__main__":
    main()

# year 2025
# solution for 05.01: 775
# solution for 05.02: 350684792662845
