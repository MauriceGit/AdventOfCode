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

# modinv and egcd taken from here: https://stackoverflow.com/questions/4798654/modular-multiplicative-inverse-function-in-python
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)
def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

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
            break

        if "170641" == "".join(map(str, scores[-6:])):
            print("FOUND")
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
