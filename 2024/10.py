#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def main():

    lines = open_data("10.data")

    f = dict()
    trailheads = []

    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            f[(x, y)] = 100 if c == "." else int(c)
            if c == "0":
                trailheads.append((x, y))

    def get_neighbors(state, pos):
        for d in dir_list_4():
            if add(pos, d) in f and f[add(pos, d)] == f[pos]+1:
                yield add(pos, d)

    def visit(state, pos, dist, path):
        if f[pos] == 9:
            state[0] += 1
        return True

    state_p1 = [0]
    state_p2 = [0]
    for start in trailheads:
        dijkstra(start, get_neighbors, state=state_p1, visit=visit)
        dijkstra(start, get_neighbors, state=state_p2, visit=visit, revisit_nodes=True)

    print(state_p1[0])
    print(state_p2[0])


if __name__ == "__main__":
    main()

# year 2024
# solution for 10.01: 468
# solution for 10.02: 966
