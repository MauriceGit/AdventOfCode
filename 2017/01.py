#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def count(n, incr):
    return sum([int(n[i]) if n[i] == n[(i+incr)%len(n)] else 0 for i in range(len(n))])


def main():

    lines = open_data("01.data")[0]

    print(count(lines, 1))
    print(count(lines, len(lines)//2))

if __name__ == "__main__":
    main()

# year 2017
# solution for 01.01: 1390
# solution for 01.02: 1232
