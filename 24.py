from collections import defaultdict

def p(i, end="\n"):
    print("{0:b}".format(i).zfill(25), end=end)



# returns just one bit, if it should stay alive and 0 otherwise
def kill(i, x, y, level, infested, i_dict):
    s = y*5+x

    if infested(i, x, y, s, level, i_dict) != 1:
        # unset
        return 0
    # all good, bit stays.
    return i & (1<<s)

# returns just one bit at a specific position
def alive(i, x, y, level, infested, i_dict):
    s = y*5+x

    # no bug yet, but should be
    if (i & (1<<s)) == 0 and infested(i, x, y, s, level, i_dict) in (1,2):
        return 1<<s
    return 0

# returns the count of neighbor bugs
# we ignore the level and i_dict parameters. Those are only needed for puzzle_2.
def infested_puzzle_1(i, x, y, s, *_):
    up    = i & (0 if y == 0 else (1<<(s-5)))
    down  = i & (0 if y == 4 else (1<<(s+5)))
    left  = i & (0 if x == 0 else (1<<(s-1)))
    right = i & (0 if x == 4 else (1<<(s+1)))

    return len(list(filter(lambda x: x != 0, [up, down, left, right])))

# returns set bits for a whole row (5 values). first/last row!
# 31 == 11111, 32505856 == 11111'00000'00000'00000'00000
def get_row(first_row):
    return 31 if first_row else 32505856

# returns set bits for a whole row (5 values). first/last row!
# 17318416 == 1000010000100001000010000, 1082401 == 0000100001000010000100001
def get_col(first_col):
    return 17318416 if first_col else 1082401

# i_dict is a dictionary: "level -> i" used to query different levels
# we ignore the i parameter, as we can read it from the dict ourselves (for consistency).
def infested_puzzle_2(_, x, y, s, level, i_dict):

    i     = i_dict[level]
    i_in  = i_dict[level+1]
    i_out = i_dict[level-1]

    if y == 3 and x == 2:
        up = i_in & get_row(False)
    else:
        up = (i_out & (1<<7)) if y == 0 else (i & (1<<(s-5)))

    if y == 1 and x == 2:
        down = i_in & get_row(True)
    else:
        down = (i_out & (1<<17)) if y == 4 else (i & (1<<(s+5)))

    if x == 3 and y == 2:
        left = i_in & get_col(False)
    else:
        left = (i_out & (1<<11)) if x == 0 else (i & (1<<(s-1)))

    if x == 1 and y == 2:
        right = i_in & get_col(True)
    else:
        right = (i_out & (1<<13)) if x == 4 else (i & (1<<(s+1)))

    return sum(map(lambda x: bin(x).count("1"), [up, down, left, right]))


def one_epoche(i, infested, level=0, i_dict=None, exclude_center=False):

    i2 = 0
    for y in range(5):
        for x in range(5):

            if exclude_center and x == 2 and y == 2:
                continue

            i2 |= kill(i, x, y, level, infested, i_dict) | alive(i, x, y, level, infested, i_dict)
    return i2

def run_puzzle_1(i):

    s = set()
    while True:
        i = one_epoche(i, infested_puzzle_1)
        if i in s:
            return i
        s.add(i)
    return None

def run_puzzle_2(i):

    d = defaultdict(int)
    d[0] = i
    for _ in range(10):
        new_d = defaultdict(int)

        max_level = 0
        min_level = 0

        # recalculate all maps.
        for level in d.copy():
            new_d[level] = one_epoche(_, infested_puzzle_2, level, d.copy(), True)
            max_level = max(level, max_level)
            min_level = min(level, min_level)

        # Every iteration, we can potentially go one level higher/deeper.
        new_d[max_level+1] = one_epoche(_, infested_puzzle_2, max_level+1, d, True)
        new_d[min_level-1] = one_epoche(_, infested_puzzle_2, min_level-1, d, True)

        d = new_d.copy()
    p(d[0])



def main():

    with open("24.data", "r") as f:

        s = ""
        for line in f.read().splitlines():
            for v in line:
                s = ("1" if v == "#" else "0") + s

        print("Puzzle 1: {}".format(run_puzzle_1(int(s, 2))))
        print("Puzzle 1: {}".format(run_puzzle_2(int(s, 2))))


if __name__ == "__main__":
    main()

# solution for 24.01: 18407158
# solution for 24.02:
