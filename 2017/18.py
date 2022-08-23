#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *

import string
from enum import Enum

class Status(Enum):
    FINISHED = 1
    WAITING  = 2
    OK       = 3

def run(regs, lines, i, recv_values):

    sent_values = []
    while True:
        if i >= len(lines) or i < 0:
            return Status.FINISHED, 0, sent_values
        t = lines[i].split(" ")
        op = t[0]
        r1 = t[1] if t[1] in regs else int(t[1])
        r2 = 0 if len(t) <= 2 else regs[t[2]] if t[2] in regs else int(t[2])
        jump = 1

        if op == "snd":
            sent_values.append(regs[r1] if r1 in regs else int(r1))
        elif op == "set":
            regs[r1] = r2
        elif op == "add":
            regs[r1] += r2
        elif op == "mul":
            regs[r1] *= r2
        elif op == "mod":
            regs[r1] %= r2
        elif op == "rcv" and r1 != 0:
            if len(recv_values) > 0:
                regs[r1] = recv_values.pop(0)
            else:
                return Status.WAITING, i, sent_values

        elif op == "jgz":
            if r1 in regs and regs[r1] > 0 or r1 not in regs and r1 > 0:
                jump = r2

        i += jump

    # status, next_i, sent_values
    return Status.FINISHED, 0, sent_values


def main():
    lines = open_data("18.data")

    print(run({r:0 for r in string.ascii_lowercase}, lines, 0, [])[2][-1])

    regs0 = regs = {r:0 for r in string.ascii_lowercase}
    regs1 = regs = {r:1 if r == "p" else 0 for r in string.ascii_lowercase}
    i0, i1 = 0, 0
    sent0, sent1 = [], []
    count1 = 0
    s0, s1 = Status.OK, Status.OK

    while True:
        if s0 != Status.OK and s1 != Status.OK and sent0 == sent1 == []:
            break

        s0, i0, sent0 = run(regs0, lines, i0, sent1)
        s1, i1, sent1 = run(regs1, lines, i1, sent0)
        count1 += len(sent1)

    print(count1)


if __name__ == "__main__":
    main()

# year 2017
# solution for 18.01: 3423
# solution for 18.02: 7493
