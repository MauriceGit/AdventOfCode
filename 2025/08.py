#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def main():

    boxes = lmap(lambda x: tuple(ints(x.split(","))), open_data("08.data"))
    boxes_set = set(range(len(boxes)))

    distances = dict()
    for i,b1 in enumerate(boxes):
        for j,b2 in enumerate(boxes):
            # so we don't have like (0,19) AND (19,0) in the dataset
            if j > i:
                distances[(i,j)] = length_squared(sub(b2, b1))

    all_dists = lmap(lambda x: (x[1],x[0]), distances.items())
    heapify(all_dists)

    sets = []
    for i in range(len(all_dists)):
        d, (b1, b2) = heappop(all_dists)
        last_sets_len = len(sets)

        added = []
        for si, s in enumerate(sets):
            if b1 in s or b2 in s:
                added.append(si)
        if len(added) == 0:
            sets.append({b1, b2})
        elif len(added) == 2:
            sets[added[0]] |= sets[added[1]]
            del sets[added[1]]
        else:
            sets[added[0]] |= {b1,b2}

        if i == 1000-1:
            print(reduce(operator.mul, sorted(lmap(len, sets), reverse=True)[:3]))

        if len(sets) == 1 and boxes_set - sets[0] == set():
            print(boxes[b1][0] * boxes[b2][0])
            break


if __name__ == "__main__":
    main()

# year 2025
# solution for 08.01: 66640
# solution for 08.02: 78894156
