#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *


def valid_part_1(path):
    c = Counter(path)
    return max(c.values()) <= 1


def valid_part_2(path):
    c = Counter(path)
    tmp = [v for v in c.values() if v >= 2]
    return max(c.values()) <= 2 and len(tmp) <= 1


def find_paths_dfs(graph, current_node, path, valid):

    if current_node == "end":
        return 1

    count = 0
    for next_node in graph[current_node]:
        new_path = path + [next_node] if next_node.islower() else path
        if next_node != "start" and valid(new_path):
            count += find_paths_dfs(graph, next_node, new_path, valid)
    return count


def main():

    lines = open_data("12.data")

    graph = defaultdict(list)
    for l in lines:
        s, d = l.split("-")
        graph[s].append(d)
        graph[d].append(s)

    print(find_paths_dfs(graph, "start", ["start"], valid_part_1))
    print(find_paths_dfs(graph, "start", ["start"], valid_part_2))


if __name__ == "__main__":
    main()

# year 2021
# solution for 12.01: 4338
# solution for 12.02: 114189
