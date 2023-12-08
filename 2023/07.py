#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def calc_strength(card, part2=False):
    if part2 and "J" in card and card != "JJJJJ":
        card_ = card.replace("J", "")
        sorted_cc = sorted(Counter(card_).items(), key=lambda x: x[1], reverse=True)
        return calc_strength(card_ + sorted_cc[0][0] * (5-len(card_)))

    c = Counter(card)
    match len(c):
        case 1: return 7
        case 2: return 6 if set(c.values()) == {1,4} else 5
        case 3: return 4 if set(c.values()) == {1,3} else 3
        case 4: return 2
        case 5: return 1


def compare(c1, c2, part2=False):
    s1 = calc_strength(c1[0], part2=part2)
    s2 = calc_strength(c2[0], part2=part2)
    if s1 > s2:
        return 1
    if s1 < s2:
        return -1

    cards = "AKQJT98765432"
    if part2:
        cards = cards.replace("J", "") + "J"
    strength = dict(zip(cards, range(len(cards)-1, -1, -1)))

    return 1 if lmap(lambda x: strength[x], c1[0]) > lmap(lambda x: strength[x], c2[0]) else -1


def main():

    lines = open_data("07.data")
    lines = lmap(lambda x: (x.split(" ")[0], int(x.split(" ")[1])), lines)

    lines.sort(key=cmp_to_key(lambda x,y: compare(x,y,part2=False)))
    print(sum(lines[i][1] * (i+1) for i in range(len(lines))))

    lines.sort(key=cmp_to_key(lambda x,y: compare(x,y,part2=True)))
    print(sum(lines[i][1] * (i+1) for i in range(len(lines))))


if __name__ == "__main__":
    main()

# year 2023
# solution for 06.01: 250946742
# solution for 06.02: 251824095
