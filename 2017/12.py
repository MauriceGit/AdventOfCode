#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def calc_group(conns, base):
    queue = [base]
    used = set()
    while len(queue) > 0:
        id_ = queue.pop(-1)
        if id_ not in used:
            queue.extend(conns[id_])
            used.add(id_)
    return used


def main():
    lines = open_data("12.data")

    conns = dict()
    for c in map(ints, lines):
        conns[c[0]] = c[1:]

    print(len(calc_group(conns, 0)))

    unused = set(conns.keys())
    count = 0
    while len(unused) > 0:
        unused -= calc_group(conns, unused.pop())
        count += 1
    print(count)


if __name__ == "__main__":
    main()

# year 2017
# solution for 12.01: 128
# solution for 12.02: 209
