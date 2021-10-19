#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *


def remove_nodes(graph, nodes, index):
    graph.remove_nodes_from([x[0] for i,x in enumerate(nodes) if index != i])

# returns (target, path) for the closest target
def closest_target(orig_graph, friends, current_friend, targets):

    dist = 1000000000
    best = ()

    all_paths = []

    for i,t in enumerate(targets):
        graph = orig_graph.copy()

        # so that we can't run through other players
        remove_nodes(graph, targets, i)
        remove_nodes(graph, friends, current_friend)

        try:
            paths = list(nx.all_shortest_paths(graph, friends[current_friend][0], t[0]))
            paths.sort(key=lambda x: (len(x), x[0][1], x[0][0]))
            all_paths.append(paths[0])
        except:
            pass

    all_paths.sort(key=lambda x: (len(x), x[0][1], x[0][0]))

    print(all_paths)


    return best



def run_round(graph, elfes, gnomes):
    closest_target(graph, elfes, 0, gnomes)


def main():

    lines = open_data("15.data")

    graph = nx.Graph()
    # (pos, health)
    elfes = []
    gnomes = []

    for y, l in enumerate(lines):
        for x, c in enumerate(l):
            if c != "#":
                graph.add_node((x,y))
                print("add ", (x,y))
                add_surrounding_edge(graph, (x,y))
                if c == "G":
                    gnomes.append(((x,y), 200))
                if c == "E":
                    elfes.append(((x,y), 200))

    #print(elfes)
    #print(gnomes)


    run_round(graph, elfes, gnomes)





if __name__ == "__main__":
    main()

# year 2018
# solution for 15.01: ?
# solution for 15.02: ?
