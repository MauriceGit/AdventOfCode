#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *

def get_n(f, pos, offset, count=4):
    s = ""
    for i in range(count):
        s += f[add(pos, mul(offset, i))]
    return s


def start_xmas(f, pos):
    if f[pos] not in "XS":
        return False

    return sum(get_n(f, pos, d) in ["XMAS", "SAMX"] for d in dir_list_8())


def find_mas_x(f, pos):
    if f[pos] != "A":
        return False

    x1 = get_n(f, add(pos, (-1, -1)), (1, 1), count=3)
    x2 = get_n(f, add(pos, (1, -1)), (-1, 1), count=3)
    return all(map(lambda x: x in ["SAM", "MAS"], [x1, x2]))

def main():

    lines = open_data("04.data")

    f = defaultdict(str)
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            f[(x,y)] = c

    print(sum(start_xmas(f, k) for k in list(f.keys()))//2)
    print(sum(find_mas_x(f, k) for k in list(f.keys())))


if __name__ == "__main__":
    main()

# year 2024
# solution for 04.01: 2593
# solution for 04.02: 1950
