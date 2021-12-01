#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *


def main():

    l = lmap(int, open_data("01.data"))

    print(sum(l[i]>l[i-1] for i in range(1, len(l))))
    # two of the three numbers in the sliding window are equal, so we only
    # have to compare the lowest from the last to the highest on the current.
    print(sum(l[i]>l[i-3] for i in range(3, len(l))))


if __name__ == "__main__":
    main()

# year 2021
# solution for 01.01: 1655
# solution for 01.02: 1683
