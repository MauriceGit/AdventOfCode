#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *

from scipy.spatial import KDTree


def main():

    lines = open_data("20.data")
    f = dict()
    start = (0,0)
    end = (0,0)
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == "#":
                f[(x,y)] = "#"
            if c == "S":
                start = (x,y)
            if c == "E":
                end = (x,y)


    def get_neighbors(state, pos):
        for d in dir_list_4():
            if add(pos, d) not in f:
                yield add(pos, d)

    _, dist, path = dijkstra(start, get_neighbors, end_pos=end, use_path=True)
    #draw(f | {p:"█" for p in path}, print_directly=True)

    dists = dict()
    for i, p in enumerate(path):
        dists[p] = dist-i

    c = 0
    for p in path:
        for d in dir_list_4():
            cheat = add(p, mul(d, 2))
            if cheat in dists and dists[p]-dists[cheat] >= 102:
                c += 1
    print(c)

    tree = KDTree(path)
    count = 0
    for i, p in enumerate(path):
        _dists, _indices = tree.query(p, k=600, p=1, distance_upper_bound=21)
        count += sum(i<=ii<=dist and dists[p]-dists[path[ii]] >= 100+int(_dists[j]) for j,ii in enumerate(_indices))
    print(count)


if __name__ == "__main__":
    main()

# year 2024
# solution for 20.01: 1395
# solution for 20.02: 993178
