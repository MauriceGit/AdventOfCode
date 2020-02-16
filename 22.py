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

def run(commands, cards):
    for c in commands:
        cards = c[0](cards, c[1])

    return cards


# modinv and egcd taken from here: https://stackoverflow.com/questions/4798654/modular-multiplicative-inverse-function-in-python
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)
def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

# Copied, to be safe, but not complex anyway.
def rev_new_stack(i, _, d):
    return d-1-i

def rev_cut(i, n, d):
    # without the + stack_size ??
    return (i+n+d)%d

def rev_incr_n(i, n, d):
    return modinv(n, d) * i%d

def f(commands, i, d):
    for c in commands:
        i = c[0](i, c[1], d)
    return i

#
#
# Took solution from here: https://old.reddit.com/r/adventofcode/comments/ee0rqi/2019_day_22_solutions/fbnifwk/
# Worked through, understood, recreated on paper myself, no idea why I never actually got this idea myself
# ( done the same over and over at university... Maybe just never applied in real life?)
#
#
# f() reverses the chain of commands once for an index!
# All operations are linear.
# So there must be a polynom of the form: A*X+B = Y
# We create two, like:
# X = 2020, Y = f(2020)
# and: A*Y+B = Z
# After substracting them from each other, we get:
#   A = (Y-Z)/(X-Y)
#   B = Y-A*X
# After we have A and B, reapply f a couple of times. Note, that:
# f(f(f(x))) == A*(A*(A*X+B)+B)+B
#            == A^3*X + A^2*B + A*B + B
#            -> A^n*x + (A^n-1) / (A-1) * B
#
# Note: Dividing in space of mod D needs to be replaced by '* modinv' which is the inverse of a normal '*n % d'.

def puzzle_2(commands):

    # Test, if the reversing actually works on the ouput of puzzle 1:
    # Should print: 2019
    #print(f(commands, 2514, 10007))

    d = 119315717514047
    x = 2020
    y = f(commands, x, d)
    z = f(commands, y, d)
    a = (y-z) * modinv(x-y+d, d) % d
    b = (y-a*x) %d
    n = 101741582076661

    return (pow(a, n, d)*x + (pow(a, n, d)-1) * modinv(a-1, d) * b) %d

def main():

    with open("22.data", "r") as f:

        commands = []
        commands_rev = []

        for line in f.read().splitlines():
            if line.startswith("#"):
                continue

            if line.startswith("deal into"):
                commands.append((deal_new_stack, 0))
                commands_rev.insert(0, (rev_new_stack, 0))

            elif line.startswith("cut"):
                commands.append((cut_n, int(line.split(" ")[-1])))
                commands_rev.insert(0, (rev_cut, int(line.split(" ")[-1])))

            elif line.startswith("deal with"):
                commands.append((deal_incr_n, int(line.split(" ")[-1])))
                commands_rev.insert(0, (rev_incr_n, int(line.split(" ")[-1])))

        print("Puzzle 1: {}".format(run(commands, list(range(deck_size))).index(2019)))
        print("Puzzle 2: {}".format(puzzle_2(commands_rev)))

if __name__ == "__main__":
    main()

# solution for 22.01: 2514
# solution for 22.02: 88843646341519
