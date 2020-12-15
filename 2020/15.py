#!/usr/bin/env python3.7

from utility import *

def main():

    lines = ints(open_data("15.data")[0])

    pos = 0
    numbers = defaultdict(list)
    last_num = 0

    for i, n in enumerate(lines):
        numbers[n].append(pos)
        last_num = n
        pos = i+1

    while True:

        if pos == 2020:
            print(last_num)
        if pos == 30000000:
            print(last_num)
            break

        last = numbers[last_num]
        new = 0
        if len(last) > 1:
            new = last[-1]-last[-2]

        numbers[new].append(pos)
        last_num = new
        pos += 1


if __name__ == "__main__":
    main()

# solution for 15.01: 206
# solution for 15.02: 955
