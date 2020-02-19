from collections import defaultdict






def p(i, end="\n"):
    print("{0:b}".format(i).zfill(25), end=end)


# returns just one bit, if it should stay alive and 0 otherwise
def kill(i, x, y):
    s = y*5+x

    up    = i & (0 if y == 0 else (1<<(s-5)))
    down  = i & (0 if y == 4 else (1<<(s+5)))
    left  = i & (0 if x == 0 else (1<<(s-1)))
    right = i & (0 if x == 4 else (1<<(s+1)))

    if (up | down | left | right) == 0:
        # unset
        return 0
    print("-", end="")
    # all good, bit stays.
    return i & (1<<s)

# returns just one bit at a specific position
def alive(i, x, y):
    s = y*5+x

    up    = i & (0 if y == 0 else (1<<(s-5)))
    down  = i & (0 if y == 4 else (1<<(s+5)))
    left  = i & (0 if x == 0 else (1<<(s-1)))
    right = i & (0 if x == 4 else (1<<(s+1)))

    infested = len(list(filter(lambda x: x != 0, [up, down, left, right])))

    # no bug yet, but should be
    if (i & (1<<s)) == 0 and infested in (1,2):
        print(".", end="")
        return 1<<s
    return 0


def run(i):

    i2 = 0

    p(i)
    print()

    for y in range(5):
        for x in range(5):
            #print(x,y)
            #print(kill(i, x, y))
            #i2 = i2 | kill(i, x, y)
            i2 |= kill(i, x, y) | alive(i, x, y)

            p(i2)
        print()


    p(kill(i, 2, 3))
    p(alive(i, 2, 3))
    print()
    p(i2)







def main():

    with open("24.data", "r") as f:

        s = ""
        for line in f.read().splitlines():
            for v in line:
                s = ("1" if v == "#" else "0") + s

        run(int(s, 2))



        #print("Puzzle 1: {}".format(puzzle_1(field, portals, portal_map, graph)))
        #print("Puzzle 2: {}".format(puzzle_2(field, portals, portal_map, graph)))

if __name__ == "__main__":
    main()

# solution for 20.01: 654
# solution for 20.02: 7360
