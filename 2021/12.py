#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *
from copy import deepcopy



def is_invalid(visited, visit_at_most):
    tmp = lfilter(lambda x: x >= visit_at_most, visited.values())
    return visited["start"] > 2 or max(visited.values()) > 2 or len(tmp) > 1


def find_paths(graph, visit_at_most):

    # current_node, last_node, visited
    queue = [("start", defaultdict(int, {"start": 1}))]
    found_paths = 0
    all_paths = []

    while len(queue) > 0:
        node, visited = queue.pop(0)

        if node == "end":
            found_paths += 1
            continue

        if node.islower():
            visited[node] += 1

        for next_node in graph[node]:

            if next_node == "start" or next_node in visited and is_invalid(visited, visit_at_most):
                continue

            queue.append((next_node, visited.copy()))

    return found_paths


def main():

    lines = open_data("12.data")

    graph = defaultdict(list)
    for l in lines:
        s, d = l.split("-")
        graph[s].append(d)
        graph[d].append(s)

    print(find_paths(graph, 1))
    print(find_paths(graph, 2))


if __name__ == "__main__":
    main()

# year 2021
# solution for 12.01: ?
# solution for 12.02: ?
