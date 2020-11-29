from functools import reduce

grid = dict()
dir_map = dict(zip("RLUD", [(1,0), (-1,0), (0,1), (0,-1)]))

def follow_cable(cable):

    pos = (0,0)
    step_count = 1
    # To detect self-collisions
    cable_internal_grid = dict()

    for c in cable.split(","):
        for _ in range(int(c[1:])):
            pos = (pos[0]+dir_map[c[0]][0], pos[1]+dir_map[c[0]][1])

            if pos not in grid:
                grid[pos] = step_count
                cable_internal_grid[pos] = 0
            # Check, that we don't count crosses with ourself!
            elif pos not in cable_internal_grid:
                other_cable_count = grid[pos]
                yield (pos[0], pos[1], other_cable_count+step_count)
            step_count += 1

collisions = reduce(list.__add__, map(list, map(follow_cable, open("03.data", "r").read().splitlines())))
print(min(map(lambda p: abs(p[0]) + abs(p[1]), collisions)))
print(min(map(lambda p: p[2], collisions)))

# solution for 03.01: 1674
# solution for 03.02: 14012
