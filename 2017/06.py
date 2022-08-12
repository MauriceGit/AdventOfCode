#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def get_max_index(numbers):
    return max(enumerate(numbers), key=lambda x: x[1])[0]


def run(numbers, part2):
    d = dict()
    d[tuple(numbers)] = True

    for count in itertools.count():
        mi = get_max_index(numbers)
        m = numbers[mi]
        numbers[mi] = 0

        for i in range(m):
            numbers[(i+mi+1)%len(numbers)] += 1

        if tuple(numbers) in d:
            return count+1

        if not part2:
            d[tuple(numbers)] = True


def main():

    numbers = ints(open_data("06.data")[0])

    print(run(numbers, False))
    print(run(numbers, True))


if __name__ == "__main__":
    main()

# year 2017
# solution for 06.01: 14029
# solution for 06.02: 2765
