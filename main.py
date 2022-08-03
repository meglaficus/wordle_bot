from unicodedata import name
from tqdm import tqdm
import numpy as np
from itertools import combinations_with_replacement
from itertools import permutations
import pickle
from rich.console import Console

# word_dict = {i:set() for i in string.ascii_lowercase}

# with open('allowed.txt') as words:
#     allowed = [i.strip() for i in words.readlines()]

with open('test.txt') as words:
    answers = [i.strip() for i in words.readlines()]

# Possible combinations of hints
with open('combis.pkl', 'rb') as file:
    combis = pickle.load(file)

matrix = np.zeros((len(answers), len(answers), 3 ** 5), dtype='int')

word_locs = {value: i for i, value in enumerate(answers)}


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
                list_of_words = [
                    i for i in list_of_words if let in i if i[ind] != let]
    return list_of_words


def use_clues_multiple(word, clues, list_of_words):
    working_clues = zip(clues, [i for i in word])

    for ind, other_thing in enumerate(working_clues):
        match other_thing:
            case 0, let:
                if word.count(let) > 1:
                    if (1, let) in working_clues or (2, let) in working_clues:
                        continue
                # if word.count(let) > 1 and ((1, let) in working_clues or (1, let) in working_clues):
                #     continue
                else:
                    list_of_words = [i for i in list_of_words if let not in i]

            case 1, let:
                list_of_words = [i for i in list_of_words if i[ind] == let]

            case 2, let:
                list_of_words = [
                    i for i in list_of_words if let in i if i[ind] != let]

    return list_of_words


def find_words(word, words, clues):

    clues = tuple([int(i) for i in clues])

    list_of_words = use_clues(word, clues, words)

    console = Console()

    best = []
    with console.status('[bold blue]Thinking...') as status:
        for my_word in list_of_words:
            y = 0

            for thing in combis:

                list_of_words2 = list_of_words.copy()
                list_of_words3 = use_clues(my_word, thing, list_of_words2)

                if len(list_of_words2):
                    x = len(list_of_words3) / len(list_of_words2)
                else:
                    x = 0

                if x:
                    y += x * np.log2(1 / x)

                # for thingino in list_of_words:
                #     # print(outer_ind, row_ind, columns_ind)
                #     matrix[word_locs[thingino], row_ind, columns_ind] = 1

            best.append((y, my_word))

        # best = sorted(best, reverse=True)
        # print(best[:10])

        # best = []
        # for row in tqdm(range(len(matrix[0]))):
        #     y = 0
        #     for column in range(len(matrix[0, 0])):
        #         if column == row:
        #             continue
        #         x = np.sum(matrix[:, row, column])/len(matrix[:, row, column])
        #         if x:
        #             y += x * np.log2(1/x)

        #     best.append((y, list_of_words[row]))

        best = sorted(best, reverse=True)[0][1]

        return list_of_words, best
    # print(best[:10])


# if __name__ == '__main__':
#     main()
