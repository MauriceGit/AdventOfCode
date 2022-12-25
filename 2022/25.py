#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


from_snafu = {"2": 2, "1": 1, "0": 0, "-": -1, "=": -2}
to_snafu = dict(map(reversed, from_snafu.items()))

def add_snafu(s1, s2):
    res = ""
    overflow = 0
    max_len = max(len(s1), len(s2))
    s1 = "0"*(max_len-len(s1)) + s1
    s2 = "0"*(max_len-len(s2)) + s2

    i = max_len-1
    while i >= 0 or overflow != 0:
        nx = from_snafu[s1[i] if i >= 0 else "0"] + from_snafu[s2[i] if i >= 0 else "0"] + overflow
        overflow = 0

        if nx in to_snafu.keys():
            res += to_snafu[nx]
        elif nx < -2:
            res += to_snafu[5+nx]
            overflow = -1
        elif nx > 2:
            res += to_snafu[-5+nx]
            overflow = 1
        i -= 1

    return res[::-1]


def snafu_to_int(number):
    num = 0
    for i, n in enumerate(number):
        if n == "=":
            num += 5**(len(number)-i-1) * -2
        elif n == "-":
            num += 5**(len(number)-i-1) * -1
        else:
            num += 5**(len(number)-i-1) * int(n)
    return num


def main():

    lines = open_data("25.data")
    print(reduce(add_snafu, lines))


if __name__ == "__main__":
    main()

# year 2022
# solution for 25.01: 2011-=2=-1020-1===-1
# solution for 25.02: *
