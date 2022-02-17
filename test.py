import joblib

with open('step1_0.1.pkl', 'rb') as f:
    words = joblib.load(f)

for score, word in enumerate(words):
    if word == 'crane':
        print(int, score)
        
print(words[:10])