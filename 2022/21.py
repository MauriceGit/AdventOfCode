#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def run(monkeys, current):

    if type(monkeys[current]) == int:
        if current == "humn":
            return monkeys[current], "x"
        return monkeys[current], str(monkeys[current])

    l, op, r = monkeys[current]

    d = {"+": operator.add, "*": operator.mul, "/": lambda x,y: x//y, "-": lambda x,y: x-y}

    rl = run(monkeys, l)
    rr = run(monkeys, r)
    r = d[op](rl[0], rr[0])

    if type(rl) == int and type(rr) == int:
        return r, f"{rl[1]} {op} {rr[1]}"

    if current == "root":
        op = "="

    if type(rl) == int:
        return r, f"{rl[0]} {op} ({rr[1]}))"
    return r, f"({rl[1]}) {op} {rr[0]})"

    #return r, f"({rl[1]}) {op} ({rr[1]})"




def main():

    lines = open_data("21.data")


    monkeys = dict()
    for l in lines:
        s = l.split(": ")
        i = ints(s[1])
        if len(i) == 1:
            monkeys[s[0]] = i[0]
        else:
            monkeys[s[0]] = s[1].split(" ")

    print(run(monkeys, "root"))



if __name__ == "__main__":
    main()

# year 2022
# solution for 21.01: ?
# solution for 21.02: ?
