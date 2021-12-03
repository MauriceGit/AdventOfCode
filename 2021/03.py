#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *


def bit_criteria(numbers, index, search):
    return lfilter(lambda n: n[index] == search, numbers)


def main():

    lines = open_data("03.data")

    gamma = [""]*len(lines[0])
    eps = [""]*len(lines[0])
    oxygen_rating = lines
    co2_rating = lines

    for i in range(len(lines[0])):
        c = Counter(l[i] for l in lines)
        gamma[i] = int(c["1"] > c["0"])
        eps[i] = int(c["1"] < c["0"])

        if len(oxygen_rating) > 1:
            c = Counter(l[i] for l in oxygen_rating)
            oxygen_rating = bit_criteria(oxygen_rating, i, str(int(c["1"] >= c["0"])))
        if len(co2_rating) > 1:
            c = Counter(l[i] for l in co2_rating)
            co2_rating = bit_criteria(co2_rating, i, str(int(c["1"] < c["0"])))

    print(int("".join(lmap(str, gamma)), 2) * int("".join(lmap(str, eps)), 2))
    print(int(oxygen_rating[0],2) * int(co2_rating[0],2))


if __name__ == "__main__":
    main()

# year 2021
# solution for 03.01: 3549854
# solution for 03.02: 3765399
