#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def run(ps, commands):
    for c in commands:
        i = ints(c)
        if c[0] == "s":
            ps.rotate(i[0])
        elif c[0] == "x":
            ps[i[0]], ps[i[1]] = ps[i[1]], ps[i[0]]
        elif c[0] == "p":
            p0 = ps.index(c[1])
            p1 = ps.index(c[3])
            ps[p0], ps[p1] = ps[p1], ps[p0]
    return ps


def main():
    commands = open_data("16.data")[0].split(",")

    print("".join(run(deque("abcdefghijklmnop"), commands)))

    d = dict()
    ps = deque("abcdefghijklmnop")
    states = []
    for i in itertools.count():
        tmp = "".join(ps)
        if tmp in d:
            print(states[1000000000%i])
            break
        d[tmp] = True
        states.append(tmp)

        ps = run(ps, commands)


if __name__ == "__main__":
    main()

# year 2017
# solution for 16.01: kpbodeajhlicngmf
# solution for 16.02: ahgpjdkcbfmneloi
