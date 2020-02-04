from collections import defaultdict

deck_size = 10007

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

def run(commands):

    cards = list(range(deck_size))

    for c in commands:
        cards = c[0](cards, c[1])

    return cards


def main():

    with open("22.data", "r") as f:

        commands = []

        for line in f.read().splitlines():

            if line.startswith("deal into"):
                commands.append((deal_new_stack, 0))
            elif line.startswith("cut"):
                commands.append((cut_n, int(line.split(" ")[-1])))
            elif line.startswith("deal with"):
                commands.append((deal_incr_n, int(line.split(" ")[-1])))

        cards = run(commands)

        for i,c in enumerate(cards):
            if c == 2019:
                print(i)




if __name__ == "__main__":
    main()

# solution for 22.01:
# solution for 22.02:
