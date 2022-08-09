singlets = []

with open(r'data/allowed.txt', 'r') as f:
    for word in f.readlines():
        word = word.strip()
        if all(word.count(i) == 1 for i in word):
            singlets.append(word)

with open(r'data\all_singles.txt', 'w') as f:
    for i in singlets:
        f.write(i + '\n')
