import re
import string
import numpy as np

from itertools import combinations_with_replacement
from itertools import permutations
import pickle
from math import log2

# word_dict = {i:set() for i in string.ascii_lowercase}

with open('5words.txt') as words:
    word_list = [i.strip() for i in words.readlines()]

print('creating_counts')

counts =  np.zeros((len(word_list), len(word_list), 3**5), dtype='int')

test = np.zeros((2, 3, 4))

print(test)

print(test[0, 0])


# for ind, word in enumerate(word_list):
#     for ind2, other_word in enumerate(word_list):
#         if ind == ind2:
#             continue
#         if any(i in other_word for i in word):
#             counts[ind, ind2] = 1

# for column in range(len(counts[0] - 1)):
#     print(sum(counts[:, column]))        
        

# for word in word_list:
#     for letter in word:
#         word_dict[letter].add(word)

# win = False
# new_word = 'arose'
    
# counts = float('inf')

# for word in word_list:
#     for letter in word:
#         count = len(word_dict[letter])

word_locs = {value:i for i,value in enumerate(word_list)}

print('combining')

my_combinations = combinations_with_replacement(range(3), 5)

combis = set()

for thing in my_combinations:
    my_permutations = permutations(thing)
    for other_thing in my_permutations:
        combis.add(other_thing)
    
combis = sorted(list(combis))

with open('combis.pkl', 'wb') as file:
    pickle.dump(combis, file)

# combis = pickle.load(combis)
# print(combis)

def use_clues(word, clues, list_of_words):
    
    working_clues = zip(clues, [i for i in my_word])
    
    for ind, other_thing in enumerate(working_clues):
        
        match other_thing:
            case 0, let:
                list_of_words = [i for i in list_of_words if let not in i]
                
            case 1, let:
                list_of_words = [i for i in list_of_words if i[ind] == let]
                
            case 2, let:
                list_of_words = [i for i in list_of_words if let in word and i[ind] != let]
                
    return list_of_words


print('starting')
for outer_ind, my_word in enumerate(word_list):
    print(my_word)
    y = 0
    for columns_ind, clues in enumerate(combis):
        
        working_list = word_list.copy()
        working_list = use_clues(my_word, clues, working_list)
                        
                        
        x = len(working_list)/len(word_list)
        
        if x:
            y += x * log2(1/x)
                
        
        for thingino in working_list:
                # print(outer_ind, row_ind, columns_ind)
                counts[outer_ind, word_locs[thingino], columns_ind] = 1
    print(y)        
        

        
    
# proba besedo:





# dobi stvari, ki so in tiste ki niso:

# nardi okrajšan spisek besed tako da gre čez spisek in gleda če je beseda v setu
# hkrati šteje črke v besedah in gleda na kerih mestih je

# ugotovi kera je najboljša nova beseda




