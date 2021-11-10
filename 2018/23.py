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
    #dists = [(dist(c[0],(0,0,0)), c[0]) for c in coords]
    #dists.sort()
    #return dists[0][1]

    return [c[0] for c in coords]


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

    bot_range = sub(end_pos, start_pos)
    start_pos = lmap(int, div(start_pos, factor))
    end_pos = lmap(int, div(end_pos, factor))

    print(start_pos, end_pos)

    start_positions = [(start_pos, end_pos, factor)]

    final_positions = []

    while len(start_positions) > 0:

        new_start_positions = []
        start_positions.sort(key=lambda x: dist(x[0], (0,0,0))*x[2])
        best = start_positions[0]
        for p in start_positions:
            if dist(p[0], (0,0,0))*p[2] <= dist(best[1], (0,0,0))*best[2]:
                new_start_positions.append(p)
        start_positions = new_start_positions
        start_positions.sort(key=lambda x: x[2], reverse=True)

        start, end, fac = start_positions.pop(0)

        print(fac)

        bots = [(lmap(int, div(p[0], fac)), p[1]/fac) for p in nanobots]

        new_positions = find_coords(bots, start, end)

        for p in new_positions:
            if fac == 1:
                final_positions.append(p)
                #print(sum(map(abs, p)))
                #return
            else:
                start_positions.append((lmap(int, mul(p, 2)), lmap(int, mul(add(p, (1,1,1)), 2)), fac//2))



    final_positions.sort(key=lambda x: dist(x, (0,0,0)))

    #print([dist(x, (0,0,0)) for x in final_positions])

    print("final: ", final_positions[0])
    print(sum(map(abs, final_positions[0])))

    # <  156987769
    # != 156631040
    # != 148326432
    # != 148326435
    # != 148632564
    # != 148324352
    # >  9645141
if __name__ == "__main__":
    main()

# year 2018
# solution for 23.01: 935
# solution for 23.02: ?
