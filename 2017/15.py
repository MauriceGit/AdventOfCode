#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def generate(last, factor, mod, part2):
    while True:
        last = (last*factor)%2147483647
        if not part2 or last%mod == 0:
            yield last&0xffff


def main():
    starts = lmap(lambda x: ints(x)[0], open_data("15.data"))
    factors = (16807, 48271)

    g1 = generate(starts[0], factors[0], 4, False)
    g2 = generate(starts[1], factors[1], 8, False)
    print(sum(next(g1) == next(g2) for i in range(40000000)))

    g1 = generate(starts[0], factors[0], 4, True)
    g2 = generate(starts[1], factors[1], 8, True)
    print(sum(next(g1) == next(g2) for i in range(5000000)))


if __name__ == "__main__":
    main()

# year 2017
# solution for 15.01: 569
# solution for 15.02: 298
