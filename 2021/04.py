#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *


winning_positions = []
for i in range(5):
    winning_positions.append({(v,i) for v in range(5)})
    winning_positions.append({(i,v) for v in range(5)})


def check_winner(found_positions):
    return any(w - found_positions == set() for w in winning_positions)


def score(p_dict, checked_positions, number):
    unmarked = set(p_dict.keys()) - checked_positions
    return sum(p_dict[u] for u in unmarked) * number


def play(boards, numbers, win_first=True):

    won_boards = set()
    for n in numbers:
        for i,_ in enumerate(boards):
            if n in boards[i][0]:
                boards[i][1].add(boards[i][0][n])
                if check_winner(boards[i][1]):
                    won_boards.add(i)
                    if win_first or len(won_boards) == len(boards):
                        return score(boards[i][2], boards[i][1], n)
    return 0

def main():

    lines = open_data_groups("04.data")
    numbers = ints(lines[0][0])
    boards = []

    for b in lines[1:]:
        # [value -> pos, found_pos, pos -> value]
        board = [dict(), set(), dict()]
        for y, row in enumerate(b):
            for x, v in enumerate(ints(row)):
                board[0][v] = (x,y)
                board[2][(x,y)] = v
        boards.append(board)

    print(play(boards, numbers))
    print(play(boards, numbers, win_first=False))


if __name__ == "__main__":
    main()

# year 2021
# solution for 04.01: 58412
# solution for 04.02: 10030
