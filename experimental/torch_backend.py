import torch as t
import numpy as np
import pickle as pkl
from tqdm import tqdm

cuda0 = t.device('cuda:0')

with open('data/answers.txt', 'r') as f:
    actual_words = [i.strip() for i in f.readlines()]

with open('data/combis.pkl', 'rb') as file:
    combis = t.tensor(pkl.load(file), device=cuda0)


words = [[[ord(j) for j in i]] for i in actual_words]
words0 = [[ord(j) for j in i.strip()] for i in actual_words]

words = t.tensor(words, dtype=t.int8, device=cuda0)
words0 = t.tensor(words0, dtype=t.int8, device=cuda0)


vert_words = words.transpose(1, 2)
entropies = t.zeros(len(words), device=cuda0)

combis_e0 = combis[:, None, :]


for ind in tqdm(range(len(words))):

    positions = t.where((vert_words - words0[ind]) == 0, 1, 0)

    position_sums = positions.sum(dim=1)
    position_sums = position_sums[None, :]

    orig_word_counts0 = t.where(
        (vert_words[ind] - words0[ind]) == 0, 1, 0)

    orig_word_counts0 = orig_word_counts0[None, :]
    orig_word_counts = t.where(
        combis_e0 != 0, orig_word_counts0, 0).sum(dim=1)

    compare_counts = t.where((words0 - words0[ind]) == 0, 1, 0)
    # print(compare_counts)
    compare_counts = compare_counts[None, :]

    combis_e = combis[:, None, :]
    orig_word_counts = orig_word_counts[:, None, :]

    hard_counts = t.where(combis_e == 0, orig_word_counts, 6)
    soft_counts = t.where(combis_e == 2, orig_word_counts, 6)

    hard_filtered = t.where((hard_counts < 6) & (
        hard_counts > 0), orig_word_counts0, 0)

    slice_kernel = t.tensor([[1, 1, 1, 1, 1],
                            [0, 1, 1, 1, 1],
                            [0, 0, 1, 1, 1],
                            [0, 0, 0, 1, 1],
                            [0, 0, 0, 0, 1]], dtype=t.int8, device=cuda0)
    slice_kernel = slice_kernel[None, :]

    hard_filtered = t.where(slice_kernel == 0, hard_filtered, 0)

    dup_check_result = t.where(hard_filtered.sum(1).sum(1) == 0, 1, 0)

    position_check_pos = t.where(combis_e == 1, compare_counts, 1)
    position_check_neg = t.where(
        (combis_e == 0) | (combis_e == 2), compare_counts, 0)
    position_check_neg = t.where(position_check_neg == 0, 1, 0)

    position_results = t.where((t.sum(position_check_pos, dim=2) == 5) & (
        t.sum(position_check_neg, dim=2) == 5), 1, 0)

    hard_check = t.where((hard_counts == position_sums)
                         | (hard_counts == 6), 1, 0)
    soft_check = t.where((soft_counts <= position_sums)
                         | (soft_counts == 6), 1, 0)

    hard_results = t.where(t.all(hard_check == 1, dim=2), 1, 0)
    soft_results = t.where(t.all(soft_check == 1, dim=2), 1, 0)

    combined_results = t.where((position_results == 1) & (
        hard_results == 1) & (soft_results == 1) & (dup_check_result[:, None] == 1), 1, 0)

    results_sums = combined_results.sum(dim=1)

    result_entropy = t.where(
        results_sums != 0, (results_sums/len(words)) * t.log2(1/(results_sums/len(words))), 0)

    entropies[ind] = result_entropy.sum()

    pairs = sorted(
        [i for i in zip(np.array(entropies.cpu()), actual_words)], reverse=True)


print(pairs[:5])
