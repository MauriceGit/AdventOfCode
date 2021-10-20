#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *


# returns (target, path) for the closest target
def closest_target(orig_graph, units, current_index):

    all_paths = []
    for i,t in enumerate(units):
        if i == current_index or units[current_index][2] == t[2]:
            continue

        # so that we can't run through other players
        graph = orig_graph.copy()
        graph.remove_nodes_from([x[0] for j,x in enumerate(units) if current_index != j and j != i])
        try:
            paths = list(nx.all_shortest_paths(graph, units[current_index][0], t[0]))
            paths.sort(key=lambda x: (len(x), x[0][1], x[0][0]))
            all_paths.append(paths[0])
        except Exception as e:
            pass

    all_paths.sort(key=lambda x: (len(x), x[0][1], x[0][0]))

    # first node is the current node, last node is the target node!
    # leave the target node in so we know where enemies are
    return [] if len(all_paths) == 0 else all_paths[0][1:][:-1]

def length2(p):
    return abs(p[0]) + abs(p[1])

def get_inrange_target(p, units, team):
    t_index = -1
    for i, u in enumerate(units):
        if u[2] != team and length2(sub(u[0], p)) == 1 and (t_index == -1 or u[1] < units[t_index][1]):
            t_index = i
    return t_index


def run_round(graph, units):

    i = 0
    while i < len(units):
        u = units[i]

        if all(x[2] == units[0][2] for x in units):
            return False

        path = closest_target(graph, units, i)
        if len(path) > 0:
            units[i][0] = path[0]

        target_index = get_inrange_target(units[i][0], units, u[2])
        if target_index != -1:
            units[target_index][1] -= 3
            if units[target_index][1] <= 0:
                del units[target_index]
                if target_index < i:
                    continue
        i += 1

    return True



def run(lines):
    graph = nx.Graph()
    # (pos, health, team)
    units = []

    for y, l in enumerate(lines):
        for x, c in enumerate(l):
            if c != "#":
                graph.add_node((x,y))
                add_surrounding_edge(graph, (x,y))
                if c in "GE":
                    units.append([(x,y), 200, c == "E"])

    rounds = 0
    while True:
        units.sort(key=lambda x: (x[0][1], x[0][0]))
        print(units)
        if not run_round(graph, units):
            break
        rounds += 1

    print(units)
    print(rounds)
    print((rounds) * sum(x[1] for x in units))


def main():

    groups = open_data_groups("15.data")

    for g in groups:
        run(g)
        print()




if __name__ == "__main__":
    main()

# year 2018
# solution for 15.01: ?
# solution for 15.02: ?
