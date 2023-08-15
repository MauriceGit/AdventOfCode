#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def puzzle_1(n):
    reductions = 1
    candidate = 0
    while n > 1:
        last_n = n
        steps = 2**reductions
        if n%2 != 0:
            candidate = candidate+steps
        n = n//2
        reductions += 1

    return candidate+1


def run(l_in):
    n = len(l_in)
    l = []
    mod = n%3
    offset = (n+2)%3

    for i in range(offset, n-mod, 3):
        l.append(l_in[i if i < n//2 else i+mod])

    return l if mod == 0 else l[1:] + l[:1]


def puzzle_2(l):
    while len(l) > 1:
        l = list(run(l))
    return l[0]


def main():

    n = int(open_data("19.data")[0])

    print(puzzle_1(n))
    print(puzzle_2(list(range(1, n+1))))


if __name__ == "__main__":
    main()

# year 2016
# solution for 19.01: 1808357
# solution for 19.02: 1407007
