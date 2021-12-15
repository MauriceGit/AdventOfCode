#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *

def fill_field(lines, field, x_diff, y_diff, increase):
    for y,l in enumerate(lines):
        for x,v in enumerate(l):
            print(field == None)
            field[(x+x_diff,y+y_diff)] = (int(v)+increase)%9

def main():

    lines = open_data("15.data")

    field = defaultdict(lambda: 1000)
    for y,l in enumerate(lines):
        for x,v in enumerate(l):
            field[(x,y)] = int(v)
    w = len(lines[0])
    h = len(lines)

    fold = 5
    for i in range(fold):
        for j in range(fold):
            field = fill_field(lines, field, i*w, j*h, i+j)

    w *= fold
    h *= fold

    graph = nx.DiGraph()

    for y in range(h):
        for x in range(w):
            pos = (x,y)
            for d in dir_list_4():
                new_pos = add(pos, d)
                graph.add_edge(pos, new_pos, weight=field[new_pos])
                graph.add_edge(new_pos, pos, weight=field[pos])

    shortest_path_length = nx.shortest_path_length(graph, (0,0), (w-1,h-1), weight='weight')
    #shortest_path = nx.shortest_path(graph, (0,0), (w-1,h-1), weight='weight')

    print(shortest_path_length)



if __name__ == "__main__":
    main()

# year 2021
# solution for 15.01: 447
# solution for 15.02: ?
