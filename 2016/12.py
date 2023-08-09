#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def main():

    lines = open_data("12.data")

    # The instructions correspond to the following code:
    # a = 1
    # b = 1
    # c = 0
    # d = 26
    # if c != 0:
    #     d += 7
    #
    # while d != 0:
    #     c = a
    #     while b != 0:
    #         a += 1
    #         b -= 1
    #     b = c
    #     d -= 1
    #
    # a += 19*11

    # The outer while loop just calculates the fibonacci-numbers for d
    # (fibonacci index d+2 times actually because we start the sequence not at the first)

    # So the end-result is:
    fibonacci_28 = 317811
    fibonacci_35 = 9227465
    print(fibonacci_28 + 19*11)
    print(fibonacci_35 + 19*11)


if __name__ == "__main__":
    main()

# year 2016
# solution for 12.01: 318020
# solution for 12.02: 9227674
