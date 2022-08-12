from itertools import combinations_with_replacement, combinations, permutations
import pickle as pkl

raw_combis = combinations_with_replacement((0, 1, 2), 5)
combis = set()

for combi in raw_combis:
    perms = permutations(combi)

    for i in perms:
        combis.add(i)

combis = sorted(list(combis))

with open('src/data/combis.pkl', 'wb') as f:
    pkl.dump(combis, f)
