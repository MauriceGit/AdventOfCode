#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


# subtract s2 from s1
def difference(s1, s2):
    # no overlap
    if s1[0] < s2[0] and s1[1] < s2[0] or s2[0] < s1[0] and s2[1] < s1[0]:
        return [s1]
    # 1111
    #   2222
    if s1[0] <= s2[0] and s1[1] <= s2[1]:
        return [(s1[0], s2[0]-1)]
    #   1111
    # 2222
    if s1[0] >= s2[0] and s1[1] >= s2[1]:
        return [(s2[1]+1, s1[1])]
    # 1111
    #  22
    if s1[0] < s2[0] and s1[1] > s2[1]:
        return [(s1[0], s2[0]-1), (s2[1]+1, s1[1])]
    return []


def find_all_valid_ips(blocked, max_ip):
    valid = [(0, max_ip)]
    for b in blocked:
        valid = [e for v in valid for e in difference(v, b)]
    return sum(map(lambda x: x[1]+1-x[0], valid))


def main():

    lines = sorted(map(lambda l: tuple(map(int, l.split("-"))), open_data("20.data")))

    max_ip = 4294967295
    min_ip = 0
    for a, b in lines:
        if a <= min_ip:
            min_ip = b+1
    print(min_ip)

    print(find_all_valid_ips(lines, max_ip))


if __name__ == "__main__":
    main()

# year 2016
# solution for 20.01: 19449262
# solution for 20.02: 119
