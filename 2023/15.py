#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *

def hash(s):
    v = 0
    for c in s:
        v = ((v+ord(c))*17)%256
    return v

def main():

    seq = open_data("15.data")[0].split(",")

    print(sum(map(hash, seq)))

    boxes = [[] for i in range(256)]

    # label -> focal_length dictionary
    label_map = dict()

    for s in seq:
        if "-" in s:
            label = s[:-1]
            box = hash(label)
            if label in boxes[box]:
                i = boxes[box].index(label)
                boxes[box] = boxes[box][:i]+boxes[box][i+1:]
        if "=" in s:
            label, focal = s.split("=")
            box = hash(label)
            if label not in boxes[box]:
                boxes[box].append(label)
            label_map[label] = int(focal)

    focusing_power = 0
    for i, box in enumerate(boxes):
        for j, lens in enumerate(box):
            focusing_power += (i+1) * (j+1) * label_map[lens]
    print(focusing_power)


if __name__ == "__main__":
    main()

# year 2023
# solution for 15.01: 511416
# solution for 15.02: 290779
