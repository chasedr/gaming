import nltk
from nltk.corpus import wordnet

#nltk.download('averaged_perceptron_tagger')

words = []
with open('The_Oxford_3000_with_only_CEFR.txt', 'r') as f:
    for line in f:
        parts = line.split() 
        word = parts[0]
        words.append(word)

tagged_words = nltk.pos_tag(words)
'''
with open('output.txt', 'w') as f:
    for word, tag in tagged_words:
        f.write(f'{word} {tag}\n')
'''

import random
import time

nouns = []  
verbs = []

for word, tag in tagged_words:
    if tag == 'NN':
        nouns.append(word)
    elif tag == 'VB': 
        verbs.append(word)

while True:
    n1 = random.choice(nouns)  
    v = random.choice(verbs)
    n2 = random.choice(nouns)
    
    sentence = f"{n1} {v} {n2}"
    print(sentence)
    time.sleep(1)

#for word, tag in tagged_words:
#    print(f'{word} {tag}')
