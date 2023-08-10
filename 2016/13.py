#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def main():

    office = int(open_data("13.data")[0])

    def get_neighbors(state, pos):
        neighbors = []
        for d in dir_list_4():
            tmp = add(pos, d)
            n = tmp[0]*tmp[0] + 3*tmp[0] + 2*tmp[0]*tmp[1] + tmp[1] + tmp[1]*tmp[1] + office
            if tmp[0] >= 0 and tmp[1] >= 0 and n.bit_count() % 2 == 0:
                neighbors.append(tmp)
        return neighbors

    print(dijkstra((1,1), get_neighbors, end_pos=(31,39))[1])

    def visit(state, pos, dist, path):
        if dist > 50:
            return False
        state.add(pos)
        return True

    positions = set()
    dijkstra((1,1), get_neighbors, state=positions, visit=visit)

    print(len(positions))


if __name__ == "__main__":
    main()

# year 2016
# solution for 13.01: 90
# solution for 13.02: 135
