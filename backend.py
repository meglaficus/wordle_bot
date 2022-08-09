from tqdm import tqdm
import numpy as np
import pickle as pkl
from rich.console import Console


def use_clues(word, clues, list_of_words):
    working_clues = [i for i in zip(clues, [i for i in word])]

    for ind, other_thing in enumerate(working_clues):
        hint, let = other_thing

        if word.count(let) > 1 and hint in (0, 2):
            letter_count = 0
            for clue, letter in working_clues:
                if clue in (1, 2) and letter == let:
                    letter_count += 1

            if hint == 0:
                for clue, letter in working_clues[ind + 1:]:
                    if clue == 2 and letter == let:
                        return []

                list_of_words = [
                    i for i in list_of_words if i.count(let) == letter_count]

                list_of_words = [i for i in list_of_words if i[ind] != let]

            if hint == 2:
                if letter_count:
                    list_of_words = [
                        i for i in list_of_words if i.count(let) >= letter_count]

                illegal_locs = []
                for ind, (clue, letter) in enumerate(working_clues):
                    if letter == let:
                        illegal_locs.append(ind)

                list_of_words = [i for i in list_of_words if (
                    let in i and all(i[j] != let for j in illegal_locs))]

        else:
            match other_thing:
                case 0, let:
                    list_of_words = [i for i in list_of_words if let not in i]

                case 1, let:
                    list_of_words = [i for i in list_of_words if i[ind] == let]

                case 2, let:
                    list_of_words = [
                        i for i in list_of_words if (let in i and i[ind] != let)]

    return list_of_words


def find_words(word, words, clues):
    console = Console()

    # Possible combinations of hints
    with open('data/combis.pkl', 'rb') as file:
        combis = pkl.load(file)

    clues = tuple([int(i) for i in clues])

    list_of_words = use_clues(word, clues, words)
    print(f'{len(list_of_words)} words left')
    result = []
    with console.status('[bold blue]Thinking...') as status:
        for my_word in list_of_words:
            y = 0

            for thing in combis:
                list_of_words2 = use_clues(
                    my_word, thing, list_of_words)

                x = len(list_of_words2) / len(list_of_words)
                if x:
                    y += x * np.log2(1 / x)

            result.append((y, my_word))

        best_score = 0
        best_word = result[0][1]
        for score, word in result:
            if score > best_score:
                score = best_score
                best_word = word

        return list_of_words, best_word


if __name__ == '__main__':
    with open('data/combis.pkl', 'rb') as file:
        combis = pkl.load(file)

    with open('data/answers.txt', 'r') as f:
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

        print(sorted(result, reverse=True)[:5])
