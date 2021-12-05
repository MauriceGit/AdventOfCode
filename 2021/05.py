#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *


def direction(a, b):
    return 1 if b > a else (-1 if b < a else 0)


def run(lines, first_part=True):
    field = defaultdict(int)
    for l in lines:
        if first_part and l[0] != l[2] and l[1] != l[3]:
            continue

        dx, dy = direction(l[0], l[2]), direction(l[1], l[3])
        x, y = l[0], l[1]
        while (x,y) != (l[2]+dx,l[3]+dy):
            field[(x,y)] += 1
            x, y = x+dx, y+dy

    return(len(lfilter(lambda x: x > 1, field.values())))


def main():

    lines = lmap(ints, open_data("05.data"))

    print(run(lines))
    print(run(lines, first_part=False))


if __name__ == "__main__":
    main()

# year 2021
# solution for 05.01: 6461
# solution for 05.02: 18065
