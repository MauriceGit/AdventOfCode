from collections import defaultdict
from sympy import mod_inverse


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


def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv_(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

modinv = lambda A, n,s=1,t=0,N=0: (n < 2 and t%N or modinv(n, A%n, t, s-A//n*t, N or n),-1)[n<1]

def rev_new_stack(i, _, d):
    return d-1-i

def rev_cut(i, n, d):
    # without the + stack_size ??
    return (i+n+d)%d

def rev_incr_n(i, n, d):
    return modinv_(n, d) * i%d

def f(commands, i, d):
    for c in commands:
        i = c[0](i, c[1], d)
    return i


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

def puzzle_2(commands):

    print(f(commands, 2514, 10007))


    d = 119315717514047
    x = 2020
    y = f(commands, x, d)
    z = f(commands, y, d)
    a = (y-z) * modinv_(x-y+d, d) % d
    b = (y-a*x) %d
    n = 101741582076661

    print(a,b)

    return (pow(a, n, d)*x + (pow(a, n, d)-1) * modinv_(a-1, d) * b) %d

    # 61413248796526 too low





def main():

    with open("22.data", "r") as f:

        commands = []
        commands_rev = []

        index = 2019

        for line in f.read().splitlines():
            if line.startswith("#"):
                continue

            if line.startswith("deal into"):
                commands.append((deal_new_stack, 0))
                commands_rev.append((rev_new_stack, 0))

            elif line.startswith("cut"):
                commands.append((cut_n, int(line.split(" ")[-1])))
                commands_rev.append((rev_cut, int(line.split(" ")[-1])))

            elif line.startswith("deal with"):
                commands.append((deal_incr_n, int(line.split(" ")[-1])))
                commands_rev.append((rev_incr_n, int(line.split(" ")[-1])))
        commands_rev = reversed(commands_rev)

        print(run(commands, list(range(deck_size))).index(2019))

        print(puzzle_2(commands_rev))

if __name__ == "__main__":
    main()

# solution for 22.01: 2514
# solution for 22.02:
