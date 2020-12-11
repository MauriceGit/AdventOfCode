#!/usr/bin/env python3.7

from utility import *

# pos, dir
def get(seats, p, d):
    return seats.get(add(p, d))

# pos, dir
def get2(seats, p, d):
    new_p = add(p, d)
    while seats.get(new_p) == ".":
        new_p = add(new_p, d)
    return seats.get(new_p)

def epoche(seats, puzzle_2):
    change = False
    new_seats = seats.copy()

    occupied = 5 if puzzle_2 else 4
    get_seat_f = get2 if puzzle_2 else get

    for s in seats:
        c = Counter(map(lambda x: get_seat_f(seats, s, x), dir_list_8()))

        if seats[s] == "L" and c["#"] == 0:
            new_seats[s] = "#"
            change = True
            continue

        if seats[s] == "#" and c["#"] >= occupied:
            new_seats[s] = "L"
            change = True
            continue

        new_seats[s] = seats[s]

    return change, new_seats

def main():

    lines = open_data("11.data")

    seats_o = defaultdict(lambda: "L")
    for row in range(len(lines)):
        for col in range(len(lines[row])):
            seats_o[(col, row)] = lines[row][col]


    change, seats = epoche(seats_o.copy(), False)
    while change:
        change, seats = epoche(seats, False)
    print(Counter(seats.values())["#"])

    change, seats = epoche(seats_o.copy(), True)
    while change:
        change, seats = epoche(seats, True)
    print(Counter(seats.values())["#"])


if __name__ == "__main__":
    main()

# solution for 11.01: 2126
# solution for 11.02: 1914
