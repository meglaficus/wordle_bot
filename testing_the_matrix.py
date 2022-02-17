import joblib
import numpy as np
from math import log2
from tqdm import tqdm

with open('the_matrix.pkl', 'rb') as file:
    matrix = joblib.load(file)

with open('allowed.txt') as words:
    allowed = [i.strip() for i in words.readlines()]

print('imported')

best = []
for row in tqdm(range(len(matrix[0]))):
    y = 0
    for column in range(len(matrix[0,0])):
        if column == row:
            continue
        x = np.sum(matrix[:, row, column])/len(matrix[:, row, column])
        if x:
            y += x * log2(1/x)
            
    best.append((y, allowed[row]))

best = sorted(best, reverse=True)
print(best)

with open('step1_0.1.pkl', 'wb') as f:
    joblib.dump(best, f)