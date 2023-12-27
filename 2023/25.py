#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


# This could be solved cleaner/nicer by using my own dijkstra and just not generate the edges
# instead of removing and re-adding them every time...
def find_path(graph, n1, n2, exclude_edges):
    for e in exclude_edges:
        graph.remove_edge(*e)
    path = None
    if nx.has_path(graph, n1, n2):
        path = nx.shortest_path(graph, n1, n2)
    for e in exclude_edges:
        graph.add_edge(*e)
    return path


def main():

    lines = open_data("25.data")
    lines = lmap(lambda x: (x.split(": ")[0], x.split(": ")[1].split(" ")), lines)

    graph = nx.Graph()
    edges = []
    for line in lines:
        for component in line[1]:
            graph.add_edge(line[0], component)
            edges.append((line[0], component))

    # Between two nodes, find all paths that use only edges (nodes?) that it didn't use for the other paths yet!
    # If the number of distinct paths are exactly 3, the edge is to be removed! (Because this means, that the
    #    graph only has three possible ways to connect the nodes without re-using nodes/edges!
    #    That means, that the other two critical edges ore on the two paths we just found! (could be an optimization...)
    critical_edges = []
    for (n1, n2) in edges:
        exclude_edges = [(n1, n2)]
        count = 0
        for i in range(3):
            path = find_path(graph, n1, n2, exclude_edges)
            if path is not None:
                exclude_edges.extend([(path[i-1], path[i]) for i in range(1, len(path))])
                count += 1
        if count <= 2:
            critical_edges.append((n1, n2))

    for (n1, n2) in critical_edges:
        graph.remove_edge(n1, n2)

    print(reduce(operator.mul, (len(graph.subgraph(c).nodes()) for c in nx.connected_components(graph))))


if __name__ == "__main__":
    main()

# year 2023
# solution for 25.01: 598120
# solution for 25.02: *
