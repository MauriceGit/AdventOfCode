#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *

def part1(inputs, ops):
    while len(ops) > 0:
        for k, v in ops.items():
            if k not in inputs and v[1] in inputs and v[2] in inputs:
                inputs[k] = v[0](inputs[v[1]], inputs[v[2]])
                del ops[k]
                break

    return int("".join([str(int(inputs[k])) for k in sorted(filter(lambda x: x.startswith("z"), inputs.keys()), key=lambda x: int(x[1:]), reverse=True)]), 2)


def pp_(inputs, ops, n):

    if n in inputs:
        return f"{n}"

    o, a, b = ops[n]
    op = ""
    match o:
        case operator.and_:
            op = "&"
        case operator.or_:
            op = "|"
        case operator.xor:
            op = "^"

    print(f"{n} = {a} {op} {b}")
    return f"({pp_(inputs, ops, a)} {op} {pp_(inputs, ops, b)})"

def pp(inputs, ops, n):
    print(pp_(inputs, ops, n))



def main():

    lines = open_data_groups("24.data")

    inputs = dict()
    for l in lines[0]:
        i, b = l.split(": ")
        inputs[i] = b == "1"

    # result <- (op-function, input1, input2)
    ops = dict()
    for l in lines[1]:
        ab, res = l.split(" -> ")
        a, op, b = ab.split(" ")
        o = {"AND": operator.and_, "OR": operator.or_, "XOR": operator.xor}[op]
        ops[res] = (o, a, b)

    print(part1(inputs.copy(), ops.copy()))

    pp(inputs, ops, "z00")
    pp(inputs, ops, "z01")
    pp(inputs, ops, "z02")
    pp(inputs, ops, "z03")



if __name__ == "__main__":
    main()

# year 2024
# solution for 24.01: ?
# solution for 24.02: ?
