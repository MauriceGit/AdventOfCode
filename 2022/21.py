#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *

# for each equation, one part is always an int!
def solve(monkeys, current, solution):

    if current == "humn":
        return solution

    l, op, r = monkeys[current]

    if type(l) == int:
        match op:
            case "+": return solve(monkeys, r, solution-l)
            case "*": return solve(monkeys, r, solution//l)
            case "/": return solve(monkeys, r, l//solution)
            case "-": return solve(monkeys, r, l-solution)
    if type(r) == int:
        match op:
            case "+": return solve(monkeys, l, solution-r)
            case "*": return solve(monkeys, l, solution//r)
            case "/": return solve(monkeys, l, solution*r)
            case "-": return solve(monkeys, l, solution+r)


def run(monkeys, current):

    if type(monkeys[current]) == int:
        return monkeys[current], None if current == "humn" else monkeys[current]

    l_m, op, r_m = monkeys[current]

    d = {"+": operator.add, "*": operator.mul, "/": operator.floordiv, "-": operator.sub}
    rl = run(monkeys, l_m)
    rr = run(monkeys, r_m)
    result = d[op](rl[0], rr[0])

    if rr[1] != None and rl[1] == None:
        monkeys[current][2] = rr[0]
    if rl[1] != None and rr[1] == None:
        monkeys[current][0] = rl[0]
    if rl[1] != None and rr[1] != None:
        monkeys[current] = result

    if current == "root":
        return result, (rl[0] if rl[1] != None else rr[0], l_m if rl[1] == None else r_m)

    return result, result if rl[1] != None and rr[1] != None else None


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

    p1, p2 = run(monkeys, "root")
    print(p1)
    print(solve(monkeys, p2[1], p2[0]))


if __name__ == "__main__":
    main()

# year 2022
# solution for 21.01: 364367103397416
# solution for 21.02: 3782852515583
