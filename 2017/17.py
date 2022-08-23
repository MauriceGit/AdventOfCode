#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def main():
    skip = int(open_data("17.data")[0])
    buf = deque([0])
    for i in range(50_000_000):
        if i == 2017:
            print(buf[0])
        buf.rotate(-skip)
        buf.appendleft(i+1)
        buf.rotate(-1)
    print(buf[buf.index(0)+1])


if __name__ == "__main__":
    main()

# year 2017
# solution for 17.01: 600
# solution for 17.02: 31220910
