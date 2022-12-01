#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def main():

    counts = sorted(map(sum, map(ints, open_data_groups("01.data"))))

    print(counts[-1])
    print(sum(counts[-3:]))


if __name__ == "__main__":
    main()

# year 2022
# solution for 01.01: 69626
# solution for 01.02: 206780
