#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def concat(a, b):
    return a * 10**(int(math.log10(b))+1) + b


def run(result, current, numbers, part2=False):
    if len(numbers) == 0:
        return current == result
    if current > result:
        return False
    for op in [operator.add, operator.mul] + ([concat] if part2 else []):
        if run(result, op(current, numbers[0]), numbers[1:], part2=part2):
            return True
    return False


def main():

    lines = lmap(ints, open_data("07.data"))

    print(sum(l[0] * run(l[0], 0, l[1:]) for l in lines))
    print(sum(l[0] * run(l[0], 0, l[1:], part2=True) for l in lines))


if __name__ == "__main__":
    main()

# year 2024
# solution for 07.01: 3245122495150
# solution for 07.02: 105517128211543
