#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *


def dist(b1, b2):
    s = sub3(b1, b2)
    return abs(s[0])+abs(s[1])+abs(s[2])



# with the highest number of bots in range
def find_coords(bots, start_pos, end_pos):

    max_value = 0
    field = dict()
    for x in range(start_pos[0], end_pos[0]):
        for y in range(start_pos[1], end_pos[1]):
            for z in range(start_pos[2], end_pos[2]):
                field[(x,y,z)] = sum(dist(b[0], (x,y,z)) <= b[1] for b in bots)
                max_value = max(max_value, field[(x,y,z)])

    coords = lfilter(lambda x:x[1] == max_value, field.items())
    dists = [(dist(c[0],(0,0,0)), c[0]) for c in coords]
    dists.sort()

    return dists[0][1]



def main():

    lines = open_data("23.data")

    nanobots = []
    for l in lines:
        x,y,z,r = ints(l)
        nanobots.append(((x,y,z), r))

    best_bot = max(nanobots, key=lambda x: x[1])

    print(sum(dist(b[0], best_bot[0]) <= best_bot[1] for b in nanobots))

    factor = 2**26
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
    #start_pos = add(start_pos, (-10000000, -10000000, -10000000))
    #end_pos = add(end_pos, (1000000, 1000000, 1000000))

    start_pos = lmap(int, div(start_pos, factor))
    end_pos = lmap(int, div(end_pos, factor))

    print(start_pos, end_pos)

    while True:

        bots = [(lmap(int, div(p[0], factor)), p[1]/factor) for p in nanobots]

        start_pos = find_coords(bots, start_pos, end_pos)
        end_pos = add(start_pos, (1,1,1))
        print("start_pos: ", start_pos, end_pos)

        if factor == 1:
            break
        start_pos = lmap(int, mul(start_pos, 2))
        end_pos   = lmap(int, mul(end_pos, 2))
        factor //= 2

    print("start_pos: ", start_pos)
    print(sum(map(abs, start_pos)))

    # <  156987769
    # != 148326432
    # != 148326435
    # != 156631040
    # >  9645141
if __name__ == "__main__":
    main()

# year 2018
# solution for 23.01: 935
# solution for 23.02: ?
