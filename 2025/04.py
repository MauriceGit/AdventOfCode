#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *

def remove_rolls(grid):
    removed = []
    for p in filter(lambda x: grid[x] == "@", grid.keys()):
        if sum(grid[add(p, d)] == "@" for d in dir_list_8() if add(p, d) in grid) < 4:
            removed.append(p)
    for r in removed:
        grid[r] = "."

    return len(removed)

def main():

    lines = open_data("04.data")

    grid = dict()
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            grid[(x,y)] = c

    print(remove_rolls(grid.copy()))

    removed = 0
    for i in itertools.count():
        tmp = remove_rolls(grid)
        if tmp == 0:
            break
        removed += tmp
    print(removed)





if __name__ == "__main__":
    main()

# year 2025
# solution for 04.01: 1626
# solution for 04.02: 9173
