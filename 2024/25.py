#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *

def parse_group(g):
    res = [-1]*5
    for line in g:
        for x, c in enumerate(line):
            res[x] += c == "#"
    return tuple(res)

def find_locks(locks, key):
    return sum(all(l[i]+key[i] <= 5 for i in range(5)) for l in locks)

def main():

    groups = open_data_groups("25.data")

    locks = lmap(parse_group, filter(lambda x: "." not in x[0], groups))
    keys = map(parse_group, filter(lambda x: "#" not in x[0], groups))

    print(sum(map(lambda k: find_locks(locks, k), keys)))


if __name__ == "__main__":
    main()

# year 2024
# solution for 25.01: 3483
# solution for 25.02: *
