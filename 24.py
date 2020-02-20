
def p(i, end="\n"):
    print("{0:b}".format(i).zfill(25), end=end)



# returns just one bit, if it should stay alive and 0 otherwise
def kill(i, x, y, level, infested):
    s = y*5+x

    if infested(i, x, y, s, level) != 1:
        # unset
        return 0
    # all good, bit stays.
    return i & (1<<s)

# returns just one bit at a specific position
def alive(i, x, y, level, infested):
    s = y*5+x

    # no bug yet, but should be
    if (i & (1<<s)) == 0 and infested(i, x, y, s, level) in (1,2):
        return 1<<s
    return 0

# returns the count of neighbor bugs
def infested_puzzle_1(i, x, y, s, _):
    up    = i & (0 if y == 0 else (1<<(s-5)))
    down  = i & (0 if y == 4 else (1<<(s+5)))
    left  = i & (0 if x == 0 else (1<<(s-1)))
    right = i & (0 if x == 4 else (1<<(s+1)))

    return len(list(filter(lambda x: x != 0, [up, down, left, right])))

def one_epoche_puzzle_1(i):

    i2 = 0
    for y in range(5):
        for x in range(5):
            i2 |= kill(i, x, y, 0, infested_puzzle_1) | alive(i, x, y, 0, infested_puzzle_1)
    return i2

def run_puzzle_1(i):

    s = set()
    while True:
        i = one_epoche_puzzle_1(i)
        if i in s:
            return i
        s.add(i)
    return None


def main():

    with open("24.data", "r") as f:

        s = ""
        for line in f.read().splitlines():
            for v in line:
                s = ("1" if v == "#" else "0") + s

        print("Puzzle 1: {}".format(run_puzzle_1(int(s, 2))))


if __name__ == "__main__":
    main()

# solution for 24.01: 18407158
# solution for 24.02:
