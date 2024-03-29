#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def hash_round(inputs, numbers, skip):
    start = 0
    numbers = deque(numbers)
    for n in inputs:
        l = []
        for _x in range(n):
            l.append(numbers.popleft())
        numbers.extendleft(l)
        numbers.rotate(-(n+skip))
        start -= n+skip
        skip += 1
    return list(numbers), start, skip


def knot_hash(seed):
    seed = lmap(ord, seed) + [17,31,73,47,23]
    numbers = list(range(256))
    skip = 0
    offset = 0

    for i in range(64):
        numbers, off, skip = hash_round(seed, numbers, skip)
        offset += off
    tmp = deque(numbers)
    tmp.rotate(-offset%256)
    numbers = list(tmp)

    dense_hash = [reduce(operator.xor, numbers[i*16:(i+1)*16]) for i in range(16)]
    return "".join(f"{x:02x}" for x in dense_hash)


def main():
    inputs = open_data("10.data")[0]

    out, offset, _ = hash_round(ints(inputs), list(range(256)), 0)
    print(out[offset%256]*out[(offset+1)%256])
    print(knot_hash(inputs))


if __name__ == "__main__":
    main()

# year 2017
# solution for 10.01: 4480
# solution for 10.02: c500ffe015c83b60fad2e4b7d59dabc4
