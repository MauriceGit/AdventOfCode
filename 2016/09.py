#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def calc_len(line, multiplier, part_1=True):
    m = re.finditer(r"(\(\d+x\d+\))", line)
    count = 0
    i = 0
    for g in m:
        c, r = ints(g.groups(0)[0])
        start, stop = g.span()

        if i > start:
            continue

        count += len(line[i:start])
        if part_1:
            count += len(line[stop:stop+c]) * r
        else:
            count += calc_len(line[stop:stop+c], r, part_1=part_1)
        i = stop+c

    count += len(line[i:])
    return count * multiplier

def main():

    line = open_data("09.data")[0]

    print(calc_len(line, 1, part_1=True))
    print(calc_len(line, 1, part_1=False))


if __name__ == "__main__":
    main()

# year 2016
# solution for 09.01: 150914
# solution for 09.02: 11052855125
