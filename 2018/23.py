#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *


def dist(b1, b2):
    s = sub3(b1[0], b2[0])
    return abs(s[0])+abs(s[1])+abs(s[2])


# with the highest number of bots in range
def find_coords(bots, start_pos, end_pos):

    field = dict()
    max_x = max(bots, key=lambda x:x[0])
    for x in range(start_pos[0], end_pos[0]):
        for y in range(start_pos[1], end_pos[1]):
            for z in range(start_pos[2], end_pos[2]):
                field[(x,y,z)] = sum(dist(b, ((x,y,z),0)) <= b[1] for b in bots)

    coord = max(field.items(), key=lambda x:x[1])[0]
    next_coord = field[add3(coord, (1,1,1))][0]

    return coord, next_coord


def main():

    lines = open_data("23.data")

    nanobots = []
    for l in lines:
        x,y,z,r = ints(l)
        nanobots.append(((x,y,z), r))

    best_bot = max(nanobots, key=lambda x: x[1])

    print(sum(dist(b, best_bot) <= best_bot[1] for b in nanobots))

    factor = 2**2
    start_pos = (
        min(nanobots, key=lambda x:x[0][0])[0][0],
        min(nanobots, key=lambda x:x[0][1])[0][1],
        min(nanobots, key=lambda x:x[0][2])[0][2]
    )
    end_pos = (
        max(nanobots, key=lambda x:x[0][0])[0][0],
        max(nanobots, key=lambda x:x[0][1])[0][1],
        max(nanobots, key=lambda x:x[0][2])[0][2]
    )

    start_pos = lmap(int, mul3(start_pos, 1/factor))
    end_pos = lmap(int, mul3(end_pos, 1/factor))

    print(start_pos, end_pos)

    while factor >= 1:

        bots = [(lmap(int, mul3(p[0], 1/factor)), p[1]/factor) for p in nanobots]
        print(bots[0])

        start_pos, end_pos = find_coords(bots, start_pos, end_pos)

        start_pos = lmap(int, mul3(start_pos, 2))
        end_pos   = lmap(int, mul3(end_pos, 2))
        factor //= 2

    print(start_pos)


    # < 156987769
    # > 9645141
if __name__ == "__main__":
    main()

# year 2018
# solution for 23.01: 935
# solution for 23.02: ?
