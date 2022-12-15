#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *



def main():

    lines = open_data("15.data")

    sensors = dict()
    beacons = set()
    for line in lines:
        x,y, bx,by = ints(line)
        sensors[(x,y)] = manhatten_dist((x,y), (bx, by))
        beacons.add((bx,by))

    #yy = 2000000
    #grid_y = set()
    #for s, b in sensors.items():
    #    d = manhatten_dist(s, b)
    #        for x in range(s[0]-d, s[0]+d):
    #            if manhatten_dist((x,yy), s) <= d:
    #                #grid_y[(x,10)] = 1
    #                grid_y.add((x,yy))
    #print(len(grid_y)-1)

    r = 4000000
    #r = 20

    #for y in range(r+1):
    #    #for x in range(r+1):
    #    x = 0
    #    print(y)
    #    while x <= r:
    #        skip_x = 1
    #        found = True
    #        for s,d in sensors.items():
    #            dd = manhatten_dist((x,y), s)
    #            if dd <= d:
    #                skip_x = max(1, d-dd)
    #                found = False
    #                break
    #
    #        if found:
    #            print((x,y), x*4000000+y)
    #            return
    #        x += skip_x

    grid = dict()
    poss = set(sensors.keys())
    for y in range(-10,30):
        for x in range(-10,30):
            for s,d in sensors.items():
                if (x,y) in poss:
                    grid[(x,y)] = '●'
                elif (x,y) in beacons:
                    grid[(x,y)] = '■'
                elif manhatten_dist((x,y), s) <= d:
                    grid[(x,y)] = 1 if (x,y) not in grid else grid[(x,y)]+1

    draw_direct(grid)










if __name__ == "__main__":
    main()

# year 2022
# solution for 15.01: 5127797
# solution for 15.02: 12518502636475
