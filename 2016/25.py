#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


# d = a
# d += 7*365
# b = 0
# c = 0
# do:
#     a = d
#     do:
#         ...
#         b = a
#         a = 0
#         do:
#             c = 2
#             do:
#                 if b == 0:
#                     GOTO LABEL 1
#                 b -= 1
#                 c -= 1
#             while c != 0
#             a += 1
#         while True
# LABEL 1:
#         b = 2 - c
#         c = 0
#         OUT b
#     while a != 0
# while True

# This translates to the following python code:
# a = IN + 2555
# while a != 0:
#     print(a%2)
#     a = a//2

# So we are looking for a number with alternating 1/0 bits that is even (odd input!)


def main():

    lines = open_data("25.data")

    # xored with itself shifted once should result in only 1 bits! So bit_count should be equal to bit_length!
    i = 1
    while True:
        n = (i+2555) ^ ((i+2555)>>1)
        if n.bit_count() == n.bit_length():
            break
        i += 2
    print(i)


if __name__ == "__main__":
    main()

# year 2016
# solution for 25.01: 175
# solution for 25.02: *
