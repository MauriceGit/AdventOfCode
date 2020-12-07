#!/usr/bin/env python3.7

from utility import *
import networkx as nx
import re

def get_weight(graph, path):
    w = 1
    for i in range(1, len(path)):
        w *= graph.get_edge_data(path[i-1], path[i])["weight"]
    return w

def main():

    lines = open_data("07.data")
    graph1 = nx.DiGraph()
    graph2 = nx.DiGraph()

    for l in lines:
        s, t = l.split(" bags contain ")
        t = t[:-1].split(", ")

        if t[0] == "no other bags":
            continue

        for bag in t:
            r = re.match(r"(\d+) (.*) (bag|bags)$", bag)
            #print(bag, t)
            count  = int(r.group(1))
            target = r.group(2)

            graph1.add_edge(target, s)
            graph2.add_edge(s, target, weight=count)

            #print(s, "-->", target)


    print(len(nx.single_source_shortest_path_length(graph1, "shiny gold"))-1)

    #print(nx.single_source_shortest_path(graph2, "shiny gold"))
    #print(nx.single_source_dijkstra(graph2, "shiny gold"))

    count = 0
    for n in graph2.nodes():
        path_count = 1
        if len(graph2.edges(n)) == 0 and nx.has_path(graph2, "shiny gold", n):
            print(n)
            print(graph1.edges(n))
            # reverse direction
            for e in graph1.edges(n):

                if not nx.has_path(graph2, "shiny gold", e[1]):
                    continue

                print("  ", e)
                print("  ", graph2.get_edge_data(e[1],e[0])["weight"])

                path_count *= graph2.get_edge_data(e[1],e[0])["weight"]

        count += path_count
    print(count)

    #_, paths = nx.single_source_dijkstra(graph2, "shiny gold")
    #for k in paths:
    #
    #    edges = list(paths[k])
    #    print(k, edges)
    #
    #    #print(graph2.get_edge_data("shiny gold", "dark olive")["weight"])
    #
    #    #print(k, graph2.edge(k))
    #    # only count end-nodes!
    #    if len(list(graph2.edges(k))) == 0:
    #        print(edges)
    #        print(get_weight(graph2, edges))



if __name__ == "__main__":
    main()

# solution for 07.01: 164
# solution for 07.02: ´?
