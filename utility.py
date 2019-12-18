
def draw(f, symbols=None):

    if symbols == None:
        symbols = {-1: "█", 0: "█", 1: " ", 2: "0", 3: "#", 4: "X"}

    min_x = min(f.keys(), key=lambda x: x[0])[0]
    min_y = min(f.keys(), key=lambda x: x[1])[1]
    max_x = max(f.keys(), key=lambda x: x[0])[0]
    max_y = max(f.keys(), key=lambda x: x[1])[1]

    for y in range(min_y, max_y+1):
        for x in range(min_x, max_x+1):

            p = (x,y)
            if p not in f:
                c = -1
            else:
                c = f[p]

            if c not in symbols:
                symbols[c] = "?"

            print(symbols[c], end="")

        print("")

