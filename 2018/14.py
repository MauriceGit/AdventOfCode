#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *

def pp(scores, current):

    for i, s in enumerate(scores):
        c0 = "(" if current[0] == i else "[" if current[1] == i else " "
        c1 = ")" if current[0] == i else "]" if current[1] == i else " "
        print("{}{}{}".format(c0, s, c1), end="")
    print("")


def main():

    rounds = ints(open_data("14.data"))[0]

    scores = [3,7]
    current = [0, 1]

    #for i in range(rounds):
    #while len(scores) < rounds+10:
    #for i in range(1000000):
    while True:

        if len(scores) == rounds+10:
            print("".join(map(str, scores[rounds:rounds+10])))

        tmp = lmap(str, scores[-7:])
        if "170641" in "".join(tmp):
            print("FOUND")
            print(len(scores) - (6 if "170641" == tmp[:-1] else 7))
            break

        #pp(scores, current)

        new_score = scores[current[0]] + scores[current[1]]

        if new_score >= 10:
            scores.append((new_score//10) % 10)
        scores.append(new_score % 10)

        for i,c in enumerate(current):
            current[i] = (c + 1 + scores[c]) % len(scores)

    #print("".join(map(str, scores[rounds:rounds+10])))


    #print("59414" in "".join(map(str, scores)))
    #print("170641" in "".join(map(str, scores)))


if __name__ == "__main__":
    main()

# year 2018
# solution for 14.01: 2103141159
# solution for 14.02: ?
