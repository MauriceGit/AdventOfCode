
############################### Useful imports

from functools import lru_cache

import re

from collections import defaultdict, Counter
# Counter() creates a dictionary with "elem: count" for each element in the list.

from fractions import gcd

from recordtype import recordtype
# example: Planet = recordtype("Planet", "p v")

import math
# example: math.ceil()

from itertools import repeat, chain, islice, accumulate, permutations, combinations
# examples:
#
# accumulate([1,2,3,4,5]) --> 1 3 6 10 15
#
# islice('ABCDEFG', 2) --> A B
# islice('ABCDEFG', 2, 4) --> C D
# islice('ABCDEFG', 2, None) --> C D E F G
# islice('ABCDEFG', 0, None, 2) --> A C E G
#
# chain('ABC', 'DEF') --> A B C D E F
#
# repeat(10, 3) --> 10 10 10
#
# permutations('ABCD', 2) --> AB AC AD BA BC BD CA CB CD DA DB DC
#
# combinations('ABCD', 2) --> AB AC AD BC BD CD

import networkx as nx
from networkx.algorithms.shortest_paths.weighted import single_source_dijkstra
#
# graph = nx.Graph()
# add_surrounding_edge(graph, ...)
#
# nx.shortest_path_length(graph, node1, node2)
#
# nx.shortest_path(graph, node1, node2)
#
# step_count, steps = single_source_dijkstra(graph, "AA", "ZZ")
#

from threading import Thread
from queue import Queue
#
# t = Thread(target=function, args=())
# t.start()
# t.join()
#
# q = Queue(maxsize=0) --> blocking queue
# q.empty(), q.get(), q.put(...)


############################### Vector calculations

# Adds, but with 3 coordinates
def add3(a,b):
    return (a[0]+b[0], a[1]+b[1], a[2]+b[2])

def add(p, p2):
    return (p[0]+p2[0], p[1]+p2[1])

def mul(p, s):
    return (p[0]*s, p[1]*s)

def sub(p, p2):
    return (p2[0]-p[0], p2[1]-p[1])

def div(p, f):
    return (p[0]//f if f else 0, p[1]//f if f else 0)

# Returns a dictionary of number/letter -> direction vector. For reading direction strings directly.
def direction_map(direction=None):
    if direction == None:
        return dict(zip("RLUD", [(1,0), (-1,0), (0,1), (0,-1)]))
    return dict(zip(direction, [(1,0), (-1,0), (0,1), (0,-1)]))

@lru_cache(maxsize=10)
def dir_list_4():
    return [(1,0), (-1,0), (0,1), (0,-1)]

@lru_cache(maxsize=10)
def dir_list_8():
    return dir_list_4() + [(1,1), (-1,-1), (-1,1), (1,-1)]

# Takes a direction tuple and rotates it in 2D in the given direction
# ignores a count=0 and still rotates at least once!
def rotate(d, left, count=1):
    r = (-d[1], d[0]) if left else (d[1], -d[0])
    if count > 1:
        return rotate(r, left, count-1)
    return r

############################### Graph things

# Adds edge from p in direction d, if there is a node at p+d
def add_edge(graph, p, d):
    if add(p, d) in graph:
        graph.add_edge(p, add(p, d), weight=1)
    else:
        graph.add_node(p)

# Adds edges to all neighbors (if there are any)
def add_surrounding_edge(graph, p):
    add_edge(graph, p, ( 1,0))
    add_edge(graph, p, (-1,0))
    add_edge(graph, p, (0, 1))
    add_edge(graph, p, (0,-1))

############################### Other

# compare like in C. -1, 0, 1
def cmp(x1, x2):
    return 0 if x1 == x2 else 1 if x2-x1 > 0 else -1


# Least common multiplier
def lcm(a,b):
    return (a*b)//gcd(a,b)

def lmap(f, *iterables):
    return list(map(f, *iterables))

def ints(s):
    if type(s) == str:
        return lmap(int, re.findall(r"-?\d+", s))
    if type(s) == list:
        return lmap(int, s)

def floats(s):
    if type(s) == str:
        return lmap(float, re.findall(r"-?\d+(?:\.\d+)?", s))
    if type(s) == list:
        return lmap(float, s)

############################### IO

# Return .data file split up for each line
def open_data(filename, no_filter=False):
    with open(filename, "r") as f:
        if no_filter:
            return f.read().splitlines()
        return list(filter(lambda x: not x.startswith("//") and not x.strip() == "", f.read().splitlines()))

# Returns groups of lines divided by an empty line
def open_data_groups(filename, no_filter=False):

    groups = open("06.data", "r").read().split("\n\n")
    groups = lmap(lambda x: x.splitlines(), groups)

    if no_filter:
        return groups

    def filter_(g):
        return list(filter(lambda x: not x.startswith("//") and not x.strip() == "", g))

    return lmap(filter_, groups)

# Can draw a 2D-map of coordinates -> something in dictionary form.
# Requires a dict of: (int, int): char
def draw(f, symbols=None, print_directly=False, flip=False):

    if symbols == None:
        symbols = {-1: "█", 0: "█", 1: " ", 2: "0", 3: "#", 4: "X"}

    min_x = min(f.keys(), key=lambda x: x[0])[0]
    min_y = min(f.keys(), key=lambda x: x[1])[1]
    max_x = max(f.keys(), key=lambda x: x[0])[0]
    max_y = max(f.keys(), key=lambda x: x[1])[1]

    y_range = range(min_y, max_y+1)
    if flip:
        y_range = reversed(y_range)

    for y in y_range:
        for x in range(min_x, max_x+1):

            p = (x,y)
            if p not in f:
                c = -1
            else:
                c = f[p]

            if c not in symbols:
                if print_directly:
                    symbols[c] = c
                else:
                    symbols[c] = "?"

            print(symbols[c], end="")

        print("")
    print("")
