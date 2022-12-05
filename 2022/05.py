#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def run(commands, crates, part1=True):
    for instr in commands:
        c, fr, to = ints(instr)
        if part1:
            for i in range(c):
                crates[to-1].append(crates[fr-1].pop())
        else:
            crates[to-1].extend(crates[fr-1][-c:])
            del crates[fr-1][-c:]
    return "".join(map(lambda x: x[-1], crates))


def main():

    groups = open_data_groups("05.data")

    layout = [[l[i] for i in range(1, len(l), 4)] for l in groups[0][:-1]]
    crates = [list(filter(lambda x: x != " ", l[::-1])) for l in np.transpose(layout)]

    print(run(groups[1], deepcopy(crates)))
    print(run(groups[1], crates, part1=False))


if __name__ == "__main__":
    main()

# year 2022
# solution for 05.01: SHQWSRBDL
# solution for 05.02: CDTQZHBRS
