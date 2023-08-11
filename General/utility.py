
############################### Useful imports

from collections import namedtuple

import functools
from functools import lru_cache, reduce, cmp_to_key

import operator
# operator.mul clashes with my own mul function further down. So it needs
# to be imported as operator.mul for clarity!
from operator import itemgetter

from json import loads

from enum import Enum, IntEnum

import hashlib
# md5 = hashlib.md5()
# md5.update("abc".encode())
# h = md5.hexdigest()

import re

from copy import deepcopy

import numpy as np

from collections import defaultdict, Counter, deque
# Counter() creates a dictionary with "elem: count" for each element in the list.
#
# deque: --> doubly linked list!
# append, appendleft, rotate(n=1), pop, popleft. Can be accessed just like a list with []!

from recordtype import recordtype
# example: Planet = recordtype("Planet", "p v")

import heapq
from heapq import heapify, heappop, heappush
# queue = [(dist, pos, ...)]
# heapify(queue)
# dist, pos = heappop(queue)
# heappush(queue, (dist, new_pos))

import math
from math import sin, cos, ceil
# example: math.ceil()

import itertools
from itertools import repeat, chain, islice, accumulate, permutations, combinations, count, product
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
#
# for i in itertools.count():
#    unbounded for loop! With index assigned to i. Awesome!

from more_itertools import set_partitions
# set_partitions can divide a list into n partitions with all possible combinations.
# Example:
# list(set_partitions([2,3,4], 2)) --> [[[2], [3, 4]], [[2, 3], [4]], [[3], [2, 4]]]

import networkx as nx
from networkx.algorithms.shortest_paths.weighted import single_source_dijkstra
#
# graph = nx.Graph()
# graph = nx.DiGraph() # Creates a directed graph!!!
# add_surrounding_edge(graph, ...)
#
# nx.shortest_path_length(graph, node1, node2)
#
# nx.all_shortest_paths(graph, node1, node2)
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


# CHINESE REMAINDER THEOREM. Make sure to substract the result[0] from result[1]:
# result = result[1]-result[0]
from sympy.ntheory.modular import crt

from cachetools import cached, LRUCache
from cachetools.keys import hashkey
#
# @cached(cache, key=lambda rules, rule: hashkey(rule))
# def combine_rules(rules, rule): ...

############################### Vector calculations

def add(p, p2):
    return tuple(p[i]+p2[i] for i in range(len(p)))

def mul(p, s):
    return tuple(x*s for x in p)

def sub(p, p2):
    return tuple(p[i]-p2[i] for i in range(len(p)))

def div(p, f):
    return tuple(x/f if f else 0 for x in p)

def length(p):
    return math.sqrt(sum(p[i]*p[i] for i in range(len(p))))

def rad_to_deg(a):
    return a*180/math.pi

def deg_to_rad(a):
    return a*math.pi/180

def manhatten_length(p):
    return sum(map(abs, p))

def manhatten_dist(p1, p2):
    return manhatten_length(sub(p1, p2))

# Returns a dictionary of number/letter -> direction vector. For reading direction strings directly.
def direction_map(direction=None):
    if direction == None:
        return dict(zip("RLDU", [(1,0), (-1,0), (0,1), (0,-1)]))
    return dict(zip(direction, [(1,0), (-1,0), (0,1), (0,-1)]))

@lru_cache(maxsize=10)
def dir_list_4():
    return [(1,0), (-1,0), (0,1), (0,-1)]

@lru_cache(maxsize=10)
def dir_list_8():
    return dir_list_4() + [(1,1), (-1,-1), (-1,1), (1,-1)]

@lru_cache(maxsize=10)
def dir_list_3D_6():
    return [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]

# Takes a direction tuple and rotates it in 2D in the given direction
# ignores a count=0 and still rotates at least once!
def rotate(d, left, count=1):
    if count == 0:
        return d
    r = (-d[1], d[0]) if left else (d[1], -d[0])
    if count > 1:
        return rotate(r, left, count-1)
    return r

############################### Graph things

# Adds edge from p in direction d, if there is a node at p+d
def add_edge(graph, p, d):
    if p not in graph:
        graph.add_node(p)
    if add(p, d) in graph:
        graph.add_edge(p, add(p, d), weight=1)

# Adds edges to all neighbors (if there are any)
def add_surrounding_edge(graph, p):
    add_edge(graph, p, ( 1,0))
    add_edge(graph, p, (-1,0))
    add_edge(graph, p, (0, 1))
    add_edge(graph, p, (0,-1))


# get_neighbors:    Function with state and current_pos as parameters: get_neighbors(state, pos)
# state:            Most likely just the field that contains the graph. Could also be a tuple that contains more information!
# edge_cost:        Function with state, current_pos and next_pos as parameters: edge_cost(state, pos, next_pos)
# visit:            Function that gets called for every single node that gets reached (with minimum distance).
#                   It expects state, pos, dist and path as parameters: visit(state, pos, dist, path)
#                   visit() should return True to continue searching and False to stop visiting further nodes!
# use_path:         True, if you need the actual shortest path from start to end. Will impact runtime!
#                   Otherwise, the returned path will always be []
def dijkstra(start_pos, get_neighbors, state=None, edge_cost=None, end_pos=None, visit=None, use_path=False, revisit_nodes=False):

    visited = set()
    queue = [(0, start_pos, [start_pos] if use_path else [])]
    heapify(queue)

    while len(queue) > 0:
        dist, pos, path = heappop(queue)

        if not revisit_nodes:
            if pos in visited:
                continue

            visited.add(pos)

        if visit is not None and not visit(state, pos, dist, path):
            return pos, dist, path

        if end_pos is not None and pos == end_pos:
            return pos, dist, path

        for new_pos in get_neighbors(state, pos):
            cost = 1 if edge_cost is None else edge_cost(state, pos, new_pos)
            new_path = [] if not use_path else path + [new_pos]
            heappush(queue, (dist+cost, new_pos, new_path))

    return None, None, None

############################### Other

# compare like in C. -1, 0, 1
def cmp(x1, x2):
    return 0 if x1 == x2 else 1 if x2-x1 > 0 else -1


# Least common multiplier
def lcm(a,b):
    return (a*b)//math.gcd(a,b)

def lmap(f, *iterables):
    return list(map(f, *iterables))

def lfilter(f, *iterables):
    return list(filter(f, *iterables))

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

# turns a list of tuples into lists with each element
# [(1,2),(3,4),(5,6)] --> [[1, 3, 5], [2, 4, 6]]
def unzip(l):
    return lmap(list, zip(*l))

# Credit to: https://stackoverflow.com/questions/16996217/prime-factorization-list
# Careful: This function omits 1 and n from the list (which is correct, but still!)
def prime_factors(n):
    l = []
    if n < 2: return l
    if n&1==0:
        l.append(2)
        while n&1==0: n>>=1
    i = 3
    m = int(math.sqrt(n))+1
    while i < m:
        if n%i==0:
            l.append(i)
            while n%i==0: n//=i
        i+= 2
        m = int(math.sqrt(n))+1
    if n>2: l.append(n)
    return l

############################### IO

# Return .data file split up for each line
def open_data(filename, no_filter=False):
    with open(filename, "r") as f:
        if no_filter:
            return f.read().splitlines()
        return list(filter(lambda x: not x.startswith("//") and not x.strip() == "", f.read().splitlines()))

# Returns groups of lines divided by an empty line
def open_data_groups(filename, no_filter=False):

    groups = open(filename, "r").read().split("\n\n")
    groups = lmap(lambda x: x.splitlines(), groups)

    if no_filter:
        return groups

    def filter_(g):
        return list(filter(lambda x: not x.startswith("//") and not x.strip() == "", g))

    return lmap(filter_, groups)

#def _get_char(characters, start, end):
#
#
#
#def ocr(characters):
#
#    # Characters are always 4 chars wide and 6 chars large!
#    if type(characters) == list and type(characters[0]) == str:
#        substr
#


# Can draw a 2D-map of coordinates -> something in dictionary form.
# Requires a dict of: (int, int): char
def draw(f, symbols=None, print_directly=False, flip=False):

    if symbols == None:
        symbols = {-1: ".", 0: " ", 1: "#", 2: "█", 3: "■", 4: "ʘ"}

    min_x = min(f.keys(), key=lambda x: x[0])[0]
    min_y = min(f.keys(), key=lambda x: x[1])[1]
    max_x = max(f.keys(), key=lambda x: x[0])[0]
    max_y = max(f.keys(), key=lambda x: x[1])[1]

    y_range = range(min_y, max_y+1)
    if flip:
        y_range = reversed(y_range)

    for y in y_range:
        for x in range(min_x, max_x+1):
            if (x,y) not in f:
                c = symbols[-1] if -1 in symbols else "."
            else:
                c = f[(x,y)]

            if print_directly or c not in symbols:
                symbols[c] = c
            print(symbols[c], end="")
        print("")
    print("")

def draw_direct(f, flip=False):
    draw(f, print_directly=True, flip=flip)
