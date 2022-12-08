#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def treeline(field, pos, dx=None, dy=None):
    ts = []
    if not dx:
        dx = (pos[0], pos[0]+1, 1)
    if not dy:
        dy = (pos[1], pos[1]+1, 1)
    for y in range(*dy):
        for x in range(*dx):
            ts.append(field[(x, y)] < field[pos])
    return ts


def visible(field, pos, w, h):
    tls = [
        all(treeline(field, pos, dx=(pos[0]+1, w))),
        all(treeline(field, pos, dx=(0, pos[0]))),
        all(treeline(field, pos, dy=(pos[1]+1, h))),
        all(treeline(field, pos, dy=(0, pos[1])))
    ]

    return any(tls)


def scenic_score(field, pos, w, h):
    tls = [
        treeline(field, pos, dx=(pos[0]+1, w)),
        treeline(field, pos, dx=(pos[0]-1, -1, -1)),
        treeline(field, pos, dy=(pos[1]+1, h)),
        treeline(field, pos, dy=(pos[1]-1, -1, -1))
    ]
    tls = list(map(lambda x: len(x) if False not in x else x.index(False)+1, tls))
    return reduce(operator.mul, tls, 1)


def main():

    lines = open_data("08.data")
    grid = {(x,y): int(v) for y,line in enumerate(lines) for x,v in enumerate(line)}

    print(sum(visible(grid, pos, len(lines[0]), len(lines)) for pos in grid))
    print(max(scenic_score(grid, pos, len(lines[0]), len(lines)) for pos in grid))


if __name__ == "__main__":
    main()

# year 2022
# solution for 08.01: 1679
# solution for 08.02: 536625
