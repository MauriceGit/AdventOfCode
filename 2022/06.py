#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def main():

    line = open_data("06.data")[0]
    print("\n".join(map(str, (next(i+n for i in range(len(line)) if len(set(line[i:i+n])) == n) for n in [4, 14]))))


if __name__ == "__main__":
    main()

# year 2022
# solution for 06.01: 1929
# solution for 06.02: 3298
