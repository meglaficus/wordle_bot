import pandas as pd
import numpy as np
from tqdm import tqdm

with open('data/allowed.txt', 'r') as f:
    words = [i.strip() for i in f.readlines()]

df = pd.read_csv('data/unigram_freq.csv')

word_set = set(words)
word_dict = {}
total_number = 0

# I'm not very good at pandas yes I know
for ind in tqdm(df.index):
    row = df.loc[ind]
    word, count = row['word'], int(row['count'])
    if word in word_set:
        word_dict[word] = count
        total_number += count

print(word_dict)

count_list = [i for i in word_dict.values()]
smallest = min(count_list)

for word in word_set:
    if word not in word_dict:
        word_dict[word] = smallest
        print(word)
