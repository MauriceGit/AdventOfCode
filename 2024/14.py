#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *
import time

Robot = recordtype("Robot", "p v")

def mod(p, m):
    return tuple(p[i]%m[i] for i in range(len(p)))

def savety_factor(robots, size):
    quadrants = [
        (0, size[0]//2, 0, size[1]//2),                 # upper left
        (size[0]//2+1, size[0], 0, size[1]//2),         # upper right
        (0, size[0]//2, size[1]//2+1, size[1]),         # lower left
        (size[0]//2+1, size[0], size[1]//2+1, size[1]), # lower left
    ]

    def _filter(q):
        return filter(lambda x: q[0] <= x.p[0] < q[1] and q[2] <= x.p[1] < q[3], robots)
    return reduce(operator.mul, (sum(map(lambda x: 1, _filter(q))) for q in quadrants))


def main():

    size = (101, 103)
    robots = []
    lines = open_data("14.data")
    for px, py, vx, vy in map(ints, lines):
        robots.append(Robot((px, py), (vx, vy)))

    def is_christmas_tree(robots):
        # most points in the center quarter on both axes seems to match only the christmas tree :)
        def test(r):
            return (r.p[0] >= size[0]//4 and
                   r.p[0] < 3*size[0]//4 and
                   r.p[1] >= size[1]//4 and
                   r.p[1] < 3*size[1]//4)
        return len(list(filter(lambda x: test(x), robots))) >= 2*len(robots)//4

    for i in itertools.count():
        for r in robots:
            r.p = mod(add(r.p, r.v), size)

        if i == 99:
            print(savety_factor(robots, size))

        if is_christmas_tree(robots):
            #draw({r.p:"#" for r in robots}, print_directly=True, symbols={-1: " "})
            print(i+1)
            break


if __name__ == "__main__":
    main()

# year 2024
# solution for 14.01: 231221760
# solution for 14.02: 6771
