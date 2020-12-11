#!/usr/bin/env python3.7

from utility import *



def get(seats, p):

    if p not in seats.keys():
        return 0

    if seats[p] in (0, 1):
        return seats[p]
    return 0

def epoche(seats):
    change = False
    new_seats = seats.copy()
    for s in seats.keys():

        l  = get(seats, add(s, (-1, 0)))
        r  = get(seats, add(s, (1, 0)))
        u  = get(seats, add(s, (0, -1)))
        d  = get(seats, add(s, (0,   1)))
        ul = get(seats, add(s, (-1, -1)))
        ur = get(seats, add(s, (1, -1)))
        dr = get(seats, add(s, (1, 1)))
        dl = get(seats, add(s, (-1, 1)))

        if seats[s] == 0 and all([x == 0 for x in [l,r,u,d,ul,ur,dr,dl]]):
            new_seats[s] = 1
            change = True
            continue
        if seats[s] == 1 and Counter([l,r,u,d,ul,ur,dr,dl])[1] >= 4:
            new_seats[s] = 0
            change = True
            continue
        new_seats[s] = seats[s]

    return change, new_seats

# pos, dir
def get2(seats, p, d):


    new_p = add(p, d)
    while True:
        if new_p not in seats.keys():
            return 0

        if seats[new_p] in (0, 1):
            return seats[new_p]

        new_p = add(new_p, d)

    return 0

def epoche2(seats):
    change = False
    new_seats = seats.copy()
    for s in seats.keys():

        l  = get2(seats, s, (-1, 0))
        r  = get2(seats, s, (1, 0))
        u  = get2(seats, s, (0, -1))
        d  = get2(seats, s, (0,   1))
        ul = get2(seats, s, (-1, -1))
        ur = get2(seats, s, (1, -1))
        dr = get2(seats, s, (1, 1))
        dl = get2(seats, s, (-1, 1))

        if seats[s] == 0 and all([x == 0 for x in [l,r,u,d,ul,ur,dr,dl]]):
            new_seats[s] = 1
            change = True
            continue
        if seats[s] == 1 and Counter([l,r,u,d,ul,ur,dr,dl])[1] >= 5:
            new_seats[s] = 0
            change = True
            continue
        new_seats[s] = seats[s]

    return change, new_seats

def main():

    lines = open_data("11.data")

    seats_o = dict()
    for row in range(len(lines)):
        for col in range(len(lines[row])):
            if lines[row][col] == "L":
                seats_o[(col, row)] = 0
            else:
                seats_o[(col, row)] = -1

    change, seats = epoche(seats_o.copy())
    while change:
        change, seats = epoche(seats)

    print(Counter(seats.values())[1])

    change, seats = epoche2(seats_o.copy())
    while change:
        change, seats = epoche2(seats)

    print(Counter(seats.values())[1])


if __name__ == "__main__":
    main()

# solution for 11.01: 2126
# solution for 11.02: 1914
