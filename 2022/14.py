#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def run(rocks, part1=True):
    lowest_point = max(map(lambda x: x[1], filter(lambda k: rocks[k] == 1, rocks.keys())))
    for i in itertools.count():
        sand = (500,0)
        while True:
            if part1 and sand[1] > lowest_point:
                return i
            if add(sand, (0, 1)) not in rocks:
                sand = add(sand, (0, 1))
                continue
            if add(sand, (-1, 1)) not in rocks:
                sand = add(sand, (-1, 1))
                continue
            if add(sand, (1, 1)) not in rocks:
                sand = add(sand, (1, 1))
                continue
            rocks[sand] = 2
            break
        if not part1 and sand == (500,0):
            return i+1


def main():

    lines = open_data("14.data")

    rocks = dict()
    lowest_point = 0
    for line in lines:
        points = line.split(" -> ")
        px, py = ints(points[0])

        for p in points[1:]:
            xx, yy = ints(p)
            for x in range(min(px, xx), max(px, xx)+1):
                rocks[(x,py)] = 1
            for y in range(min(py, yy), max(py, yy)+1):
                rocks[(px,y)] = 1
            px, py = xx, yy
            lowest_point = max(py, lowest_point)

    for x in range(-1000, 1000):
        rocks[(x, lowest_point+2)] = 3

    print(run(rocks.copy()))
    print(run(rocks, part1=False))


if __name__ == "__main__":
    main()

# year 2022
# solution for 14.01: 808
# solution for 14.02: 26625
