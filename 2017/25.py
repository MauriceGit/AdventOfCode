#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def main():
    groups = open_data_groups("25.data")

    current_state = groups[0][0][-2]
    steps = ints(groups[0][1])[0]

    states = dict()
    for g in groups[1:]:
        s = g[0][-2]
        todo = ((
            ints(g[2])[0],                  # what to write
            1 if "right" in g[3] else -1,   # which way to move
            g[4][-2]                        # which state to continue
        ), (
            ints(g[6])[0],
            1 if "right" in g[7] else -1,
            g[8][-2]
        ))
        states[s] = todo

    tape = defaultdict(int)
    cursor = 0
    for i in range(steps):
        tape[cursor], step, current_state = states[current_state][tape[cursor]]
        cursor += step

    print(sum(tape.values()))


if __name__ == "__main__":
    main()

# year 2017
# solution for 25.01: 2832
# solution for 25.02: *
