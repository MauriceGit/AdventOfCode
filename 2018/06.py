#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *

def positive(p):
    return (abs(p[0]), abs(p[1]))

def dist(p0, p1):
    return sum(positive(sub(p0, p1)))

# returns a tuple of the closest ID and the accumulated distance to all IDs
def all_dist(coords, p):
    d = 1000000
    min_i = -1
    d_all = 0
    for i, c in enumerate(coords):
        tmp = dist(c, p)
        if tmp == d:
            min_i = -1
        if tmp < d:
            min_i = i
            d = tmp
        d_all += tmp
    return (min_i, d_all)


def main():

    lines = open_data("06.data")

    coords = [tuple(ints(l)) for l in lines]

    min_x = min(coords, key=lambda x:x[0])[0]
    max_x = max(coords, key=lambda x:x[0])[0]
    min_y = min(coords, key=lambda x:x[1])[1]
    max_y = max(coords, key=lambda x:x[1])[1]

    d = defaultdict(lambda x: -1)

    for x in range(min_x, max_x+1):
        for y in range(min_y, max_y+1):
            d[(x,y)] = all_dist(coords, (x,y))

    invalid_ids = set()

    # Filter out all ids that occur on the edges. That means, that they
    # belong to an infinite region and do not count.
    for x in range(min_x, max_x+1):
        invalid_ids.update([d[(x, min_y)][0], d[(x, max_y)][0]])
    for y in range(min_y, max_y+1):
        invalid_ids.update([d[(min_x, y)][0], d[(max_x, y)][0]])

    c = Counter(dist[0] for dist in d.values())

    # Remove invalid ids from the counter.
    for k in c.keys():
        if k in invalid_ids:
            c[k] = 0

    print(max(c.values()))

    print(len(list(filter(lambda x: x < 10000, [dist[1] for dist in d.values()]))))


if __name__ == "__main__":
    main()

# year 2018
# solution for 06.01: 3010
# solution for 06.02: 48034
