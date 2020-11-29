from recordtype import recordtype
from collections import defaultdict
import math


# n A ==> ([m, ORE], surplus A)
# Chem(quantity=1, ingredients=[Ingredient(quantity=7, chem='A'), Ingredient(quantity=1, chem='B')])
def convert(n, c, chems_rel):
    res_chems = chems_rel[c]
    mult = math.ceil(n / res_chems.quantity)
    total = mult * res_chems.quantity
    extra = total - n

    new_ingredients = [Ingredient(mult*i.quantity, i.chem) for i in res_chems.ingredients]
    return (new_ingredients, extra)


def reduce_layer(amounts, chems_rel, chems_extra):

    for k in list(amounts.keys()):
        cnt = amounts[k]

        if k == "ORE":
            continue

        # This chemical will be replaced by its ingredients.
        del amounts[k]

        # No need to substitute, we already have enough of k.
        if chems_extra[k] >= cnt:
            chems_extra[k] -= cnt
            continue

        final_cnt = cnt - chems_extra[k]
        # We use all we have (if not, we continue above).
        del chems_extra[k]

        new_list, extra = convert(final_cnt, k, chems_rel)
        chems_extra[k] += extra

        for new in new_list:
            amounts[new.chem] += new.quantity

    return amounts

def reduce_fuel_to_ore(chems_rel, fuel_cnt):

    chems_extra = defaultdict(int)
    amounts = defaultdict(int)
    amounts["FUEL"] = fuel_cnt

    while "FUEL" in amounts or len(amounts) > 1:
        amounts = reduce_layer(amounts, chems_rel, chems_extra)

    return amounts["ORE"]

if __name__ == "__main__":

    chems_rel = dict()

    chems_rel["ORE"] = []

    Ingredient = recordtype("Ingredient", "quantity chem")
    Chem = recordtype("Chem", "quantity ingredients")

    with open("14.data", "r") as f:
        for l in f.read().splitlines():
            ingr, dest = l.split("=>")
            ingr = ingr.split(",")
            ingr = list(map(lambda x: x.strip(), ingr))

            ingr = list(map(lambda x: Ingredient(int(x.split(" ")[0]), x.split(" ")[1]), ingr))
            dest = dest.strip().split(" ")

            chems_rel[dest[1]] = Chem(int(dest[0]), ingr)

    # solution for the first puzzle
    print(reduce_fuel_to_ore(chems_rel, 1))

    last_ore_cnt = 0
    current_ore_cnt = 0
    n = 0
    incr = 1000000
    # binary search for the correct amount of fuel!
    while incr > 1:
        incr //= 10
        last_ore_cnt = 0
        current_ore_cnt = 0
        while current_ore_cnt <= 1000000000000:
            n += incr
            last_ore_cnt = current_ore_cnt
            current_ore_cnt = reduce_fuel_to_ore(chems_rel, n)
        # Back to the last still valid fuel count.
        n -= incr

    # solution for the second puzzle
    print(n)

# solution for 14.01: 387001
# solution for 14.02: 3412429
