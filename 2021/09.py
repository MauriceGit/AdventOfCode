#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *


def bfs(field, pos):
    basin = set()
    queue = [pos]

    while len(queue) > 0:
        p = queue.pop(0)
        basin.add(p)
        neighbors = [add(p, (-1,0)), add(p, (1,0)), add(p, (0,-1)), add(p, (0,1))]
        for n in neighbors:
            if field[n] >= field[p] and field[n] < 9 and n not in basin:
                queue.append(n)

    return basin


def main():

    lines = open_data("09.data")

    field = defaultdict(lambda: 10)
    for y,col in enumerate(lines):
        for x,v in enumerate(col):
            field[x,y] = int(v)

    low_points = []
    low_point_pos = []
    for pos, v in list(field.items()):
        if v < field[add(pos, (-1,0))] and v < field[add(pos, (1,0))] and v < field[add(pos, (0,1))] and v < field[add(pos, (0,-1))]:
            low_points.append(1+v)
            low_point_pos.append(pos)

    print(sum(low_points))

    basins = [bfs(field, p) for p in low_point_pos]
    print(reduce(lambda x,y: x*y, sorted(lmap(len, basins))[-3:]))


if __name__ == "__main__":
    main()

# year 2021
# solution for 09.01: 506
# solution for 09.02: 931200
