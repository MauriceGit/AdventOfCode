#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def main():
    lines = open_data("22.data")

    grid = defaultdict(int, {(x,y): int(c == "#") for y,l in enumerate(lines) for x,c in enumerate(l)})
    p = (len(lines[0])//2, len(lines)//2)
    d = (0,-1)
    infect = 0
    for i in range(10_000):
        d = rotate(d, grid[p] == 1)
        grid[p] = 0 if grid[p] == 1 else 1
        infect += grid[p]
        p = add(p, d)
    print(infect)

    grid = defaultdict(int, {(x,y): int(c == "#")*2 for y,l in enumerate(lines) for x,c in enumerate(l)})
    p = (len(lines[0])//2, len(lines)//2)
    d = (0,-1)
    infect = 0
    # clean -> weak -> infected -> flagged -> clean
    # 0 -> 1 -> 2 -> 3 -> 0...
    for i in range(10_000_000):
        d = rotate(d, grid[p] != 0, count=grid[p]-1)
        grid[p] = (grid[p]+1)%4
        infect += grid[p] == 2
        p = add(p, d)
    print(infect)


if __name__ == "__main__":
    main()

# year 2017
# solution for 22.01: 5538
# solution for 22.02: 2511090
