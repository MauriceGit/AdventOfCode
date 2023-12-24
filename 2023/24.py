#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *

Hail = recordtype("Hail", "px py pz vx vy vz")


def line_intersection(l1, l2):
    # Convert to standard form
    m1 = l1.vy / l1.vx
    c1 = l1.py - m1 * l1.px
    m2 = l2.vy / l2.vx
    c2 = l2.py - m2 * l2.px

    # Calculate intersection point
    if m1 == m2:
        # The lines are parallel, so they don't intersect
        return None
    else:
        x = (c2 - c1) / (m1 - m2)
        y = m1 * x + c1
        return (x, y)


def intersection(h1, h2):

   return line_intersection(h1, h2)


def in_future(h1, cross):
    s = sub(cross, (h1.px, h1.py))
    return (s[0] >= 0) == (h1.vx >= 0) and (s[1] >= 0) == (h1.vy >= 0)


def main():

    lines = open_data("24.data")

    hail = lmap(lambda x: Hail(*ints(x)), lines)

    def in_area(p):
        for v in p:
            #if not (200000000000000 <= v <= 400000000000000):
            if not (7 <= v <= 27):
                return False
        return True

    count = 0
    for i, h1 in enumerate(hail):
        for i2 in range(i+1, len(hail)):
            h2 = hail[i2]
            p = intersection(h1, h2)
            ok = False if p == None else (in_future(h1, p) and in_future(h2, p))
            if p is not None and in_future(h1, p) and in_future(h2, p) and in_area(p):
                count += 1
    print(count)


if __name__ == "__main__":
    main()

# year 2023
# solution for 24.01: 24627
# solution for 24.02: ?
