#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *

Brick = namedtuple("Brick", "id x1 y1 z1 x2 y2 z2")
Relation = namedtuple("Relation", "under over")

def move_down(b, n=1):
    return Brick(b.id, b.x1, b.y1, b.z1-n, b.x2, b.y2, b.z2-n)

def range_overlap(v1min, v1max, v2min, v2max):
    if v1min < v2min and v1max < v2min or v2min < v1min and v2max < v1min:
        return False
    return True

def overlap(b1, b2):
    # X doesn't overlap at all
    if not range_overlap(b1.x1, b1.x2, b2.x1, b2.x2):
        return False
    if not range_overlap(b1.y1, b1.y2, b2.y1, b2.y2):
        return False
    if not range_overlap(b1.z1, b1.z2, b2.z1, b2.z2):
        return False
    return True


def max_move(bricks, b, i):

    for n in itertools.count():
        b = move_down(b)
        if b.z1 < 1:
            return n, []
        overlaps = []
        for bi in range(i):
            if overlap(b, bricks[bi]):
                overlaps.append(bricks[bi].id)
        if overlaps != []:
            return n, overlaps

def would_fall(relations, b_id):
    fall_ids = []
    for over_b in relations[b_id].over:
        if len(relations[over_b].under) <= 1:
            fall_ids.append(over_b)
    return fall_ids


def how_many_would_fall(relations, brick_id):
    count = 0
    fallen = {brick_id}


    queue = relations[brick_id].over.copy()

    while len(queue) > 0:

        b_id = queue.pop()

        safe = False
        for i in relations[b_id].under:
            if i not in fallen:
                safe = True
                break

        if not safe:
            fallen.add(b_id)

            queue.extend(relations[b_id].over)

    return fallen



def main():

    lines = open_data("22.data")

    bricks = [Brick(i, x,y,z,a,b,c) for i, (x,y,z,a,b,c) in enumerate(lmap(ints, lines))]
    #print(bricks)
    bricks.sort(key=itemgetter(3, 2, 1))

    relations = dict()
    for b in bricks:
        relations[b.id] = Relation([], [])
        #print(b.id, b)

    print("sorted")

    for i in range(len(bricks)):
        n, underneath = max_move(bricks, bricks[i], i)
        if n >= 1:
            bricks[i] = move_down(bricks[i], n=n)

        for under in underneath:
            relations[under].over.append(bricks[i].id)
            relations[bricks[i].id].under.append(under)

    print("moved")

    #bricks.sort(key=itemgetter(2,1,0))

    #print(relations)
    #for r in sorted(relations.items()):
    #    print(r)
    count = 0
    for b in bricks:
        if relations[b.id].over == []:
            count += 1
            #print(f"{b.id} doesnt support anything")
        else:
            # lies on more than just one brick
            all_are_safe = True
            for over_b in relations[b.id].over:
                if len(relations[over_b].under) <= 1:
                    all_are_safe = False
                    break
                #if len(relations[over_b].under) > 1:
                #    count += 1
                #    break
            if all_are_safe:
                count += 1

    print(count)

    count = 0
    for b_id in relations.keys():
        count += len(how_many_would_fall(relations, b_id))-1


    print(count)


if __name__ == "__main__":
    main()

# year 2023
# solution for 22.01: < 557
# solution for 22.02: ?
