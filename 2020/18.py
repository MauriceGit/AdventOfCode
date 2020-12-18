#!/usr/bin/env python3.7

from utility import *

# I know. But we reverse the data before evaluating so we add/mult from the correct side.
# Thus the parenthesis are reversed now...
close_paren = "("
open_paren = ")"

class Mult():
    left  = 0
    right = 0
    fixed = False

    def __init__(self, left, right, fixed):
        self.left  = left
        self.right = right
        self.fixed = fixed

class Add():
    left  = 0
    right = 0
    fixed = False

    def __init__(self, left, right, fixed):
        self.left  = left
        self.right = right
        self.fixed = fixed

# e[0] == (
def extract_paren(e):
    c = 0
    for i, v in enumerate(e):
        if v == close_paren and c == 1:
            # remove )
            return e[1:i], e[i+1:]

        c += v == open_paren
        c -= v == close_paren

    return None

# Creates a tree from the given expression
def create_ast(e):

    if e.isnumeric():
        return int(e)

    if e[0] == open_paren:
        left, rest = extract_paren(e)
        left = create_ast(left)

        left.fixed = True

        if rest == "":
            return left

        r = re.match(r"([+|*])(.*)$", rest)

        op = r.group(1)
        right = create_ast(r.group(2))

    else:

        r = re.match(r"(\d)([+|*])(.*)$", e)
        left = create_ast(r.group(1))
        op = r.group(2)
        right = create_ast(r.group(3))


    if op == "+":
        return Add(left, right, False)
    return Mult(left, right, False)


# Changes the tree according to operator priority!
def reconstruct(t):

    if isinstance(t, int):
        return t

    if isinstance(t, Mult):
        return Mult(reconstruct(t.left), reconstruct(t.right), t.fixed)

    if isinstance(t.left, Mult) and not t.left.fixed:
        return reconstruct(Mult(reconstruct(t.left.left), reconstruct(Add(t.left.right, t.right, True)), t.fixed))

    if isinstance(t.right, Mult) and not t.right.fixed:
        return reconstruct(Mult(reconstruct(Add(t.left, t.right.left, True)), reconstruct(t.right.right), t.fixed))

    left  = reconstruct(t.left)
    right = reconstruct(t.right)

    if isinstance(left, Mult) and not left.fixed or isinstance(right, Mult) and not right.fixed:
        return reconstruct(Add(left, right, t.fixed))

    return Add(left, right, t.fixed)

# Evaluates the given tree and returns the resulting number
def eval_tree(t):
    if isinstance(t, int):
        return t

    if isinstance(t, Mult):
        return eval_tree(t.left) * eval_tree(t.right)

    return eval_tree(t.left) + eval_tree(t.right)


def main():

    lines = open_data("18.data")

    print(sum(eval_tree(create_ast(l[::-1].replace(" ", ""))) for l in lines))
    print(sum(eval_tree(reconstruct(create_ast(l[::-1].replace(" ", "")))) for l in lines))


if __name__ == "__main__":
    main()

# solution for 18.01: 9535936849815
# solution for 18.02: 472171581333710
