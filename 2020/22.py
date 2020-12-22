#!/usr/bin/env python3.7

from utility import *

def score(l):
    return sum(c * (i+1) for i, c in enumerate(reversed(l)))

# returns points for each player
def play_rec(state, c1, c2, recursive):

    while True:

        if (tuple(c1), tuple(c2)) in state:
            return score(c1), 0
        state[(tuple(c1), tuple(c2))] = 1

        if len(c1) == 0 or len(c2) == 0:
            return score(c1), score(c2)

        draw_c1, draw_c2 = c1[0], c2[0]
        c1, c2 = c1[1:], c2[1:]

        if recursive and draw_c1 <= len(c1) and draw_c2 <= len(c2):
            a, b = play_rec({}, c1[:draw_c1].copy(), c2[:draw_c2].copy(), recursive)
            win_c1 = a > b
        else:
            win_c1 = draw_c1 > draw_c2

        if win_c1:
            c1 = c1 + [draw_c1, draw_c2]
        else:
            c2 = c2 + [draw_c2, draw_c1]

    return 0

def main():

    p1, p2 = open_data_groups("22.data")
    p1 = ints(p1[1:])
    p2 = ints(p2[1:])

    print(max(play_rec({}, p1.copy(), p2.copy(), False)))
    print(max(play_rec({}, p1.copy(), p2.copy(), True)))


if __name__ == "__main__":
    main()

# solution for 22.01: 35562
# solution for 22.02: 34424
