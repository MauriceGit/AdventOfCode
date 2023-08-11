#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def find_consecutive(s):
    three_of = []
    five_of = []
    count = 0
    for i, c in enumerate(s):
        if i > 0:
            if c == s[i-1]:
                count += 1
                if count+1 == 3 and len(three_of) == 0:
                    three_of.append(c)
                if count+1 == 5:
                    five_of.append(c)
            else:
                count = 0
    return three_of, five_of

def stretch_md5(key, count):
    for i in range(count):
        key = hashlib.md5(key.encode()).hexdigest()
    return key

def update_dicts(has_triple, five_of, salt, i, should_stretch=False):

        h = stretch_md5(salt + str(i), should_stretch * 2016 + 1)
        three, five = find_consecutive(h)
        if len(three) > 0:
            has_triple[i] = three[0]
        for f in five:
            five_of[f].append(i)

def calc_solution(salt, should_stretch=False):

    # {index: "a"}
    has_triple = dict()

    # {"a": [index_1, index_2, ...]}
    five_of = defaultdict(list)

    valid_hashes = 0
    for i in itertools.count():

        update_dicts(has_triple, five_of, salt, i, should_stretch=should_stretch)
        ii = i-1000

        if ii >= 0 and ii in has_triple:
            for index in five_of[has_triple[ii]]:
                if index > ii:
                    valid_hashes += 1
                    break

        if valid_hashes >= 64:
            return ii


def main():

    salt = open_data("14.data")[0]

    print(calc_solution(salt))
    print(calc_solution(salt, should_stretch=True))


if __name__ == "__main__":
    main()

# year 2016
# solution for 14.01: 16106
# solution for 14.02: 22423
