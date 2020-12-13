#!/usr/bin/env python3.7

from utility import *

from sympy.ntheory.modular import crt

def main():

    lines = open_data("13.data")

    wait = int(lines[0])

    earliest = 0
    earliest_id = 0

    for b in ints(lines[1]):
        ap = wait//b + 1
        if ap*b < earliest or earliest == 0:
            earliest = ap*b
            earliest_id = b

    print((earliest-wait)*earliest_id)


    busses = [(int(t), i) for i,t in enumerate(lines[1].split(",")) if t != "x"]

    # unzip list of tuples in to two lists with the elements
    remainder, modulos = lmap(list, zip(*busses))

    # So I can search for it later: chinese remainder theorem, CRT, crt, Chinese Remainder Theorem.
    a, b = crt(remainder, modulos)

    # WHY do I need to substract the first (actual) result from the second something???
    print(b-a)


if __name__ == "__main__":
    main()

# solution for 13.01: 1895
# solution for 13.02: 840493039281088
