#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *

def main():

    lines = open_data("01.data")

    pos = (0,0)
    d = (0,-1)
    all_pos = set()
    part_2 = None
    for l in lines[0].split(", "):
        d = rotate(d, l[0] != "L")
        old_pos = pos
        pos = add(pos, mul(d, int(l[1:])))

        if part_2 is None:
            for i in range(1, int(l[1:])):
                new_pos = (old_pos[0]+d[0]*i, old_pos[1]+d[1]*i)
                if new_pos in all_pos:
                    part_2 = new_pos
                all_pos.add(new_pos)

    print(sum(map(abs, pos)))
    print(sum(map(abs, part_2)))


if __name__ == "__main__":
    main()

# year 2016
# solution for 01.01: 300
# solution for 01.02: 159
