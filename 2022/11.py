#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *

# items = [number], op = [left, op, right], div = number, throw = [number_false, number_true]
Monkey = recordtype("Monkey", "items op div throw")


def run_op(line, old):
    l = old if line[0] == "old" else int(line[0])
    r = old if line[2] == "old" else int(line[2])
    return {"+": l+r, "*": l*r}[line[1]]


def run(monkeys, part1=True):
    active = [0]*len(monkeys)
    factor = math.prod(m.div for m in monkeys)

    for r in range(20 if part1 else 10000):
        for i, m in enumerate(monkeys):
            while len(m.items) > 0:
                new_worry = run_op(m.op, m.items.popleft())
                if part1:
                    new_worry //= 3
                else:
                    new_worry %= factor

                monkeys[m.throw[new_worry % m.div == 0]].items.append(new_worry)
                active[i] += 1

    active.sort()
    return active[-1]*active[-2]


def main():

    groups = open_data_groups("11.data")

    monkeys = []
    for g in groups:
        monkeys.append(Monkey(deque(ints(g[1])), g[2].split(" = ")[1].split(" "), ints(g[3])[0], (ints(g[5])[0], ints(g[4])[0])))

    print(run(deepcopy(monkeys)))
    print(run(monkeys, part1=False))


if __name__ == "__main__":
    main()

# year 2022
# solution for 11.01: 50172
# solution for 11.02: 11614682178
