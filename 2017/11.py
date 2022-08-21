#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def cube_dist(a, b):
    return sum(map(abs, sub(a, b))) // 2


def main():
    dirs = open_data("11.data")[0].split(",")

    # odd q vertical layout -> Every odd column is pushed down!
    # https://www.redblobgames.com/grids/hexagons/
    # Use cube coordinates with (s, q, r)
    pos = (0,0,0)
    max_dist = 0
    for d in dirs:
        pos = add(pos, {
            "n": (1,0,-1),
            "ne": (0, 1, -1),
            "se": (-1, 1, 0),
            "s": (-1, 0, 1),
            "sw": (0, -1, 1),
            "nw": (1, -1, 0),
        }[d])
        max_dist = max(max_dist, cube_dist((0,0,0), pos))

    print(cube_dist((0,0,0), pos))
    print(max_dist)


if __name__ == "__main__":
    main()

# year 2017
# solution for 11.01: 682
# solution for 11.02: 1406
