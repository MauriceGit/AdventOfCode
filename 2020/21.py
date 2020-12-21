#!/usr/bin/env python3.7

from utility import *

Food = namedtuple("Food", "ingr allergen")


# returns dict of allergen -> ingredient.
def solve_allergen(allergen_ingr):

    res = dict()

    while True:
        found = False
        for k, ingr in allergen_ingr.items():
            if len(ingr) == 1:
                # remove ingr from every recipe
                for kk in allergen_ingr:
                    allergen_ingr[kk] = allergen_ingr[kk] - ingr

                res[k] = ingr
                found = True
                break
        if not found:
            break

    return res

def main():

    lines = open_data("21.data")

    recipe = []
    allergens = set()
    food = set()

    for l in lines:
        ingr, aller = l.split(" (contains ")
        aller = aller[:-1].split(", ")
        ingr = ingr.split(" ")
        recipe.append(Food(ingr, aller))
        allergens = allergens | set(aller)
        food = food | set(ingr)


    unsafe = set()

    allergen_ingr = dict()
    for a in allergens:
        res = set()
        for f in recipe:
            if a in f.allergen:
                if len(res) == 0:
                    res = set(f.ingr)
                else:
                    res = res & set(f.ingr)
        allergen_ingr[a] = res
        unsafe = unsafe | res

    print(sum(s in r.ingr for s in food ^ unsafe for r in recipe))


    res = solve_allergen(allergen_ingr)
    res = [(k,*v) for k,v in res.items()]
    print(",".join(lmap(itemgetter(1), sorted(res, key=itemgetter(0)))))


if __name__ == "__main__":
    main()

# solution for 21.01: 2176
# solution for 21.02: lvv,xblchx,tr,gzvsg,jlsqx,fnntr,pmz,csqc
