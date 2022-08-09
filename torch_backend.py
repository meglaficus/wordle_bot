import torch as t
import numpy as np
import pickle as pkl
from tqdm import tqdm

cuda0 = t.device('cuda:0')

with open('data\mini_single_test.txt', 'r') as f:
    actual_words = [i.strip() for i in f.readlines()]

words = [[[ord(j) for j in i]] for i in actual_words]
words0 = [[ord(j) for j in i.strip()] for i in actual_words]

with open('data/combis.pkl', 'rb') as file:
    combis = t.tensor(pkl.load(file), device=cuda0)


words = t.tensor(words, dtype=t.int8, device=cuda0)
words0 = t.tensor(words0, dtype=t.int8, device=cuda0)


vert_words = words.transpose(1, 2)

entropies = t.zeros(len(words), device=cuda0)


for ind in tqdm(range(len(words))):
    positions = t.where((vert_words - words[ind, 0, :]) == 0, 1, 0)
    position_sums = positions.sum(dim=1)
    position_sums = position_sums[None, :]

    orig_word_counts = t.where(
        (vert_words[ind] - words[ind, 0]) == 0, 1, 0).sum(dim=1)

    orig_word_counts = orig_word_counts[None, :]

    compare_counts = t.where((words0 - words0[ind]) == 0, 1, 0)

    hard_counts = t.ones((len(combis), 5),
                         dtype=t.int8, device=cuda0)

    soft_counts = t.ones((len(combis), 5),
                         dtype=t.int8, device=cuda0)

    combis_e = combis[:, None, :]

    # these have to be tweaked in order to work with multiple letters
    # also need to add checks for duplicate scenarios that do not come up in the actual game

    hard_counts = t.where(combis_e == 0, orig_word_counts - 1, 6)
    soft_counts = t.where(combis_e == 2, orig_word_counts, 6)

    position_check_pos = t.where(combis_e == 1, position_sums, 1)
    position_check_neg = t.where(
        (combis_e == 0) | (combis_e == 2), position_sums, 0)
    position_check_neg = t.where(position_check_neg == 0, 1, 0)

    position_results = t.where((t.all(position_check_pos == 1, dim=2)) & (
        t.all(position_check_neg == 1, dim=2)), 1, 0)

    hard_check = t.where((hard_counts == compare_counts)
                         | (hard_counts == 6), 1, 0)
    soft_check = t.where((soft_counts <= compare_counts)
                         | (soft_counts == 6), 1, 0)

    hard_results = t.where(t.all(hard_check == 1, dim=2), 1, 0)
    soft_results = t.where(t.all(soft_check == 1, dim=2), 1, 0)

    combined_results = t.where((position_results == 1) & (
        hard_results == 1) & (soft_results == 1), 1, 0)

    results_sums = combined_results.sum(dim=1)

    result_entropy = t.where(
        results_sums != 0, results_sums/len(words) * t.log2(1/(results_sums/len(words))), 0)

    entropies[ind] = result_entropy.sum()

pairs = sorted(
    [i for i in zip(np.array(entropies.cpu()), actual_words)], reverse=True)

print(pairs[:5])

# x = t.tensor([1, 2, 3])
# y = t.tensor([[3], [2], [5]])

# z = x - y

# compare_matrix = t.where(z == 0, 1, 0)
# print(x)
# print(y)
# print()
# print(z)
# print()
# print(compare_matrix)


# clues = t.tensor([0, 1, 2])

# output = t.empty(3)
# output = t.where(clues == 0, x, output)

# for ind, clue in enumerate(clues):
#     if clue == 0:
#         output[ind] = t.all(compare_matrix[:, ind] == 0)

#     elif clue == 1:
#         output[ind] = compare_matrix[ind, ind] == 1

#     elif clue == 2:
#         output[ind] = (t.all(compare_matrix[ind, ind] == 0)) & (t.any(
#             compare_matrix[:, ind] == 1))

# print(output)

# cond_list = [arr < 3, arr > 4]
# choice_list = [arr, arr**3]

# gfg = geek.select(condlist, choicelist)
