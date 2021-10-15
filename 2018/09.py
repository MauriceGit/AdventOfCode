#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *
from collections import deque

def play(max_marble, player_count):

    current_stone = 1
    circle = deque([0])
    points = [0]*player_count

    while current_stone <= max_marble:
        for i in range(player_count):
            if current_stone <= max_marble:
                if current_stone % 23 != 0:
                    circle.rotate(-2)
                    circle.appendleft(current_stone)
                else:
                    points[i] += current_stone
                    circle.rotate(7)
                    points[i] += circle.popleft()
                current_stone += 1

    return max(points)


def main():

    p_count, max_marble = ints(open_data("09.data")[0])

    print(play(max_marble, p_count))
    print(play(max_marble*100, p_count))


if __name__ == "__main__":
    main()

# year 2018
# solution for 09.01: 390592
# solution for 09.02: 3277920293
