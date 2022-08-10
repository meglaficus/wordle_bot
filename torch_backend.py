import torch as t
import numpy as np
import pickle as pkl
from rich.console import Console

gpu_ids = []
if t.cuda.is_available():
    gpu_ids += [gpu_id for gpu_id in range(t.cuda.device_count())]
    device = t.device(f'cuda:{gpu_ids[0]}')
    t.cuda.set_device(device)
else:
    print('WARNING: No CUDA devices found! Running on CPU.')
    device = t.device('cpu')


def get_base_matrices(word_list, clues):

    combis = t.tensor(clues, device=device)

    words = [[ord(j) for j in i.strip()] for i in word_list]
    words = t.tensor(words, dtype=t.int8, device=device)

    vert_words = words[:, None, :].transpose(1, 2)
    combis_e0 = combis[:, None, :]

    entropies = t.zeros(len(word_list), device=device)

    return combis, words, vert_words, combis_e0, entropies


def get_combined_results(words0, vert_words, combis, ind, combis_e0):
    positions = t.where((vert_words - words0[ind]) == 0, 1, 0)

    position_sums = positions.sum(dim=1)
    position_sums = position_sums[None, :]

    orig_word_counts0 = t.where(
        (vert_words[ind] - words0[ind]) == 0, 1, 0)

    orig_word_counts0 = orig_word_counts0[None, :]
    orig_word_counts = t.where(
        combis_e0 != 0, orig_word_counts0, 0).sum(dim=1)

    compare_counts = t.where((words0 - words0[ind]) == 0, 1, 0)
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
                            [0, 0, 0, 0, 1]], dtype=t.int8, device=device)

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

    return combined_results


def get_all_entropy(word_list):
    with open('data/combis.pkl', 'rb') as file:
        combis_base = pkl.load(file)

    combis, words, vert_words, combis_e0, entropies = get_base_matrices(
        word_list, combis_base)

    for ind in range(len(word_list)):
        combined_results = get_combined_results(
            words, vert_words, combis, ind, combis_e0)
        results_sums = combined_results.sum(dim=1)

        result_entropy = t.where(
            results_sums != 0, (results_sums/len(word_list)) * t.log2(1/(results_sums/len(word_list))), 0)

        entropies[ind] = result_entropy.sum()

    return entropies


def filter_words(word, word_list, clue):
    console = Console()
    with console.status('[bold blue]Thinking...') as status:

        clue = [[int(i) for i in clue]]

        combis, words, vert_words, combis_e0, entropies = get_base_matrices(
            word_list, clue)
        ind = word_list.index(word)

        combined_results = get_combined_results(
            words, vert_words, combis, ind, combis_e0)
        combined_results = np.array(combined_results[0].cpu())

        legal_words = [i for j, i in enumerate(
            word_list) if combined_results[j] == 1]

        entropies = get_all_entropy(legal_words)

        pairs = sorted(
            [i for i in zip(np.array(entropies.cpu()), legal_words)], reverse=True)

        best_score = 0
        best_word = pairs[0][1]
        for score, word in pairs:
            if score > best_score:
                best_score = score
                best_word = word

    return legal_words, best_word


if __name__ == '__main__':
    # purely for testing purposes
    with open('data/allowed.txt', 'r') as f:
        word_list = [i.strip() for i in f.readlines()]

    entropies = get_all_entropy(word_list)

    pairs = sorted(
        [i for i in zip(np.array(entropies.cpu()), word_list)], reverse=True)

    print(pairs[:5])
