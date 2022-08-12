import torch as t
import numpy as np
import pickle as pkl
from rich.console import Console
from tqdm import tqdm
import hashlib

gpu_ids = []
if t.cuda.is_available():
    gpu_ids += [gpu_id for gpu_id in range(t.cuda.device_count())]
    device = t.device(f'cuda:{gpu_ids[0]}')
    t.cuda.set_device(device)
else:
    print('WARNING: No CUDA devices found! Running on CPU.')
    device = t.device('cpu')

slice_kernel = t.tensor([[[0, 0, 0, 0, 0],
                        [1, 0, 0, 0, 0],
                        [1, 1, 0, 0, 0],
                        [1, 1, 1, 0, 0],
                        [1, 1, 1, 1, 0]]], dtype=t.int8, device=device)


def get_base_matrices(word_list, clues):

    combis = t.tensor(clues, device=device)

    words = [[ord(j) for j in i.strip()] for i in word_list]
    words = t.tensor(words, dtype=t.int8, device=device)

    vert_words = words[:, None, :].transpose(1, 2)

    entropies = t.zeros(len(word_list), device=device)
    combis_e = combis[:, None, :]

    return combis_e, words, vert_words, entropies


def get_combined_results(words, vert_words, combis_e, ind):
    
    position_sums = t.where((vert_words - words[ind]) == 0, 1, 0)[None, :].sum(dim=2)

    orig_word_counts = t.where((vert_words[ind] - words[ind] == 0) & (combis_e != 0), 1, 0)
    orig_word_counts_sum = orig_word_counts.sum(dim=1)[:, None, :]
    
    compare_counts = t.where((words - words[ind]) == 0, 1, 0)[None, :]

    hard_filtered = t.where((combis_e == 0), orig_word_counts, 0) * slice_kernel

    position_check = t.where((compare_counts == combis_e) | (combis_e - 2 == compare_counts) , 1, 0)
    position_results = t.where(t.sum(position_check, dim=2) == 5, 1, 0)
    
    hs_check = t.where(((orig_word_counts_sum == position_sums) & (combis_e == 0)) | ((orig_word_counts_sum <= position_sums) & (combis_e == 2)) | (combis_e == 1), 1, 0)

    combined_results = t.where((position_results == 1) & (t.all(hs_check == 1, dim=2)) & (hard_filtered.sum((1,2))[:, None] == 0), 1, 0)

    return combined_results


def get_all_entropy(word_list, probs):
    with open('data/combis.pkl', 'rb') as file:
        combis = pkl.load(file)

    combis_e, words, vert_words, entropies = get_base_matrices(
        word_list, combis)

    length_tensor = t.sum(probs)
    
    for ind in range(len(word_list)):
        combined_results = get_combined_results(
            words, vert_words, combis_e, ind)
        
        combined_results = combined_results * probs
        results_sums = combined_results.sum(dim=1)
        
        results_sums_frac = t.divide(results_sums, length_tensor)
        result_entropy = t.where(
            results_sums != 0, results_sums_frac * t.log2(1/results_sums_frac), 0)

        entropies[ind] = result_entropy.sum()
        entropies = entropies * probs

    return entropies


def filter_words(word, word_list, clue):
    console = Console()
    with console.status('[bold blue]Thinking...') as status:
        
        clue = [[int(i) for i in clue]]

        combis_e, words, vert_words, entropies = get_base_matrices(word_list, clue)
        ind = word_list.index(word)
        
        combined_results = get_combined_results(words, vert_words, combis_e, ind)
        combined_results = np.array(combined_results[0].cpu())

        legal_words = [i for j, i in enumerate(word_list) if combined_results[j] != 0]
        
        with open('data/word_probs.pkl', 'rb') as file:
            word_dict = pkl.load(file)
            
        probs = t.tensor([word_dict[i] for i in legal_words], device=device)

        entropies = get_all_entropy(legal_words, probs)
        

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
    # will produce the optimal first word
    with open('data/allowed_words.pkl', 'rb') as file:
        word_list = pkl.load(file)
        
    with open('data/word_probs.pkl', 'rb') as file:
        word_dict = pkl.load(file)
    
    with open('data/combis.pkl', 'rb') as file:
        combis = pkl.load(file)
    
    probs = t.tensor([word_dict[i] for i in word_list], device=device)
    
    combis_e, words, vert_words, entropies = get_base_matrices(
        word_list, combis)

    length_tensor = t.sum(probs)
    
    for ind in tqdm(range(len(word_list))):
        combined_results = get_combined_results(
            words, vert_words, combis_e, ind)
        
        combined_results = combined_results * probs
        results_sums = combined_results.sum(dim=1)
        
        results_sums_frac = t.divide(results_sums, length_tensor)
        result_entropy = t.where(
            results_sums != 0, results_sums_frac * t.log2(1/results_sums_frac), 0)

        entropies[ind] = result_entropy.sum()
        entropies = entropies * probs
        

    pairs = sorted(
        [i for i in zip(np.array(entropies.cpu()), word_list)], reverse=True)
    
    with open('data/text_files/best_first_words.txt', 'w') as file:
        for score, word in pairs:
            file.write(f'{word}: {score}\n')
            
    for i in range(10):
        value, word = pairs[i]
        print(f'{i + 1}   {word}   {value}')
        