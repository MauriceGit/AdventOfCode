#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def run(lines):
    factors = []
    for i, l in enumerate(lines):
        _, mod, _, offset = ints(l)
        factors.append((offset+1+i , mod))

    first = -1
    for i in itertools.count():
        ok = True
        for (offset, mod) in factors:
            if (i+offset)%mod != 0:
                ok = False
                break
        if ok:
            return i
    return -1

def main():

    lines = open_data("15.data")
    print(run(lines))

    lines.append("Disc #7 has 11 positions; at time=0, it is at position 0.")
    print(run(lines))


if __name__ == "__main__":
    main()

# year 2016
# solution for 15.01: 400589
# solution for 15.02: 3045959
