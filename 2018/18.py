#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *


def get_adjacent(field, pos):
    tmp = [field[add(pos,p)] for p in dir_list_8() if field[add(pos,p)] != -1]
    return Counter(tmp)


def run(field):

    new_field = field.copy()

    for key, item in list(field.items()):
        neighbors = get_adjacent(field, key)
        new_field[key] = item
        if item == 0 and neighbors[1] >= 3:
            new_field[key] = 1
            continue
        if item == 1 and neighbors[2] >= 3:
            new_field[key] = 2
            continue
        if item == 2 and not (neighbors[2] >= 1 and neighbors[1] >= 1):
            new_field[key] = 0
            continue

    return new_field


def score(field):
    c = Counter(field.values())
    return c[1] * c[2]


def main():

    lines = open_data("18.data")

    field = defaultdict(lambda: -1)

    for y,l in enumerate(lines):
        for x,c in enumerate(l):
            field[(x,y)] = 0 if c == "." else (1 if c == "|" else 2)


    # the field repeats from this round on!
    repeat_offset = 464
    # how many rounds are repeated
    repeat_count = 28
    max_n = 1000000000
    additional_rounds = (max_n-repeat_offset) % repeat_count
    scores = dict()

    for i in range(repeat_offset + additional_rounds):
        field = run(field)
        s = tuple(field.values())
        if s in scores:
            print("repeated round {} in round {} - diff: {}".format(scores[s], i, i-scores[s]))
            break
        else:
            scores[s] = i
        if i == 9:
            print(score(field))

    print(score(field))


if __name__ == "__main__":
    main()

# year 2018
# solution for 18.01: 605154
# solution for 18.02: 200364
