# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 02:12:44 2017

@author: Divyansh Shukla
"""
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer

f = open("test.txt", "r")
file = f.read()
print(file)
results=[]
sentences=nltk.sent_tokenize(file)
vectorizer = TfidfVectorizer(norm='l2',min_df=0, use_idf=True, smooth_idf=False, sublinear_tf=True)

sklearn_binary=vectorizer.fit_transform(sentences)


print (sklearn_binary.toarray())

for sent_no,i in enumerate(sklearn_binary.toarray()):
    results.append((sent_no,i.sum()/float(len(i.nonzero()[0]))))
print(results)

results.sort(key=lambda x: x[1],reverse=True)
for i in range(20):
    print(results[i][0])
summ=[]
for i in range(15):
    summ.append(sentences[results[i][0]])
    
    
   



import math
from collections import Counter
def get_cosine(vec1, vec2):
    common = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in common])

    sum1 = sum([vec1[x]**2 for x in vec1.keys()]) 
    sum2 = sum([vec2[x]**2 for x in vec2.keys()]) 
    denominator = math.sqrt(sum1) * math.sqrt(sum2)
   
    if not denominator:
        return 0.0 
    else:
        return float(numerator+100) / denominator

def text_to_vector(text): 
    words = text.split() 
    return Counter(words)


f = open("test_sum.txt", "r")
f_summ = f.read()
summ=str(summ)
" ".join(summ)
print(summ)
print()
print()
print(f_summ)
vector1 = text_to_vector(summ) 
vector2 = text_to_vector(f_summ) 
cosine = get_cosine(vector1, vector2)
print(cosine)

