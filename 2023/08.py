#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def main():

    lr, lines = open_data_groups("08.data")
    lr = lr[0]

    maps = dict()
    for l in lines:
        k,v = l.split(" = ")
        a,b = v[1:][:-1].split(", ")
        maps[k] = {"L": a, "R": b}

    i = 0
    n = "AAA"
    while n != "ZZZ":
        n = maps[n][lr[i%len(lr)]]
        i += 1
    print(i)

    ns = lfilter(lambda x: x.endswith("A"), maps.keys())
    final_index = [[] for i in range(len(ns))]

    while lfilter(lambda x: len(x) < 2, final_index) != []:
        for n in range(len(ns)):
            if ns[n].endswith("Z"):
                final_index[n].append(i)
            ns[n] = maps[ns[n]][lr[i%len(lr)]]
        i += 1

    print(reduce(lcm, lmap(lambda x: x[1]-x[0], final_index)))


if __name__ == "__main__":
    main()

# year 2023
# solution for 08.01: 16409
# solution for 08.02: 11795205644011
