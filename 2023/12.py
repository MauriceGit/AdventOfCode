#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *

cache = dict()

def match(s, d):
    return d <= len(s) and all(s[i] in "?#" for i in range(d)) and (len(s) == d or s[d] != "#")


@cached(cache, key=lambda s, d: hashkey(tuple(s), tuple(d)))
def check_count(springs, damaged):

    if len(damaged) == 0 and "#" in springs or len(springs) == 0 and len(damaged) != 0:
        return 0

    if len(damaged) == 0:
        return 1

    count = 0
    if match(springs, damaged[0]):
        count += check_count(springs[damaged[0]+1:], damaged[1:])

    if not springs.startswith("#"):
        count += check_count(springs[1:], damaged)

    return count


def main():

    lines = open_data("12.data")

    springs = lmap(lambda x: x.split(" "), lines)
    print(sum(check_count(s[0], ints(s[1])) for s in springs))
    print(sum(check_count("?".join([s[0]]*5), ints(s[1])*5) for s in springs))


if __name__ == "__main__":
    main()

# year 2023
# solution for 12.01: 6488
# solution for 12.02: 815364548481
