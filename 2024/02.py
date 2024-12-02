#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def safe(l):
    return lmap(lambda x: 1 <= x[1]-x[0] <= 3, pairwise(l)).count(False) == 0

def check_all(l_in, p2=False):
    return any(safe(l) or any(p2 and safe(l[:i] + l[i+1:]) for i in range(len(l))) for l in (l_in, l_in[::-1]))

def main():
    lines = lmap(ints, open_data("02.data"))

    print(sum(check_all(l) for l in lines))
    print(sum(check_all(l, p2=True) for l in lines))


if __name__ == "__main__":
    main()

# year 2024
# solution for 02.01: 299
# solution for 02.02: 364
