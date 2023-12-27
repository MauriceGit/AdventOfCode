#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *
from sympy import symbols, solve, Eq

Hail = recordtype("Hail", "px py pz vx vy vz")

def intersection(l1, l2):
    # Convert to standard form
    m1 = l1.vy / l1.vx
    c1 = l1.py - m1 * l1.px
    m2 = l2.vy / l2.vx
    c2 = l2.py - m2 * l2.px
    # The lines are parallel, so they don't intersect
    if m1 == m2:
        return None
    x = (c2 - c1) / (m1 - m2)
    y = m1 * x + c1
    return (x, y)


def in_future(h1, cross):
    s = sub(cross, (h1.px, h1.py))
    return (s[0] >= 0) == (h1.vx >= 0) and (s[1] >= 0) == (h1.vy >= 0)


def main():

    lines = open_data("24.data")

    hail = lmap(lambda x: Hail(*ints(x)), lines)

    min_area, max_area = 200000000000000, 400000000000000
    count = 0
    for i, h1 in enumerate(hail):
        for i2 in range(i+1, len(hail)):
            h2 = hail[i2]
            p = intersection(h1, h2)
            if p is not None and in_future(h1, p) and in_future(h2, p) and all((min_area <= v <= max_area for v in p)):
                count += 1
    print(count)

    h0, h1, h2 = hail[:3]
    px, py, pz, vx, vy, vz, t1, t2, t3 = symbols("px, py, pz, vx, vy, vz, t1, t2, t3")
    eqs = [
        Eq(h0.px + h0.vx*t1, px + t1*vx),
        Eq(h0.py + h0.vy*t1, py + t1*vy),
        Eq(h0.pz + h0.vz*t1, pz + t1*vz),
        Eq(h1.px + h1.vx*t2, px + t2*vx),
        Eq(h1.py + h1.vy*t2, py + t2*vy),
        Eq(h1.pz + h1.vz*t2, pz + t2*vz),
        Eq(h2.px + h2.vx*t3, px + t3*vx),
        Eq(h2.py + h2.vy*t3, py + t3*vy),
        Eq(h2.pz + h2.vz*t3, pz + t3*vz)
    ]

    sol = solve(eqs, [px, py, pz, vx, vy, vz, t1, t2, t3])
    print(sum(sol[0][:3]))


if __name__ == "__main__":
    main()

# year 2023
# solution for 24.01: 24627
# solution for 24.02: 527310134398221
