#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *

def diff(a, b):
    l = [c if c == b[i] else "_" for i, c in enumerate(a)]
    return Counter(l)["_"], "".join(list(filter(lambda x: x != "_", l)))


def main():

    lines = open_data("02.data")

    twice = 0
    thrice = 0
    for l in lines:
        c = Counter(l)
        twice  += 2 in c.values()
        thrice += 3 in c.values()
    print(twice * thrice)

    for l in lines:
        for l2 in lines:
            c, t = diff(l, l2)
            if c == 1:
                print(t)
                return


if __name__ == "__main__":
    main()

# year 2018
# solution for 02.01: 8398
# solution for 02.02: hhvsdkatysmiqjxunezgwcdpr
