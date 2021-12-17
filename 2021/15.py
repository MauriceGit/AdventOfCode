#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *


def fill_field(lines, field, x_diff, y_diff, increase):
    for y,l in enumerate(lines):
        for x,v in enumerate(l):
            value = (int(v)+increase)%10
            value += 1 if int(v)+increase >= 10 else 0
            field[(x+x_diff,y+y_diff)] = value


def create_field(lines, repeat=1):
    field = defaultdict(lambda: 1000)
    w = len(lines[0])
    h = len(lines)
    for i in range(repeat):
        for j in range(repeat):
            fill_field(lines, field, i*w, j*h, i+j)
    w *= repeat
    h *= repeat
    return field, w, h


def get_neighbors(state, p):
    return [add(p, d) for d in dir_list_4()]


def edge_cost(state, p, p2):
    if p2 not in state:
        return 1000
    return state[p2]


def main():

    lines = open_data("15.data")

    field1, w1, h1 = create_field(lines, repeat=1)
    field2, w2, h2 = create_field(lines, repeat=5)

    _, dist1, _ = dijkstra((0,0), get_neighbors, state=field1, end_pos=(w1-1,h1-1), edge_cost=edge_cost)
    _, dist2, _ = dijkstra((0,0), get_neighbors, state=field2, end_pos=(w2-1,h2-1), edge_cost=edge_cost)
    print(dist1)
    print(dist2)


if __name__ == "__main__":
    main()

# year 2021
# solution for 15.01: 447
# solution for 15.02: 2825
