#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def main():

    lines = open_data("15.data")

    sensors = dict()
    for line in lines:
        x,y, bx,by = ints(line)
        sensors[(x,y)] = manhatten_dist((x,y), (bx, by))

    yy = 2000000
    grid_y = set()
    for s, d in sensors.items():
        y_dist = abs(s[1] - yy)
        if y_dist < d:
            overlap = abs(y_dist-d)+1
            for x in range(s[0]-overlap, s[0]+overlap):
                if manhatten_dist((x,yy), s) <= d:
                    grid_y.add((x,yy))
    print(len(grid_y)-1)

    r = 4000000
    for s, d in sensors.items():
        p = (s[0]-d-1, s[1])
        for i in range(2*d):
            for pp in (add(p, (i,i)), add(add(p, (d+1,-d-1)), (i,i)), add(p, (i,-i)), add(add(p, (d+1,d+1)), (i,-i))):
                if pp[0] < 0 or pp[0] > r or pp[1] < 0 or pp[1] > r:
                    continue
                found = True
                for s2, d2 in sensors.items():
                    if s != s2 and manhatten_dist(pp, s2) <= d2:
                        found = False
                        break
                if found:
                    print(pp[0]*4000000+pp[1])
                    return


if __name__ == "__main__":
    main()

# year 2022
# solution for 15.01: 5127797
# solution for 15.02: 12518502636475
