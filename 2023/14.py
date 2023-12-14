#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *

# positions is a generator object, so positions are only generated if we actually move there!
def new_pos(cubes, rocks, positions):
    last_p = next(positions)
    for p in positions:
        if p in cubes or p in rocks:
            return last_p
        last_p = p
    return last_p

def move_up(cubes, rocks, r, len_x, len_y):
    return new_pos(cubes, rocks, ((r[0], y) for y in range(r[1], -1, -1)))

def move_down(cubes, rocks, r, len_x, len_y):
    return new_pos(cubes, rocks, ((r[0], y) for y in range(r[1], len_y)))

def move_right(cubes, rocks, r, len_x, len_y):
    return new_pos(cubes, rocks, ((x, r[1]) for x in range(r[0], len_x)))

def move_left(cubes, rocks, r, len_x, len_y):
    return new_pos(cubes, rocks, ((x, r[1]) for x in range(r[0], -1, -1)))

def tilt(cubes, rocks, len_x, len_y, sorter, move):
    for r in sorted(rocks.keys(), key=sorter[0], reverse=sorter[1]):
        tmp = move(cubes, rocks, r, len_x, len_y)
        if tmp != r:
            del rocks[r]
            rocks[tmp] = 1
    return rocks


def execute_cycle(cubes, rocks, len_x, len_y):
    tilt(cubes, rocks, len_x, len_y, (itemgetter(1, 0), False), move_up)
    tilt(cubes, rocks, len_x, len_y, (itemgetter(0, 1), False), move_left)
    tilt(cubes, rocks, len_x, len_y, (itemgetter(1, 0), True), move_down)
    tilt(cubes, rocks, len_x, len_y, (itemgetter(0, 1), True), move_right)
    return rocks


def main():

    lines = open_data("14.data")

    cubes = set()
    rocks = dict()
    for y,line in enumerate(lines):
        for x,c in enumerate(line):
            if c == "#":
                cubes.add((x,y))
            elif c == "O":
                rocks[(x,y)] = 1

    len_x = len(lines[0])
    len_y = len(lines)

    print(sum(map(lambda x: len(lines)-x[1], tilt(cubes, rocks.copy(), len_x, len_y, (itemgetter(1, 0), False), move_up))))

    cache = set()
    cycle = []
    for i in range(1000000000):

        if tuple(rocks.keys()) in cache:
            cycle.append((i, sum(map(lambda x: len(lines)-x[1], rocks.keys()))))

            c1 = lmap(itemgetter(1), cycle[:len(cycle)//2])
            c2 = lmap(itemgetter(1), cycle[len(cycle)//2:])

            if len(cycle) > 10 and len(cycle)%2==0 and c1 == c2:
                break
        else:
            cache.add(tuple(rocks.keys()))

        rocks = execute_cycle(cubes, rocks, len_x, len_y)

    print(cycle[(1000000000-cycle[0][0]) % (len(cycle)//2)][1])


if __name__ == "__main__":
    main()

# year 2023
# solution for 14.01: 109833
# solution for 14.02: 99875
