#!/usr/bin/env python3.7

from utility import *



def main():

    lines = ints(open_data("01.data"))

    print(sum(lines))

    frequencies = dict()
    current = 0
    while True:
        for s in lines:
            if current in frequencies:
                print(current)
                return
            frequencies[current] = True
            current += s



if __name__ == "__main__":
    main()

# solution for 01.01: 578
# solution for 01.02: 82516
