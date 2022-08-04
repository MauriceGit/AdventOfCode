#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def main():

    lines = open_data("02.data")

    print(sum(max(ints(l))-min(ints(l)) for l in lines))

    c = 0
    for l in lines:
        i = ints(l)
        for n1 in i:
            for n2 in i:
                if n1 != n2 and n1%n2 == 0:
                    c += n1//n2
    print(c)


if __name__ == "__main__":
    main()

# year 2017
# solution for 02.01: 53978
# solution for 02.02: 314
