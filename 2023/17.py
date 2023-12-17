#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *

Pos = namedtuple("Pos", "p d count")

def solve(lines, min_steps, max_steps):
    start = Pos((0,0), (1,0), 0)
    target = (len(lines[0])-1, len(lines)-1)

    def edge_cost(state, pos, next_pos):
        if not (0 <= next_pos.p[0] < len(state) and 0 <= next_pos.p[1] < len(state[0])):
            return 999999999999
        return state[next_pos.p[1]][next_pos.p[0]]

    def get_neighbors(state, pos, path):

        if pos.count < min_steps:
            yield Pos(add(pos.p, pos.d), pos.d, pos.count+1)
            return

        if pos.count < max_steps:
            yield Pos(add(pos.p, pos.d), pos.d, pos.count+1)

        dl = rotate(pos.d, True)
        dr = rotate(pos.d, False)
        yield Pos(add(pos.p, dl), dl, 1)
        yield Pos(add(pos.p, dr), dr, 1)


    def visit(state, pos, dist, path):
        return pos.p != target or pos.count < min_steps

    return dijkstra(start, get_neighbors, state=lines, edge_cost=edge_cost, visit=visit)[1]


def main():

    lines = open_data("17.data")
    lines = lmap(lambda line: lmap(int, list(line)), lines)

    print(solve(lines, 0, 3))
    print(solve(lines, 4, 10))


if __name__ == "__main__":
    main()

# year 2023
# solution for 17.01: 942
# solution for 17.02: 1082
