#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def find_rotation_value(d, letter):
    for i in range(len(d)):
        for extra in [1,2]:
            tmp_d = d.copy()
            tmp_d.rotate(-(extra+i))
            index = tmp_d.index(letter)
            a = (extra == 1 and index < 4)
            b = (extra == 2 and index >= 4)
            if (a or b) and index == i:
                return i+extra
    return 0


def scramble(d, lines, unscramble=False):
    for l in lines:
        if l.startswith("swap position"):
            i1, i2 = ints(l)
            d[i1], d[i2] = d[i2], d[i1]
        elif l.startswith("swap letter"):
            tmp = l.split(" ")
            i1, i2 = d.index(tmp[2]), d.index(tmp[5])
            d[i1], d[i2] = d[i2], d[i1]
        elif l.startswith("rotate based on position"):
            if unscramble:
                value = find_rotation_value(d, l.split(" ")[6])
                d.rotate(-value)
            else:
                i = d.index(l.split(" ")[6])
                d.rotate(1+i+int(i >= 4))
        elif l.startswith("rotate"):
            n = int(l.split(" ")[2]) * (-1 if unscramble else 1)
            d.rotate(n if "right" in l else -n)
        elif l.startswith("reverse"):
            d2 = list(d)
            i1, i2 = ints(l)
            d = deque(d2[:i1] + d2[i1:i2+1][::-1] + d2[i2+1:])
        elif l.startswith("move"):
            i1, i2 = ints(l)
            if unscramble:
                i1, i2 = i2, i1
            v = d[i1]
            d.remove(v)
            d.insert(i2, v)

    return "".join(d)


def main():

    lines = open_data("21.data")
    print(scramble(deque("abcdefgh"), lines))
    print(scramble(deque("fbgdceah"), lines[::-1], unscramble=True))


if __name__ == "__main__":
    main()

# year 2016
# solution for 21.01: hcdefbag
# solution for 21.02: fbhaegdc
