with open('all_words.txt', 'r', encoding='utf-8') as f:
    words = []
    for i in f.readlines():
        words.append(i.strip())

pairs = [i.split(' ') for i in words]

# to be completed...
