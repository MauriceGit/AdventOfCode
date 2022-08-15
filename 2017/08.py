#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def eval_cond(regs, c_reg, c_op, c_val):
    return {
        "<": lambda: regs[c_reg] < int(c_val),
        ">": lambda: regs[c_reg] > int(c_val),
        ">=": lambda: regs[c_reg] >= int(c_val),
        "<=": lambda: regs[c_reg] <= int(c_val),
        "!=": lambda: regs[c_reg] != int(c_val),
        "==": lambda: regs[c_reg] == int(c_val)
    }[c_op]()


def main():

    lines = open_data("08.data")

    regs = defaultdict(int)
    highest = 0

    for l in lines:
        tmp, cond = l.split(" if ")
        if eval_cond(regs, *cond.split(" ")):
            r, op, val = tmp.split(" ")
            regs[r] += int(val) if op == "inc" else -int(val)
            highest = max(highest, regs[r])

    print(max(regs.values()))
    print(highest)


if __name__ == "__main__":
    main()

# year 2017
# solution for 08.01: 4448
# solution for 08.02: 6582
