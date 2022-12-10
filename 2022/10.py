#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def main():

    lines = open_data("10.data")

    buf = []
    for l in lines:
        buf.extend([None, None, int(l.split(" ")[1])] if l.startswith("addx") else [None])

    x = 1
    cycles = 0
    signal_strength = 0
    crt = []
    for i, b in enumerate(buf):
        if b != None:
            x += b
        else:
            crt.append("█" if cycles%40 in [x-1,x,x+1] else " ")
            cycles += 1
            if cycles in [20, 60, 100, 140, 180, 220]:
                signal_strength += cycles*x

    print(signal_strength)

    for i in range(6*40):
        print(crt[(i//40)*40+(i%40)], end="\n" if i%40 == 39 else "")


if __name__ == "__main__":
    main()

# year 2022
# solution for 10.01: 14220
# solution for 10.02: ZRARLFZU
