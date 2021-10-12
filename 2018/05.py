#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *


def reduce_polymer(line, letters):
    while True:
        l = len(line)
        for c in letters:
            line = line.replace(c[0]+c[1], "")
            line = line.replace(c[1]+c[0], "")
        if l == len(line):
            return len(line)


def main():

    line = open_data("05.data")[0]

    small = [chr(i) for i in range(97, 123)]
    large = [chr(i) for i in range(65, 91)]
    letters = list(zip(small, large))

    print(reduce_polymer(line, letters))
    print(min(reduce_polymer(line.replace(c[0], "").replace(c[1], ""), letters) for c in letters))


if __name__ == "__main__":
    main()

# year 2018
# solution for 05.01: 11108
# solution for 05.02: 5094
