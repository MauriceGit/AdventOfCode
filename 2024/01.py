#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def main():

    lines = open_data("01.data")
    print(sum(map(lambda x: abs(x[0]-x[1]), zip(*map(sorted, zip(*map(tuple, map(ints, lines))))))))

    left, right = zip(*map(tuple, map(ints, lines)))
    count_right = Counter(right)
    print(sum(map(lambda x: x*count_right[x], left)))


if __name__ == "__main__":
    main()

# year 2024
# solution for 01.01: 1258579
# solution for 01.02: 23981443
