#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *


digits = ["cagedb", "ab", "gcdfa", "fbcad", "eafb", "cdfbe", "cdfgeb", "dab", "acedgfb", "cefabd"]


def get_digit(s):
    for i,d in enumerate(digits):
        if set(d) == set(s):
            return i
    return None


# fgc cgfbe ebgaf cbfa cgedbfa cf bgced gecfab defbag fgdcae | gfc cgf gbdfea fcg
# cga bcadfge aefdgc edgca dafc gdafbe aefcbg agefd ca cdegb | debcg faecgb cga gac
# dbcaf gcadebf eafcgb dbcefa gbdf cbfdga bcg adbcg gb edacg | afecbg cbg bfcad cabfdg

def solve_mapping(inputs):
    # int -> abcdefg...
    mapping = {}
    # int -> used_segments [int]*7
    nums = {0: [0,1,2,4,5,6], 1: [2,5], 2: [0,2,3,4,6], 3: [0,2,3,5,6], 4: [1,2,3,5], 5:[0,1,3,5,6],
            6: [0,1,3,4,5,6], 7: [0,2,5], 8: [0,1,2,3,4,5,6], 9: [0,1,2,3,5,6]}
    # 0..6 -> set(a..g)
    all_d = set("abcdefg")
    segments = {i: set("abcdefg") for i in range(7)}


    inputs = ["fgc", "cgfbe", "ebgaf", "cbfa", "cgedbfa", "cf", "bgced", "gecfab", "defbag", "fgdcae"]

    inputs.sort(key=lambda x: len(x))

    for i in inputs:
        if len(i) == 2:
            segments[2] = segments[2].intersection(set(i))
            segments[5] = segments[5].intersection(set(i))
        if len(i) == 3:
            segments[0] = set(i)-segments[2]
            segments[4] -= segments[0]
        if len(i) == 4:
            segments[1] = set(i)-segments[2] - segments[0]
            segments[3] = set(i)-segments[2]
        if len(i) == 5:
            print(i)

    print(segments)


def main():

    lines = open_data("08.data")

    output = []
    inputs = []

    for l in lines:
        output.append(l.split(" | ")[1].split(" "))
        inputs.append(l.split(" | ")[0].split(" "))



    count = 0
    for o in output:
        for tmp in o:
            count += int(len(tmp) in [2,4,3,7])

    print(count)

    solve_mapping("")
    return

    for o in output:
        s = ""
        for tmp in o:
            s += str(get_digit(tmp))

        print(s)

if __name__ == "__main__":
    main()

# year 2021
# solution for 08.01: ?
# solution for 08.02: ?
