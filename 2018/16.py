#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *

def apply_opcode(registers, opcode, a, b, c):
    registers[c] = {
        0:  lambda: registers[a] + registers[b],          # addr
        1:  lambda: registers[a] + b,                     # addi
        2:  lambda: registers[a] * registers[b],          # mulr
        3:  lambda: registers[a] * b,                     # muli
        4:  lambda: registers[a] & registers[b],          # banr
        5:  lambda: registers[a] & b,                     # bani
        6:  lambda: registers[a] | registers[b],          # borr
        7:  lambda: registers[a] | b,                     # bori
        8:  lambda: registers[a],                         # setr
        9:  lambda: a,                                    # seti
        10: lambda: int(a > registers[b]),                # gtir
        11: lambda: int(registers[a] > b),                # gtri
        12: lambda: int(registers[a] > registers[b]),     # gtrr
        13: lambda: int(a == registers[b]),               # eqir
        14: lambda: int(registers[a] == b),               # eqri
        15: lambda: int(registers[a] == registers[b]),    # eqrr
    }[opcode]()
    return registers


def matches(before, test, after):
    for op in range(16):
        if apply_opcode(before.copy(), op, *test[1:]) == after:
            yield op


def solve_mapping(equations):

    mapping = defaultdict(int)
    while any(lmap(len, equations.values())):
        for k in equations.keys():
            e = equations[k]
            if len(e) == 1:
                v = list(e)[0]
                mapping[k] = v
                # remove from all other list. This is a clear mapping
                for k in equations.keys():
                    equations[k] = lfilter(lambda x: x != v, equations[k])

    return mapping


def apply_sequence(mapping, sequence):
    registers = [0,0,0,0]
    for s in sequence:
        registers = apply_opcode(registers, mapping[s[0]], *s[1:])
    return registers


def main():

    groups = open_data_groups("16.data")

    equations = defaultdict(set)
    test = []

    count = 0
    for lines in groups:

        if lines == []:
            continue

        if lines[0].startswith("Before"):
            q = ints(lines[1])
            # list of opcodes that work for this given formula
            valid_opcodes = list(matches(ints(lines[0]), q, ints(lines[2])))
            count += len(valid_opcodes) >= 3

            tmp = equations[q[0]]
            equations[q[0]] = set(valid_opcodes) if tmp == set() else tmp & set(valid_opcodes)


        else:
            test = lmap(ints, lines)
            break

    print(count)
    print(apply_sequence(solve_mapping(equations), test)[0])


if __name__ == "__main__":
    main()

# year 2018
# solution for 16.01: 529
# solution for 16.02: 573
