#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def get_distance(field, keys, a, b):
    get_neighbors = lambda state, pos: [add(pos, d) for d in dir_list_4() if add(pos, d) in state]
    return dijkstra(keys[a], get_neighbors, state=field, end_pos=keys[b])[1]


def main():

    lines = open_data("24.data")

    keys = dict()
    field = dict()

    for y,l in enumerate(lines):
        for x,c in enumerate(l):
            if c.isnumeric():
                keys[int(c)] = (x,y)
            if c != "#":
                field[(x,y)] = True

    nums = sorted(list(keys.keys()))
    direct = {}
    for i1 in range(len(keys)):
        n1 = nums[i1]
        for i2 in range(i1+1, len(keys)):
            n2 = nums[i2]
            d = get_distance(field, keys, n1, n2)
            direct[(n1, n2)] = d
            direct[(n2, n1)] = d

    perm = list(filter(lambda x: x[0] == nums[0], permutations(nums)))

    print(min(sum(direct[(p[i-1], p[i])] for i in range(1, len(p))) for p in perm))

    perm = [list(p)+[0] for p in perm]
    print(min(sum(direct[(p[i-1], p[i])] for i in range(1, len(p))) for p in perm))


if __name__ == "__main__":
    main()

# year 2016
# solution for 24.01: 460
# solution for 24.02: 668
