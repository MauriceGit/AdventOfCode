#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def main():

    lines = open_data("18.data")

    field = dict()
    for l in lines:
        field[tuple(ints(l))] = 1

    count = 0
    possible_pockets = set()
    for k in field:
        for d in dir_list_3D_6():
            if add(k,d) not in field:
                count += 1
                possible_pockets.add(add(k,d))

    print(count)

    def get_neighbors(state, pos):
        for d in dir_list_3D_6():
            if add(pos, d) not in state["field"]:
                yield add(pos, d)

    def visit(state, pos, dist, path):
        state["visited"].add(pos)
        return True

    pockets = set()
    while len(possible_pockets) > 0:
        p = possible_pockets.pop()
        state = {"field": field, "visited": set()}
        if dijkstra(p, get_neighbors, state=state, visit=visit, end_pos=(0,0,0))[1] == None:
            pockets = pockets.union(state["visited"])
        possible_pockets = possible_pockets-state["visited"]

    print(count - sum(add(p,d) in field for p in pockets for d in dir_list_3D_6()))


if __name__ == "__main__":
    main()

# year 2022
# solution for 18.01: 3496
# solution for 18.02: 2064
