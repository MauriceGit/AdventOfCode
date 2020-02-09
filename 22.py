from collections import defaultdict

deck_size = 10007
#deck_size = 17

def deal_new_stack(cards, _):
    return list(reversed(cards))

def cut_n(cards, n):
    return cards[n:] + cards[:n]

def deal_incr_n(cards, n):
    l = [0]*deck_size
    length = len(cards)
    for i,c in enumerate(cards):
        l[(i*n)%length] = c
    return l

def run(commands, cards):



    for c in commands:
        cards = c[0](cards, c[1])

    return cards


def puzzle_2():

    #print([ ((i+2) *-4)%17 for i in range(17)])


    l = [0]*deck_size

    for i, v in enumerate(range(17)):
        l[(((i-2) *4)+2)%17] = v

    print(l)




def main():

    with open("22.data", "r") as f:

        commands = []

        index = 2019

        for line in f.read().splitlines():
            if line.startswith("#"):
                continue

            if line.startswith("deal into"):
                commands.append((deal_new_stack, 0))

                index = ((deck_size-1)-index)#%deck_size

            elif line.startswith("cut"):
                commands.append((cut_n, int(line.split(" ")[-1])))

                index = (index-int(line.split(" ")[-1]))#%deck_size

            elif line.startswith("deal with"):
                commands.append((deal_incr_n, int(line.split(" ")[-1])))

                index = (index*int(line.split(" ")[-1]))#%deck_size

        #print((index)%deck_size)

        #commands *= 4

        cards = list(range(deck_size))
        out = cards

        for i in range(2):
            out = run(commands, out)



        for i in range (1, 10):
            print("{} - {}: {}".format(i-1, i, (out.index(i)-out.index(i-1))%deck_size))

        print("Puzzle 1: {}".format(out.index(0)))
        print("Puzzle 1: {}".format(out.index(1)))
        print("Puzzle 1: {}".format(out.index(3000)))
        #print("Puzzle 1: {}".format(run(commands).index(2019)))

        print("Puzzle 1: {}".format(out[6000]))


        #puzzle_2()


if __name__ == "__main__":
    main()

# solution for 22.01: 2514
# solution for 22.02:
