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


def bfs(field, p, used):
    queue = [p]
    while len(queue) > 0:
        pos = queue.pop(-1)
        used.add(pos)
        for n in dir_list_4():
            new_pos = add(pos, n)
            if new_pos in field and field[new_pos] == 1 and new_pos not in used:
                queue.append(new_pos)


def count_regions(d):
    field = {(x,y): int(d[y][x]) for y in range(128) for x in range(128)}
    used = set()
    count = 0
    for p in field:
        if p not in used and field[p] == 1:
            bfs(field, p, used)
            count += 1
    return count


def main():
    seed = open_data("14.data")[0]

    d = {i: "".join(f"{int(v, base=16):04b}" for v in knot_hash(f"{seed}-{i}")) for i in range(128)}

    print(sum(Counter(v)["1"] for v in d.values()))
    print(count_regions(d))


if __name__ == "__main__":
    main()

# year 2017
# solution for 14.01: 8304
# solution for 14.02: 1018
