import torch as t
import numpy as np
import pickle as pkl
from tqdm import tqdm

cuda0 = t.device('cuda:0')

with open('data\mini_single_test.txt', 'r') as f:
    actual_words = [i.strip() for i in f.readlines()]

with open('data/combis.pkl', 'rb') as file:
    combis = t.tensor(pkl.load(file), device=cuda0)


words = [[[ord(j) for j in i]] for i in actual_words]
words0 = [[ord(j) for j in i.strip()] for i in actual_words]

words = t.tensor(words, dtype=t.int8, device=cuda0)
words0 = t.tensor(words0, dtype=t.int8, device=cuda0)


vert_words = words.transpose(1, 2)

entropies = t.zeros(len(words), device=cuda0)

combis_e0 = combis[:, None, :].transpose(1, 2)

for ind in tqdm(range(1)):
    positions = t.where((vert_words - words[ind, 0, :]) == 0, 1, 0)
    position_sums = positions.sum(dim=1)
    position_sums = position_sums[None, :]

    orig_word_counts = t.where(
        (vert_words[ind] - words[ind, 0]) == 0, 1, 0)

    orig_word_counts = orig_word_counts[None, :]

    orig_word_counts = t.where(combis_e0 != 0, orig_word_counts, 0).sum(dim=1)

    compare_counts = t.where((words0 - words0[ind]) == 0, 1, 0)
    compare_counts = compare_counts[None, :]

    combis_e = combis[:, None, :]
    orig_word_counts = orig_word_counts[:, None, :]

    # these have to be tweaked in order to work with multiple letters - this should now work

    # also need to add checks for scenarios that do not come up in the actual game!!!
    # ie. there can not be a combination of hints where there is grey letter before a green/yellow letter if the letter is the same.

    hard_counts = t.where(combis_e == 0, orig_word_counts, 6)
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
