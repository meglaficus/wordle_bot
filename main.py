from tqdm import tqdm
import numpy as np
import joblib
from itertools import combinations_with_replacement
from itertools import permutations
import pickle
from math import log2

# word_dict = {i:set() for i in string.ascii_lowercase}

with open('allowed.txt') as words:
    allowed = [i.strip() for i in words.readlines()]

with open('answers.txt') as words:
    answers = [i.strip() for i in words.readlines()]

with open('combis.pkl', 'rb') as file:
    combis = pickle.load(file)

counts = np.zeros((len(answers), len(allowed), 3 ** 5), dtype='int')

word_locs = {value: i for i, value in enumerate(answers)}
print(word_locs)


def use_clues(word, clues, list_of_words):
    working_clues = zip(clues, [i for i in word])

    for ind, other_thing in enumerate(working_clues):
        match other_thing:
            case 0, let:
                # if word.count(let) > 1 and ((1, let) in working_clues or (1, let) in working_clues):
                #     continue  
                list_of_words = [i for i in list_of_words if let not in i]

            case 1, let:
                list_of_words = [i for i in list_of_words if i[ind] == let]

            case 2, let:
                list_of_words = [i for i in list_of_words if let in i if i[ind] != let]

    return list_of_words


def use_clues_multiple(word, clues, list_of_words):
    working_clues = zip(clues, [i for i in word])

    for ind, other_thing in enumerate(working_clues):
        match other_thing:
            case 0, let:
                # if word.count(let) > 1 and ((1, let) in working_clues or (1, let) in working_clues):
                #     continue
                list_of_words = [i for i in list_of_words if let not in i]

            case 1, let:
                list_of_words = [i for i in list_of_words if i[ind] == let]

            case 2, let:
                list_of_words = [i for i in list_of_words if let in i if i[ind] != let]

    return list_of_words
    pass


for row_ind, my_word in enumerate(tqdm(allowed)):
    y = 0
    for columns_ind, thing in enumerate(combis):

        list_of_words = answers.copy()
        working_clues = zip(thing, [i for i in my_word])

        list_of_words = use_clues(my_word, thing, list_of_words)

        x = len(list_of_words) / len(answers)

        if x:
            y += x * log2(1 / x)

        for thingino in list_of_words:
            # print(outer_ind, row_ind, columns_ind)
            counts[word_locs[thingino], row_ind, columns_ind] = 1

with open('the_matrix.pkl', 'wb') as f:
    joblib.dump(counts, f)
