#!/usr/bin/env python3.7

from utility import *
from collections import Counter

def main():

    lines = open_data("02.data")

    puzzle_1_cnt = 0
    puzzle_2_cnt = 0

    for l in lines:
        mi = int(l.split("-")[0])
        ma = int(l.split("-")[1].split(" ")[0])
        letter = l.split(" ")[1][0]
        password = l.split(" ")[2]

        counter = Counter(password)
        if counter[letter] >= mi and counter[letter] <= ma:
            puzzle_1_cnt += 1

        if (mi <= len(password) and password[mi-1] == letter) != (ma <= len(password) and password[ma-1] == letter):
            puzzle_2_cnt += 1


    print(puzzle_1_cnt)
    print(puzzle_2_cnt)


if __name__ == "__main__":
    main()

# solution for 02.01: 422
# solution for 02.02: 451
