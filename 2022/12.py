#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def main():

    lines = open_data("12.data")

    grid = dict()
    start = (0,0)
    end = (0,0)
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == "S":
                start = (x,y)
                grid[(x,y)] = 0
            elif c == "E":
                end = (x,y)
                grid[(x,y)] = -1
            else:
                grid[(x,y)] = ord(c)-97

    def neighbors(state, pos):
        return (add(pos, d) for d in dir_list_4() if add(pos, d) in state and state[add(pos, d)]-state[pos] <= 1)

    print(dijkstra(start, neighbors, state=grid, end_pos=end)[1])

    def neighbors_reverse(state, pos):
        return (add(pos, d) for d in dir_list_4() if add(pos, d) in state and state[pos]-state[add(pos, d)] <= 1)

    # only visit nodes until any 'a'-node is found
    def visit(state, pos, dist, path):
        return state[pos] != 0

    print(dijkstra(end, neighbors_reverse, state=grid, visit=visit)[1])


if __name__ == "__main__":
    main()

# year 2022
# solution for 12.01: 420
# solution for 12.02: 414
