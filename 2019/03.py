
dir_map = dict(zip("RLUD", [(1,0), (-1,0), (0,1), (0,-1)]))

def follow_cable(cable, number, grid):

    collisions = []
    pos = (0,0)
    step_count = 1
    # To detect self-collisions
    cable_internal_grid = dict()

    for c in cable:
        count = int(c[1:])
        step = dir_map[c[0]]

        for _ in range(count):
            pos = (pos[0]+step[0], pos[1]+step[1])

            if pos not in grid:
                grid[pos] = step_count
                cable_internal_grid[pos] = number
            # Check, that we don't count crosses with ourself!
            elif pos not in cable_internal_grid:
                other_cable_count = grid[pos]
                collisions.append((pos[0], pos[1], other_cable_count+step_count))

            step_count += 1
    return collisions

# Calculates manhattan distance
def lowest_01(pos):
    return abs(pos[0]) + abs(pos[1])

# Calculates lowest number of accumulated steps
def lowest_02(pos):
    return pos[2]

with open("03.data", "r") as f:

    cables = f.read().splitlines()
    #cables = ["R8,U5,L5,D3", "U7,R6,D4,L4"]
    #cables = ["R75,D30,R83,U83,L12,D49,R71,U7,L72", "U62,R66,U55,R34,D71,R55,D58,R83"]
    #cables = ["R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51", "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"]

    grid = dict()
    collisions = []
    for i, c in enumerate(cables):
        collisions += follow_cable(c.split(","), i, grid)

    if len(collisions) > 0:
        print(min(map(lowest_01, collisions)))
        print(min(map(lowest_02, collisions)))

    # solution for 03.01: 1674
    # solution for 03.02: 14012
