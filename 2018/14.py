#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *


def main():

    rounds = ints(open_data("14.data"))[0]

    scores = "37"
    c0, c1 = 0, 1

    while True:

        if len(scores) == rounds+10:
            print(scores[rounds:rounds+10])

        tmp = scores[-7:]
        if str(rounds) in tmp:
            print(len(scores) - (6 if str(rounds) == tmp[:-1] else 7))
            return

        scores += str(int(scores[c0]) + int(scores[c1]))

        c0 = (c0 + 1 + int(scores[c0])) % len(scores)
        c1 = (c1 + 1 + int(scores[c1])) % len(scores)


if __name__ == "__main__":
    main()

# year 2018
# solution for 14.01: 2103141159
# solution for 14.02: ?
