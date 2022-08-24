#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


# https://stackoverflow.com/questions/8421337/rotating-a-two-dimensional-array-in-python
def rot(tile, n=1):
    for i in range(n):
        tile = list(zip(*tile[::-1]))
        tile = lmap(lambda x: "".join(x), tile)
    return tile


def flip_v(tile, n=1):
    for i in range(n):
        tile = list(reversed(tile))
    return tile


def transform(tile, trans):
    return rot(flip_v(tile, n=trans[1]), n=trans[0])


@lru_cache(maxsize=1)
def unique_transforms():
    t = ["abc","def", "ghi"]
    d = dict()
    unique = []
    for r in range(4):
        for fv in range(2):
            tmp = transform(t, (r,fv))
            if "".join(tmp) not in d:
                unique.append((r,fv))
            d["".join(tmp)] = True
    return unique


# gets the 2x2 or 3x3 part as input
def apply_rule(image, rules):
    for r in rules:
        if image == r[0]:
            return r[1]
    return image


def apply_rules(image, rules):
    new_image = defaultdict(str)
    s = 2 if len(image)%2 == 0 else 3

    for y in range(len(image)//s):
        for x in range(len(image)//s):
            sub_image = []
            for i in range(s):
                sub_image.append(image[y*s+i][x*s:x*s+s])
            tmp = apply_rule(sub_image, rules)
            for i in range(len(tmp)):
                new_image[y*len(tmp)+i] += tmp[i]
    return new_image


def main():
    rules = lmap(lambda x: x.split(" => "), open_data("21.data"))
    rules = [(r[0].split("/"), r[1].split("/")) for r in rules]

    all_rules = [(transform(r[0], t), r[1]) for r in rules for t in unique_transforms()]

    image = defaultdict(str, {
        0: ".#.",
        1: "..#",
        2: "###"
    })

    for i in range(18):
        image = apply_rules(image, all_rules)
        if i == 4:
            print(sum(l.count("#") for l in image.values()))
    print(sum(l.count("#") for l in image.values()))


if __name__ == "__main__":
    main()

# year 2017
# solution for 21.01: 150
# solution for 21.02: 2606275
