#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *

# return: (data, children), current_index_in_list
def build_tree(l, index):
    root = [[], []]
    end_index = index+2

    for i in range(l[index]):
        c, end_index = build_tree(l, end_index)
        root[1].append(c)

    root[0].extend(l[end_index:end_index+l[index+1]])
    end_index += l[index+1]

    return root, end_index

def part_1(t):
    return sum(t[0]) + sum(part_1(c) for c in t[1])

def part_2(t):
    return sum(t[0]) if len(t[1]) == 0 else sum(part_2(t[1][i-1]) for i in t[0] if i-1 < len(t[1]))


def main():

    line = ints(open_data("08.data")[0])

    t, _ = build_tree(line, 0)
    print(part_1(t))
    print(part_2(t))


if __name__ == "__main__":
    main()

# year 2018
# solution for 08.01: 40984
# solution for 08.02: 37067
