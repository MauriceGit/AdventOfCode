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


def create_graph_from_field(field, w, h):
    graph = nx.DiGraph()
    for y in range(h):
        for x in range(w):
            pos = (x,y)
            for d in dir_list_4():
                new_pos = add(pos, d)
                graph.add_edge(pos, new_pos, weight=field[new_pos])
                graph.add_edge(new_pos, pos, weight=field[pos])
    return graph


def calc_best_path(lines, repeat=1):
    field, w, h = create_field(lines, repeat=repeat)
    graph = create_graph_from_field(field, w, h)
    return nx.shortest_path_length(graph, (0,0), (w-1,h-1), weight='weight')


def main():

    lines = open_data("15.data")

    print(calc_best_path(lines))
    print(calc_best_path(lines, repeat=5))


if __name__ == "__main__":
    main()

# year 2021
# solution for 15.01: 447
# solution for 15.02: 2825
