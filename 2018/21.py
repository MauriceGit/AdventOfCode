#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *


def run_decompiled(first_part):
    a = 0
    b = c = d = e = f = 0

    numbers = set()
    last_number = 0

    while True:
        f = c | 65536
        c = 2238642

        while True:
            d = f & 255
            c = (((c+d) & 16777215) * 65899) & 16777215

            if f < 256:
                break
            else:
                d = 0
                while (d+1)*256 <= f:
                    d += 1
            f = d

        if first_part:
            print(c)
            return

        if c in numbers:
            print(last_number)
            return

        numbers.add(c)
        last_number = c

        if c == a:
            break


def main():

    run_decompiled(True)
    run_decompiled(False)


if __name__ == "__main__":
    main()

# year 2018
# solution for 21.01: 13970209
# solution for 21.02: 6267260
