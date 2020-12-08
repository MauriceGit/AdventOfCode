#!/usr/bin/env python3.7

from utility import *


def run(lines):

    visited = defaultdict(int)
    acc = 0
    at = 0

    while True:
        if at in visited:
            return False, acc

        if at >= len(lines):
            break

        visited[at] = 1

        op, arg = lines[at].split(" ")
        if op == "acc":
            acc += int(arg)
            at += 1
        elif op == "jmp":
            at += int(arg)
        elif op == "nop":
            at += 1

    return True, acc

def change(line):
    op, arg = line.split(" ")
    if op == "jmp":
        return "nop " + arg
    if op == "nop":
        return "jmp " + arg
    return line

def main():

    lines = open_data("08.data")

    _, puzzle_1 = run(lines)

    puzzle_2 = 0
    for i in range(len(lines)):
        last_line = lines[i]
        lines[i] = change(last_line)
        b, acc = run(lines)
        if b:
            puzzle_2 = acc
            break
        lines[i] = last_line

    print(puzzle_1, puzzle_2)



if __name__ == "__main__":
    main()

# solution for 08.01: 1200
# solution for 08.02: 1023
