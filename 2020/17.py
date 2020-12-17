#!/usr/bin/env python3.7

from utility import *

@lru_cache(maxsize=1)
def dirs4():
    r = list(range(-1, 2))
    return [(x,y,z,t) for x in r for y in r for z in r for t in r if (x,y,z,t) != (0,0,0,0)]

@lru_cache(maxsize=1)
def dirs3():
    r = list(range(-1, 2))
    return [(x,y,z) for x in r for y in r for z in r if (x,y,z) != (0,0,0)]

def active_count(grid, p, fdirs, fadd):
    return sum(grid[fadd(p, d)] for d in fdirs())


def cycle(grid, fdirs, fadd, zero):

    dirs = fdirs() + [zero]

    checked = dict()

    new_grid = defaultdict(bool)
    for k in list(grid.keys()):
        for offset in dirs:
            new_k = fadd(k, offset)

            if new_k in checked:
                continue
            checked[new_k] = 1

            c = active_count(grid, new_k, fdirs, fadd)

            if grid[new_k] and (2 <= c <= 3):
                new_grid[new_k] = True
            if not grid[new_k] and c == 3:
                new_grid[new_k] = True

    return new_grid


def main():

    lines = open_data("17.data")

    grid3 = defaultdict(bool)
    grid4 = defaultdict(bool)

    for y, l in enumerate(lines):
        for x, v in enumerate(l):
            grid3[(x, y, 0)] = v == '#'
            grid4[(x, y, 0, 0)] = v == '#'

    for i in range(6):
        grid3 = cycle(grid3, dirs3, add3, (0,0,0))
    print(sum(grid3.values()))

    for i in range(6):
        grid4 = cycle(grid4, dirs4, add4, (0,0,0,0))
    print(sum(grid4.values()))


if __name__ == "__main__":
    main()

# solution for 17.01: 242
# solution for 17.02: 2292
