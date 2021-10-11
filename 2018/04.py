#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *


def main():


    lines = open_data("04.data")
    lines = sorted(lines, key=lambda k: k.split("]")[0])

    for l in lines:
        print(l)


if __name__ == "__main__":
    main()

# year 2018
# solution for 04.01: ?
# solution for 04.02: ?
