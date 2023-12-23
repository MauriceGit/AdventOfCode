#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *

slope_dir = dict(zip("><v^", dir_list_4()))

def connected(f, p1, p2, branches):
    nodes = set(branches.keys())

    def get_neighbors(state, pos):
        positions = []
        for d in dir_list_4():
            new_p = add(pos, d)
            if new_p in state and state[new_p] != "#":
                if new_p not in nodes-{p1,p2}:
                    positions.append(new_p)
        return positions

    return dijkstra(p1, get_neighbors, end_pos=p2, state=f, use_path=True)[1]

def main():

    lines = open_data("23.data")
    f = dict()
    start_pos = (1,0)
    end_pos = (len(lines[0])-2, len(lines)-1)

    graph = nx.DiGraph()

    for y,line in enumerate(lines):
        for x,c in enumerate(line):
            f[(x,y)] = c
            if c == "#":
                continue
            if c in "<>^v":
                graph.add_edge((x,y), add((x,y),slope_dir[c]))
                continue
            for d in dir_list_4():
                new_p = add((x,y), d)
                if 0 <= new_p[0] < len(lines[0]) and 0 <= new_p[1] < len(lines) and lines[new_p[1]][new_p[0]] != "#":
                    graph.add_edge((x,y), new_p)

    print(max(map(len, nx.all_simple_paths(graph, start_pos, end_pos)))-1)


    reduced_field = dict()
    for p in f:
        if f[p] != "#" and sum(f[add(p, d)] != "#" for d in dir_list_4() if add(p,d) in f) != 2:
            reduced_field[p] = []

    distances = dict()
    for b1 in reduced_field.keys():
        for b2 in reduced_field.keys():
            if b1 != b2:
                dist = connected(f, b1, b2, reduced_field)
                if dist is not None:
                    reduced_field[b1].append(b2)
                    distances[(b1, b2)] = dist

    graph = nx.Graph()
    for p1 in reduced_field:
        for p2 in reduced_field[p1]:
            graph.add_edge(p1, p2, weight=distances[(p1, p2)])

    def get_path_length(path):
        return sum(distances[(path[i-1], path[i])] for i in range(1, len(path)))

    print(max(map(get_path_length, nx.all_simple_paths(graph, start_pos, end_pos))))



if __name__ == "__main__":
    main()

# year 2023
# solution for 23.01: 2050
# solution for 23.02: 6262
