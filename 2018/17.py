#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *
from time import sleep


def valid(field, visited, pos):
    return pos not in field and pos not in visited


# returns a node where water can fall down again. Or None if there isn't one
def fill(field, visited, p, d):
    p = add(p, d)
    while p not in field:
        if add(sub(p, d), (0,1)) in field and add(p, (0,1)) in visited:
            return None
        if valid(field, visited, add(p, (0, 1))):
            return p


        visited[p] = True
        p = add(p, d)

    return None

def needs_filling_up(field, visited, p, d):
    while p not in field:
        if valid(field, visited, add(p, (0, 1))):
            # we can fall down before hitting a wall. So this is NOT a basin that needs to be filled!
            return False
        p = add(p, d)

    return True

def pp(field, visited):
    combined = dict()

    min_x = min(visited.keys(), key=lambda x: x[0])[0]
    min_y = min(visited.keys(), key=lambda x: x[1])[1]
    max_x = max(visited.keys(), key=lambda x: x[0])[0]
    max_y = max(visited.keys(), key=lambda x: x[1])[1]

    for x in range(min_x, max_x+1):
        for y in range(min_y, max_y+1):
            if (x,y) in field:
                combined[(x,y)] = 1

    for k in visited.keys():
        combined[k] = 2

    draw(combined,  {-1: " ", 1: "█", 2: "|"})
    print("=========================================================================")


def run_water(field, min_y, max_y, spring_pos):

    visited = defaultdict(bool)
    front = [add(spring_pos, (0, 1))]
    backtrack = dict()
    backtrack[front[0]] = None

    while len(front) > 0:
        node = front.pop(0)

        if node in visited or node in field or node[1] > max_y:
            continue

        visited[node] = True
        next_node = add(node, (0, 1))

        if valid(field, visited, next_node):
            front.append(next_node)
            backtrack[next_node] = node
        else:

            if next_node in visited:
                l = needs_filling_up(field, visited, node, (-1, 0))
                r = needs_filling_up(field, visited, node, ( 1, 0))
                if not l or not r:
                    continue

            while True:

                down_l = fill(field, visited, node, (-1, 0))
                down_r = fill(field, visited, node, ( 1, 0))

                if down_l:
                    front.append(down_l)
                    backtrack[down_l] = node
                if down_r:
                    front.append(down_r)
                    backtrack[down_r] = node
                if down_l or down_r:
                    break

                node = backtrack[node]

        #pp(field, visited)
        #sleep(0.2)

    return visited


def main():

    lines = open_data("17.data")

    field = dict()
    for l in lines:
        a, b = l.split(",")
        if "x" in b:
            b, a = ints(a), ints(b)
        else:
            a, b = ints(a), ints(b)

        for x in range(min(a), max(a)+1):
            for y in range(min(b), max(b)+1):

                # DEBUG
                #if y <= 655:
                field[(x,y)] = 1

    visited = run_water(field, 1, max(field.keys(), key=lambda x: x[1])[1], (500, 0))

    pp(field, visited)

    print(len(visited.keys()))


    # < 444305
    # <  65377

if __name__ == "__main__":
    main()

# year 2018
# solution for 17.01: ?
# solution for 17.02: ?
