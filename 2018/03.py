#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *

# returns the maximum overlap for this piece!
def add_overlap(field, id, pos, size):
    s = 0
    for x in range(size[0]):
        for y in range(size[1]):
            field[add(pos, (x,y))] += 1
            s = max(s, field[add(pos, (x,y))])
    return s

def parse(l):
    return lmap(ints, l.split(" "))


def main():

    lines = open_data("03.data")
    lines = [l.replace("#", "").replace("@ ", "").replace(":", "") for l in lines]

    field = defaultdict(int)
    no_overlap_id = 0

    for l in lines:
        add_overlap(field, *parse(l))

    # Solution for first part
    print(len(list(filter(lambda x: x > 1, field.values()))))

    for l in lines:
        id, pos, size = parse(l)
        if add_overlap(field, id, pos, size) == 2:
            print(*id)
            break


if __name__ == "__main__":
    main()

# year 2018
# solution for 03.01: 105071
# solution for 03.02: 222
