#!/usr/bin/env python3.7

from utility import *

def overwrite_v1(memory, index, mask, number):

    if index not in memory:
        memory[index] = ['0']*36

    mask   = "".join(mask)
    number = "".join(number).rjust(36, "0")
    for i, b in enumerate(number):
        memory[index][i] = mask[i] if mask[i] != "X" else b


def get_addresses(mask):
    for i, b in enumerate(mask):
        if b == "X":
            return get_addresses(mask[:i]+['0']+mask[i+1:]) + get_addresses(mask[:i]+['1']+mask[i+1:])

    return [mask]


def overwrite_v2(memory, index, mask, number):

    index = list(bin(index))[2:]
    index = ["0"]*(36-len(index)) + index

    mask = [mask[i] if ma in "X1" else index[i] for i, ma in enumerate(mask)]

    addresses = get_addresses(mask)
    for a in addresses:
        memory[int("".join(a), 2)] = number


def main():

    lines = open_data("14.data")

    memory_v1 = dict()
    memory_v2 = dict()
    mask   = ['0']*36
    for l in lines:
        if l.split(" ")[0] == "mask":
            mask = list(l.split(" ")[2])
        else:
            r = re.match(r"mem\[(\d+)\] = (\d+)", l)

            index  = int(r.group(1))
            number = list(bin(int(r.group(2))))[2:]

            # Puzzle 1
            overwrite_v1(memory_v1, index, mask, number)
            overwrite_v2(memory_v2, index, mask, number)

    print(sum(map(lambda x: int("".join(memory_v1[x]), 2), memory_v1)))
    print(sum(map(lambda x: int("".join(memory_v2[x]), 2), memory_v2)))


if __name__ == "__main__":
    main()

# solution for 14.01: 13556564111697
# solution for 14.02: 4173715962894
