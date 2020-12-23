#!/usr/bin/env python3.7

from utility import *

def find_dest(cups, current, tmp, max_n):
    dest = current-1 if current-1 != 0 else max_n
    while dest in tmp:
        dest = dest-1 if dest-1 != 0 else max_n
    return dest

def to_list(cups, get_n):
    current = 1
    for i in range(get_n):
        yield cups[current]
        current = cups[current]

def play(cups, current, moves, get_n):

    max_n = max(cups.keys())
    for i in range(moves):

        n0 = cups[current]
        n1 = cups[n0]
        n2 = cups[n1]

        dest = find_dest(cups, current, [n0, n1, n2], max_n)

        cups[current] = cups[n2]
        cups[n2] = cups[dest]
        cups[dest] = n0

        current = cups[current]

    return to_list(cups, get_n)


def main():

    cups = lmap(int, list(open_data("23.data")[0]))

    # Create new data structure: A dict with cup_nr -> next_cup_nr
    new_cups = {c: cups[i+1] if i < len(cups)-1 else cups[0] for i, c in enumerate(cups)}
    print("".join(lmap(str, play(new_cups, cups[0], 100, 8))))

    cups = cups + [max(cups)+i+1 for i in range(1000000-len(cups))]
    new_cups = {c: cups[i+1] if i < len(cups)-1 else cups[0] for i, c in enumerate(cups)}
    a, b = play(new_cups, cups[0], 10000000, 2)
    print(a*b)


if __name__ == "__main__":
    main()

# solution for 23.01: 62934785
# solution for 23.02: 693659135400
