


def add_p(p, p2):
    return (p[0]+p2[0], p[1]+p2[1])

def draw(f, symbols=None, print_directly=False, flip=False):

    if symbols == None:
        symbols = {-1: "█", 0: "█", 1: " ", 2: "0", 3: "#", 4: "X"}

    min_x = min(f.keys(), key=lambda x: x[0])[0]
    min_y = min(f.keys(), key=lambda x: x[1])[1]
    max_x = max(f.keys(), key=lambda x: x[0])[0]
    max_y = max(f.keys(), key=lambda x: x[1])[1]

    y_range = range(min_y, max_y+1)
    if flip:
        y_range = reversed(y_range)

    for y in y_range:
        for x in range(min_x, max_x+1):

            p = (x,y)
            if p not in f:
                c = -1
            else:
                c = f[p]

            if c not in symbols:
                if print_directly:
                    symbols[c] = c
                else:
                    symbols[c] = "?"

            print(symbols[c], end="")

        print("")
