#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *


def main():

    lines = open_data("25.data")
    points = lmap(tuple, map(ints, lines))

    graph = nx.Graph()
    for p in points:
        for p2 in points:
            if manhatten_dist(p, p2) <= 3:
                graph.add_edge(p, p2)

    print(len(list(nx.connected_components(graph))))


if __name__ == "__main__":
    main()

# year 2018
# solution for 25.01: 367
# solution for 25.02: *
