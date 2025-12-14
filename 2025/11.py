#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def count_connections(connections, node, final_node, visited):
    if node == final_node:
        return 1
    if node in visited:
        return visited[node]

    res = sum(count_connections(connections, c, final_node, visited) for c in connections[node])
    visited[node] = res
    return res


def solve(connections, connection_list):
    conns = (count_connections(connections, n1, n2, dict()) for n1, n2 in pairwise(connection_list))
    return reduce(operator.mul, conns)


def main():

    lines = open_data("11.data")
    connections = dict()
    for line in lines:
        s = line.split(": ")
        connections[s[0]] = s[1].split(" ")
    connections["out"] = []

    print(solve(connections, ["you", "out"]))
    path1 = solve(connections, ["svr", "dac", "fft", "out"])
    path2 = solve(connections, ["svr", "fft", "dac", "out"])
    print(max(path1, path2))


if __name__ == "__main__":
    main()

# year 2025
# solution for 11.01: 724
# solution for 11.02: 473930047491888
