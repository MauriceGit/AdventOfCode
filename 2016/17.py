#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def visit(state, pos, dist, path):
    return pos[0] != (3,3)


def get_neighbors(state, pos):

    if state != None and pos[0] == (3,3):
        state.append(len(pos[1])-8)
        return []

    key = hashlib.md5(pos[1].encode()).hexdigest()
    # up
    if pos[0][1] > 0 and key[0] in "bcdef":
        yield (add(pos[0], (0,-1)), pos[1]+"U")
    # down
    if pos[0][1] < 3 and key[1] in "bcdef":
        yield (add(pos[0], (0,1)), pos[1]+"D")
    # left
    if pos[0][0] > 0 and key[2] in "bcdef":
        yield (add(pos[0], (-1,0)), pos[1]+"L")
    # right
    if pos[0][0] < 3 and key[3] in "bcdef":
        yield (add(pos[0], (1,0)), pos[1]+"R")


def main():

    passcode = open_data("17.data")[0]

    p, _, _ = dijkstra(((0,0), passcode), get_neighbors, visit=visit)
    print(p[1][8:])

    final_positions = []
    dijkstra(((0,0), passcode), get_neighbors, state=final_positions)
    print(max(final_positions))


if __name__ == "__main__":
    main()

# year 2016
# solution for 17.01: DURLDRRDRD
# solution for 17.02: 650
