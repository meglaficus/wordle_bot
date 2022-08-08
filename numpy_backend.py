
def use_clues2(word, clues, list_of_words, matrix, column_ind):
    working_clues = [i for i in zip(clues, [i for i in word])]

    for ind, other_thing in enumerate(working_clues):
        hint, let = other_thing

        for word_ind, second_word in enumerate(list_of_words):

            if word.count(let) > 1 and hint in (0, 2):
                letter_count = 0
                for clue, letter in working_clues:
                    if clue in (1, 2) and letter == let:
                        letter_count += 1

                if hint == 0:
                    for clue, letter in working_clues[ind + 1:]:
                        if clue == 2 and letter == let:
                            matrix[:, column_ind] = 0
                            return

                    if second_word.count(let) != letter_count or second_word[ind] == let:
                        matrix[word_ind, column_ind] = 0

                if hint == 2:
                    if letter_count and second_word.count(let) < letter_count:
                        matrix[word_ind, column_ind] = 0

                    illegal_locs = []
                    for ind, (clue, letter) in enumerate(working_clues):
                        if letter == let:
                            illegal_locs.append(ind)

                    if let in second_word and any(second_word[j] == let for j in illegal_locs):
                        matrix[word_ind, column_ind] = 0

            else:
                match other_thing:
                    case 0, let:
                        if let in second_word:
                            matrix[word_ind, column_ind] = 0

                    case 1, let:
                        if second_word[ind] != let:
                            matrix[word_ind, column_ind] = 0

                    case 2, let:
                        if let not in second_word or second_word[ind] == let:
                            matrix[word_ind, column_ind] = 0


def use_clues3(word, clues, list_of_words, matrix, column_ind):
    working_clues = [i for i in zip(clues, [i for i in word])]

    duplicates_strict = {}
    duplicates_lax = {}
    checked = set()
    illegal_locs = {}
    for ind, (hint, let) in enumerate(working_clues):
        if let in checked:
            continue

        if word.count(let) > 1 and hint in (0, 2):
            letter_count = 0
            for clue, letter in working_clues:
                if clue in (1, 2) and letter == let:
                    letter_count += 1

            if hint == 0:
                for clue, letter in working_clues[ind + 1:]:
                    if clue == 2 and letter == let:
                        matrix[:, column_ind] = 0
                        return

                if letter_count:
                    duplicates_strict[let] = letter_count
                    checked.add(let)

            if hint == 2:
                illegal_locs_local = []
                for ind, (clue, letter) in enumerate(working_clues):
                    if letter == let:
                        illegal_locs_local.append(ind)
                illegal_locs[let] = illegal_locs_local

                duplicates_lax[let] = letter_count

    for word_ind, second_word in enumerate(list_of_words):

        for ind, (hint, let) in enumerate(working_clues):

            if word.count(let) > 1 and hint in (0, 2):
                if hint == 0:
                    if (let in duplicates_strict and duplicates_strict[let] != second_word.count(let)) or second_word[ind] == let:
                        matrix[word_ind, column_ind] = 0
                        break

                if hint == 2:
                    if (let in duplicates_lax and duplicates_lax[let] < second_word.count(let)):
                        matrix[word_ind, column_ind] = 0
                        break

                    if let in second_word and second_word in illegal_locs and any(second_word[j] == let for j in illegal_locs[second_word]):
                        matrix[word_ind, column_ind] = 0
                        break

            else:
                match (hint, let):
                    case 0, let:
                        if let in second_word:
                            matrix[word_ind, column_ind] = 0
                            break

                    case 1, let:
                        if second_word[ind] != let:
                            matrix[word_ind, column_ind] = 0
                            break

                    case 2, let:
                        if let not in second_word or second_word[ind] == let:
                            matrix[word_ind, column_ind] = 0
                            break


def new_test_it():
    with open('test1.txt', 'r') as f:
        list_of_words = [i.strip() for i in f.readlines()]

    result = []
    for my_word in tqdm(list_of_words):
        matrix = np.ones((len(list_of_words), len(combis)))
        for combi_ind, thing in enumerate(combis):
            use_clues3(my_word, thing, list_of_words, matrix, combi_ind)
            sums = np.sum(matrix, axis=0)
            sums = sums / len(list_of_words)
            y = np.sum([(i * np.log2(1 / i)) if i != 0 else 0 for i in sums])

        result.append((y, my_word))

    print(sorted(result, reverse=True)[:10])
