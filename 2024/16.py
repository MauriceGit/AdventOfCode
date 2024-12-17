#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *

def part1(f, start, end):
    def get_neighbors(state, pos):
        if add(pos[0], pos[1]) not in f:
            yield (add(pos[0], pos[1]), pos[1])
        yield (pos[0], rotate(pos[1], True))
        yield (pos[0], rotate(pos[1], False))

    def visit(state, pos, dist, path):
        return pos[0] != end
    def edge_cost(state, pos, next_pos):
        if pos[0] != next_pos[0]:
            return 1
        return 1000

    return dijkstra(start, get_neighbors, edge_cost=edge_cost, visit=visit)[1]

def get_neighbors(paths, p):
    return [add(p, d) for d in dir_list_4() if add(p, d) in paths]

def neighbor_count(paths, p):
    return len(get_neighbors(paths, p))

def is_corner(paths, p):
    c = neighbor_count(paths, p)
    return c > 2 or c == 2 and (add(p, (-1,0)) in paths) != (add(p, (1,0)) in paths)

def find_next_corners(paths, nodes, p):
    corners = []
    for next_p in get_neighbors(paths, p):
        d = sub(next_p, p)
        l = [p, next_p]
        while True:
            # hit an intersection on the way!
            if next_p in nodes:
                corners.append((next_p, l.copy()))
            tmp = add(next_p, d)
            if tmp not in paths:
                break
            next_p = tmp
            l.append(next_p)

        if neighbor_count(paths, next_p) > 1:
            corners.append((next_p, l))
    return corners

def main():

    lines = open_data("16.data")

    f = dict()
    paths = dict()
    end = (0,0)
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == "#":
                f[(x,y)] = "#"
            else:
                paths[(x,y)] = "."
            if c == "S":
                start = (x,y)
            if c == "E":
                end = (x,y)
    # (pos, dir)
    start = (start, (1,0))

    print(part1(f, start, end))

    edge_cost = dict()
    nodes = set()
    edge_paths = dict()

    nx_graph = nx.Graph()

    for p in paths:
        if is_corner(paths, p) or p in [start[0], end]:
            nodes.add(p)

    for n in nodes:
        for n2, path in find_next_corners(paths, nodes, n):
            edge_cost[(n, n2)] = max(map(abs, sub(n2, n)))
            edge_paths[(n, n2)] = path
            nx_graph.add_edge(n, n2)

    def path_cost(path):
        return sum([edge_cost[pair] for pair in itertools.pairwise(path)])

    all_paths = list(nx.all_shortest_paths(nx_graph, start[0], end))
    min_cost = min(path_cost(path) for path in all_paths)
    # Only the real shortest paths! (Not just fewest corners!)
    all_paths = lfilter(lambda x: path_cost(x) == min_cost, all_paths)

    s = set()
    for path in all_paths:
        for pair in itertools.pairwise(path):
            s |= set(edge_paths[pair])
    print(len(s))


if __name__ == "__main__":
    main()

# year 2024
# solution for 16.01: 143564
# solution for 16.02: 593
