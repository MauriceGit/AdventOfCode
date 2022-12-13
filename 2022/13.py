#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def compare2(l, r):
    for i in range(max(len(l), len(r))):
        if i >= len(r):
            return False
        if i >= len(l):
            return True

        if type(l[i]) == int and type(r[i]) == int:
            if int(l[i]) > int(r[i]):
                return False
            if int(l[i]) < int(r[i]):
                return True
        elif type(l[i]) == list and type(r[i]) == list:
            if (res := compare2(l[i], r[i])) != None:
                return res
        else:
            if type(r[i]) == int:
                if (res := compare2(l[i], (r[:i]+[[r[i]]]+r[i+1:])[i])) != None:
                    return res
            else:
                if (res := compare2((l[:i]+[[l[i]]]+l[i+1:])[i], r[i])) != None:
                    return res
    return None


def compare(l, r):
    return -1 if compare2(l, r) else 1


def main():

    groups = open_data_groups("13.data")

    s = 0
    lines = []
    for i, g in enumerate(groups):
        lines.extend([eval(g[0]), eval(g[1])])
        if compare2(lines[-2], lines[-1]):
            s += i+1
    print(s)

    lines.append([[2]])
    lines.append([[6]])

    lines.sort(key=cmp_to_key(compare))
    print((lines.index([[2]])+1) * (lines.index([[6]])+1))


if __name__ == "__main__":
    main()

# year 2022
# solution for 13.01: 5588
# solution for 13.02: 23958
