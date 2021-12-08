#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *


def solve_mapping(inputs, outputs):
    segments = {i: set("abcdefg") for i in range(7)}

    inputs.sort(key=lambda x: len(x))

    for i in inputs:
        if len(i) == 2:
            segments[2] = segments[2].intersection(set(i))
            segments[5] = segments[5].intersection(set(i))
        if len(i) == 3:
            segments[0] = set(i)-segments[2]
            segments[4] -= segments[0]
        if len(i) == 4:
            segments[1] = set(i)-segments[2] - segments[0]
            segments[3] = set(i)-segments[2]
        if len(i) == 6:
            if len(segments[2]) == 2 and len(set(i) & segments[2]) == 1:
                segments[5] = set(i) & segments[2]
                segments[2] -= segments[5]

    mapping = {}
    for i in inputs:
        if len(i) == 2:
            mapping[1] = set(i)
        if len(i) == 3:
            mapping[7] = set(i)
        if len(i) == 4:
            mapping[4] = set(i)
        if len(i) == 5:
            # 2,3,5
            if len(set(i) & (segments[2] | segments[5])) == 2:
                mapping[3] = set(i)
            elif len(set(i) & segments[2]) == 1:
                mapping[2] = set(i)
            else:
                mapping[5] = set(i)
        if len(i) == 6:
            # 0,6,9
            if len(set(i) & (segments[2] | segments[5])) == 1:
                mapping[6] = set(i)
            elif len(set(inputs[2]) & set(i)) == 3:
                mapping[0] = set(i)
            else:
                mapping[9] = set(i)
        if len(i) == 7:
            mapping[8] = set(i)

    return int("".join([str(k) for o in outputs for k,v in mapping.items() if set(o) == v]))


def main():

    lines = open_data("08.data")

    output = []
    inputs = []

    for l in lines:
        inputs.append(l.split(" | ")[0].split(" "))
        output.append(l.split(" | ")[1].split(" "))

    print(sum(len(tmp) in [2,4,3,7] for o in output for tmp in o))

    print(sum(solve_mapping(inputs[i], output[i]) for i in range(len(inputs))))


if __name__ == "__main__":
    main()

# year 2021
# solution for 08.01: 352
# solution for 08.02: 936117
