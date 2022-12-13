#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def compare(l, r):

    for i in range(max(len(l), len(r))):
        if i >= len(r):
            return False
        if i >= len(l):
            return True

        match l[i], r[i]:
            case int(), int():
                if l[i] > r[i]:
                    return False
                if l[i] < r[i]:
                    return True
            case list(), list():
                if (res := compare(l[i], r[i])) != None:
                    return res
            case list(), int():
                if (res := compare(l[i], (r[:i]+[[r[i]]]+r[i+1:])[i])) != None:
                    return res
            case int(), list():
                if (res := compare((l[:i]+[[l[i]]]+l[i+1:])[i], r[i])) != None:
                    return res
    return None


def main():

    groups = open_data_groups("13.data")

    s = 0
    lines = []
    for i, g in enumerate(groups):
        lines.extend([loads(g[0]), loads(g[1])])
        s += (i+1)*compare(lines[-2], lines[-1])
    print(s)

    lines.append([[2]])
    lines.append([[6]])

    lines.sort(key=cmp_to_key(lambda l, r: -1 if compare(l, r) else 1))
    print((lines.index([[2]])+1) * (lines.index([[6]])+1))


if __name__ == "__main__":
    main()

# year 2022
# solution for 13.01: 5588
# solution for 13.02: 23958
