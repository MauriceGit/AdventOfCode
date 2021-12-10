#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *


open_close = {"<": ">", "(": ")", "{": "}", "[": "]"}
points_corruption = {")": 3, "]": 57, "}": 1197, ">": 25137}
points_completion = {")": 1, "]": 2, "}": 3, ">": 4}


def completion_points(stack):
    p = 0
    for s in reversed(stack):
        p *= 5
        p += points_completion[open_close[s]]
    return p


def verify(line):

    stack = []
    for i in range(len(line)):
        if line[i] in open_close.keys():
            stack.append(line[i])
        else:
            if not open_close[stack[-1]] == line[i]:
                return points_corruption[line[i]], 0
            stack.pop(-1)

    return 0, completion_points(stack)


def main():

    lines = open_data("10.data")

    print(sum(verify(l)[0] for l in lines))

    tmp = sorted(lfilter(lambda x: x != 0, (verify(l)[1] for l in lines)))
    print(tmp[len(tmp)//2])


if __name__ == "__main__":
    main()

# year 2021
# solution for 10.01: 392139
# solution for 10.02: 4001832844
