#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def main():
    lines = open_data("19.data")
    p = (lines[0].index("|"), 0)
    d = (0, 1)
    field = defaultdict(lambda: " ", {(x,y): c for y,l in enumerate(lines) for x,c in enumerate(l)})
    letters = []

    for i in itertools.count():
        c = field[p]
        if c == " ":
            break

        if c not in "|-+":
            letters.append(c)

        if c == "+":
            if d[0] == 0:
                d = (1,0) if field[add(p,(1,0))] != " " else (-1,0)
            else:
                d = (0,1) if field[add(p,(0,1))] != " " else (0,-1)
        p = add(p, d)

    print("".join(letters))
    print(i)


if __name__ == "__main__":
    main()

# year 2017
# solution for 19.01: BPDKCZWHGT
# solution for 19.02: 17728
