#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *


@lru_cache(maxsize=1)
def possible_dice_rolls():
    # possible dice rolls (generates 27 universes overall!)
    # calculates the point values! Some occur multiple times for the three rolls!
    dice_points = Counter(list(map(sum, product([1,2,3], repeat=3))))
    return dice_points


def one_move(players, player, scores, game_states):

    if scores[0] >= 21:
        return (1, 0)
    if scores[1] >= 21:
        return (0, 1)

    # caching! This is the key features, that makes everything work (and fast!) :)
    game_state_key = (tuple(players), tuple(scores), player)
    if game_state_key in game_states:
        return game_states[game_state_key]

    won = (0, 0)
    for count, universes in possible_dice_rolls().items():
        tmp_players = players.copy()
        tmp_players[player] = (tmp_players[player]-1+count)%10+1

        tmp_scores = scores.copy()
        tmp_scores[player] += tmp_players[player]

        # recursive call!
        tmp = one_move(tmp_players, (player+1)%2, tmp_scores, game_states)

        # multiply by count of sub-universes!
        won = (won[0]+tmp[0]*universes, won[1]+tmp[1]*universes)

    # update cache
    game_states[game_state_key] = won
    return won


def play(players, scores):
    dice = 1
    player_index = 0
    die_rolls = 0

    while scores[0] < 1000 and scores[1] < 1000:
        d = dice*3+3
        players[player_index] = (players[player_index]-1+d)%10+1
        dice = (dice-1+3)%100+1
        scores[player_index] += players[player_index]
        player_index = (player_index+1)%2
        die_rolls += 3

    return min(scores)*die_rolls


def main():

    lines = open_data("21.data")

    scores = [0,0]
    players = [int(ints(lines[0])[1]), int(ints(lines[1])[1])]

    print(play(players.copy(), scores.copy()))
    print(max(one_move(players.copy(), 0, scores.copy(), dict())))


if __name__ == "__main__":
    main()

# year 2021
# solution for 21.01: 605070
# solution for 21.02: 218433063958910
