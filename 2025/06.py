#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def main():

    lines = open_data("06.data")
    lines_p1 = lmap(lambda l: re.sub(r"\s+", " ", l).strip().split(" "), lines)
    # reorder columns to rows
    tasks = lmap(list, [*zip(*lines_p1)])
    ops = {"*": operator.mul, "+": operator.add}

    # part1
    print(sum(reduce(ops[task[-1]], ints(task[:-1])) for task in tasks))

    last_i = 0
    p2 = 0
    for task in tasks:
        task, op = task[:-1], task[-1]
        # we take the string length of the largest number in the column to know
        # how many characters we take from each line!
        max_chars = max(map(len, task))

        new_task = [line[last_i:last_i+max_chars] for line in lines]
        new_task, new_op = new_task[:-1], new_task[-1].strip()

        nums = []
        for i in reversed(range(len(new_task[0]))):
            nums.append(int("".join(task[i] for task in new_task if task[i] != " ")))
        p2 += reduce(ops[new_op], nums)

        last_i += max_chars+1

    # part2
    print(p2)


if __name__ == "__main__":
    main()

# year 2025
# solution for 06.01: 5977759036837
# solution for 06.02: 9630000828442
