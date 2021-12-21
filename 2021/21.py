#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *



def play(players, scores, highscore):
    dice = 1
    player_index = 0
    die_rolls = 0

    while scores[0] < highscore and scores[1] < highscore:
        d = dice*3+3
        players[player_index] = (players[player_index]-1+d)%10+1
        dice = (dice-1+3)%100+1
        scores[player_index] += players[player_index]
        player_index = (player_index+1)%2
        die_rolls += 3

    return min(scores)*die_rolls

def play2(players, scores, highscore):
    player_index = 0
    die_rolls = 0

    while scores[0] < 21 and scores[1] < 21:

        die_roll = 3 .. 9

        players[player_index] = (players[player_index]-1+die_roll)%10+1
        scores[player_index] += players[player_index]
        player_index = (player_index+1)%2

    return min(scores)

def main():

    lines = open_data("21.data")

    scores = [0,0]
    players = [int(ints(lines[0])[1]), int(ints(lines[1])[1])]

    print(play(players, scores, 1000))


    print(play(players, scores, 1000))







if __name__ == "__main__":
    main()

# year 2021
# solution for 21.01: 605070
# solution for 21.02: ?
