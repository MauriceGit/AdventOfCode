#!/usr/bin/env python3.7

from utility import *
import networkx as nx
import re

def get_count(graph, node):
    count = 1
    for e in graph.edges(node):
        w = graph.get_edge_data(e[0], e[1])["weight"]
        w_rec = get_count(graph, e[1])
        count += w*w_rec
    return count

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
            count  = int(r.group(1))
            target = r.group(2)

            graph1.add_edge(target, s)
            graph2.add_edge(s, target, weight=count)

    print(len(nx.single_source_shortest_path_length(graph1, "shiny gold"))-1)
    print(get_count(graph2, "shiny gold")-1)

if __name__ == "__main__":
    main()

# solution for 07.01: 164
# solution for 07.02: 7872
