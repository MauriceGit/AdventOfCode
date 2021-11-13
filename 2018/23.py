#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *


def dist(b1, b2=(0,0,0)):
    s = sub(b1, b2)
    return abs(s[0])+abs(s[1])+abs(s[2])


def min_max_dist(b):
    l = []
    for v in [-b[1], b[1]]:
        l.append(dist(add(b[0], (v,0,0))))
        l.append(dist(add(b[0], (0,v,0))))
        l.append(dist(add(b[0], (0,0,v))))
    return min(l), max(l)


# This will NOT give a general correct answer for all possible variations of this problem!
# It does however work for the highly nested nature of this days task.
# And thats good enough for now!
def linear_search(nanobots):

    # [(min_dist, max_dist)]
    dists = sorted([min_max_dist(b) for b in nanobots])

    max_overlap = None
    max_count = 0

    for i, d in enumerate(dists):
        overlap = d
        count = 1
        for d2 in dists[i:]:
            if d2[0] > overlap[1]:
                break
            overlap = (max(overlap[0], d2[0]), min(overlap[1], d2[1]))
            count += 1
            if max_count == 0 or count > max_count:
                max_overlap = overlap
                max_count = count

    return max_overlap[0]


def main():

    lines = open_data("23.data")

    nanobots = []
    for l in lines:
        x,y,z,r = ints(l)
        nanobots.append(((x,y,z), r))

    best_bot = max(nanobots, key=lambda x: x[1])

    print(sum(dist(b[0], best_bot[0]) <= best_bot[1] for b in nanobots))
    print(linear_search(nanobots))


if __name__ == "__main__":
    main()

# year 2018
# solution for 23.01: 935
# solution for 23.02: 138697281
