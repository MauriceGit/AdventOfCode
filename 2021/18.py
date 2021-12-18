#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *
import json


def should_explode(n, level):
    return type(n) == list and len(n) == 2 and type(n[0]) == int and type(n[1]) == int and level >= 4

def should_split(n):
    return type(n) == int and n >= 10


def add_left_side(number, addon):
    if type(number) == int:
        return number + addon
    return [add_left_side(number[0], addon), number[1]]


def add_right_side(number, addon):
    if type(number) == int:
        return number + addon
    return [number[0], add_right_side(number[1], addon)]


def reduce_number(number, level, explode=True):
    if type(number) == int:
        return number, None, None, False

    children = [number[0], number[1]]
    for i in range(2):

        if explode and should_explode(number[i], level+1):
            left, right = children[i]
            children[i] = 0
            if i == 0:
                children[1] = add_left_side(number[1], right)
                right = None
            else:
                children[0] = add_right_side(number[0], left)
                left = None
            return children, left, right, True

        if not explode and should_split(number[i]):
            children[i] = [number[i]//2, ceil(number[i]/2)]
            return children, None, None, True

        # always recurse left first!
        children[i], left, right, done = reduce_number(number[i], level+1, explode=explode)

        if i == 0 and right is not None:
            children[1] = add_left_side(number[1], right)
            right = None
        elif i == 1 and left is not None:
            children[0] = add_right_side(number[0], left)
            left = None

        if done:
            return children, left, right, True

    return children, None, None, False


def fix_snailfish_number(number):
    not_done = True
    while not_done:
        while not_done:
            number, _, _, not_done = reduce_number(number, 0, explode=True)
        number, _, _, not_done = reduce_number(number, 0, explode=False)
    return number


def add_snailfish_numbers(n1, n2):
    return fix_snailfish_number([n1, n2])


def magnitude(number):
    if type(number) == int:
        return number
    return 3*magnitude(number[0]) + 2*magnitude(number[1])


def main():

    lines = lmap(json.loads, open_data("18.data"))

    print(magnitude(reduce(add_snailfish_numbers, lines)))

    best_magnitude = 0
    for c in list(combinations(lines, 2))+list(combinations(reversed(lines), 2)):
        best_magnitude = max(best_magnitude, magnitude(add_snailfish_numbers(*c)))
    print(best_magnitude)


if __name__ == "__main__":
    main()

# year 2021
# solution for 18.01: 4202
# solution for 18.02: 4779
