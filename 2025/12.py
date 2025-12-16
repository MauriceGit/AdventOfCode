#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *

def region_valid(w, h, counts):
    # Pattern 0 and Pattern 1 can efficiently be combined the following way:
    # 00111
    # 00011
    # 0 011
    c01 = min(counts[0], counts[1])
    c01_all = c01 * 15
    c01_all += (counts[0]-c01) * 9
    c1_left = counts[1] - c01
    c01_all += c1_left//2 * 15 + (9 if c1_left%2 != 0 else 0)
    # Pattern 2 perfectly combines with itself:
    # aaab
    # aabb
    # abbb
    c2 = counts[2]//2 * 12 + (9 if counts[2]%2 != 0 else 0)
    # Pattern 3 efficiently combines with itself:
    # aaa
    # abbb
    # aaab
    #  bbb
    c3 = counts[3]//2 * 16 + (9 if counts[3]%2 != 0 else 0)
    # Pattern 4 efficiently combines with itself (infinitely in one direction!):
    # aaa ccc
    #  a---c    ...
    # aaa-ccc
    #   ---
    c4 = (counts[4]*2+1) * 4
    # Pattern 5 efficiently combines with itself (infinitely in one direction):
    #   aa--cc
    #  aa--cc
    #  ab-.c    ...
    #  bb..
    # bb..
    c5 = (counts[5] + 2) * 5

    return w*h >= c01_all+c2+c3+c4+c5


def count_valid_regions(regions):
    return sum(region_valid(w, h, counts) for (w, h), counts in regions)


def main():
    groups = open_data_groups("12.data")
    regions = groups.pop()
    regions = map(ints, regions)
    regions = lmap(lambda x: ((x[0],x[1]), x[2:]), regions)
    # shapes were evaluated and combined by manual observation
    # shapes = lmap(lambda x: x[1:], groups)

    print(count_valid_regions(regions))


if __name__ == "__main__":
    main()

# year 2025
# solution for 12.01: 454
# solution for 12.02: *
