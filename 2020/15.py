#!/usr/bin/env python3.7

from utility import *

def main_dict():

    lines = ints(open_data("15.data")[0])

    pos = 0
    numbers = dict()
    last_num = 0

    for i, n in enumerate(lines[:-1]):
        numbers[n] = pos
        last_num = n
        pos = i+1
    last_num = lines[-1]
    pos = i+1

    while True:

        if pos+1 == 2020:
            print(last_num)
        if pos+1 == 30000000:
            print(last_num)
            break

        new = 0
        if last_num in numbers:
            new = pos - numbers[last_num]

        numbers[last_num] = pos
        last_num = new
        pos += 1

def main_list():

    lines = ints(open_data("15.data")[0])

    pos = 0
    numbers = [-1]*30000000
    last_num = 0

    for i, n in enumerate(lines[:-1]):
        numbers[n] = pos
        last_num = n
        pos = i+1
    last_num = lines[-1]
    pos = i+1

    while True:

        if pos+1 == 2020:
            print(last_num)
        if pos+1 == 30000000:
            print(last_num)
            break

        new = 0
        if numbers[last_num] != -1:
            new = pos - numbers[last_num]

        numbers[last_num] = pos
        last_num = new
        pos += 1


if __name__ == "__main__":
    main_list()

# solution for 15.01: 206
# solution for 15.02: 955
