from tqdm import tqdm
import numpy as np
import pickle as pkl
from rich.console import Console
from backend import use_clues


console = Console()
with open('data/combis.pkl', 'rb') as file:
    combis = pkl.load(file)


def test_it():
    with open('data/test1.txt', 'r') as f:
        list_of_words = [i.strip() for i in f.readlines()]

    result = []
    for my_word in tqdm(list_of_words):
        y = 0

        for thing in combis:
            list_of_words2 = use_clues(
                my_word, thing, list_of_words)

            x = len(list_of_words2) / len(list_of_words)
            if x:
                y += x * np.log2(1 / x)

        result.append((y, my_word))

    print(sorted(result, reverse=True)[:10])


if __name__ == "__main__":
    test_it()
