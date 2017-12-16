# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 15:05:20 2017

@author: Divyansh Shukla
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 21:29:12 2017

@author: Divyansh Shukla
"""
import newspaper
from newspaper import Article
import nltk
import re
from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
from string import punctuation
from heapq import nlargest

#toi_paper = newspaper.build('http://timesofindia.indiatimes.com/') 



class Summarize_Frequency:
    def __init__(self, cut_min=0.1, cut_max=0.8):
        """
        Initilize the text summarizer.
        Words that have a frequency term lower than cut_min
        or higer than cut_max will be ignored.
        """
        self._cut_min = cut_min
        self._cut_max = cut_max
        self._stopwords = set(stopwords.words('english') +
        list(punctuation))
        
    
    
    def _compute_frequencies(self, word_sent):
        """
        Compute the frequency of each of word.
        Input:
        word_sent, a list of sentences already tokenized.
        Output:
        freq, a dictionary where freq[w] is the frequency of w.
        """
        freq = defaultdict(int)
        for s in word_sent:
            for word in s:
                if word not in self._stopwords:
                    freq[word] += 1
        m = float(max(freq.values()))
        a = {}
        for w,i in freq.items():
            freq[w] = freq[w]/m
            if freq[w] < self._cut_max and freq[w] > self._cut_min:
                a[w] = i/m
        return a
    
    def summarize(self, text, n):
        """
        list of (n) sentences are returned.
        summary of text is returned.
        """
        
        #print("hi")
        sents = sent_tokenize(text)
        assert n <= len(sents)
        
        word_sent = [word_tokenize(s.lower()) for s in sents]
        self._freq = self._compute_frequencies(word_sent)
        ranking = defaultdict(int)
        for i,sent in enumerate(word_sent):
            for w in sent:
                if w in self._freq:
                    ranking[i] += self._freq[w]
        sents_idx = self._rank(ranking, n)
        return [sents[j] for j in sents_idx]
    
    def _rank(self, ranking, n):
        """ return the first n sentences with highest ranking """
        return nlargest(n, ranking, key=ranking.get)
    
    
if __name__ == "__main__":
    '''url = 'https://timesofindia.indiatimes.com/business/india-business/fuel-to-get-cheaper-as-gujarat-maharashtra-cut-vat-on-petrol-and-diesel/articleshow/61020344.cms'
    article = Article(url)
    article.download()
    article.parse()
    
    
    news_content = article.text
    '''
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
            return float(numerator+60) / denominator
    
    def text_to_vector(text): 
        words = text.split() 
        return Counter(words)
    
   
    
    
    
    ob = Summarize_Frequency()
    '''f = open("test1.txt", "r")
    file = f.read()
    print(file)
    summ = ob.summarize(file,4)
    print(summ)
    f = open("test_sum1.txt", "r")
    f_summ = f.read()
    summ=str(summ)
    print(f_summ)'''
    import csv
    su = 0
    c = 0
    l = 0
    with open('news_summary.csv') as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        for row in csvReader:
            
            f_summ = str(row[4])
            file = str(row[5])
            summ = ob.summarize(file,2)
            summ = str(summ)
            l +=1
            
            vector1 = text_to_vector(summ) 
            vector2 = text_to_vector(f_summ) 
            cosine = get_cosine(vector1, vector2)
            if (cosine <1):
                c+=1
                print(summ)
                print()
                print()
                print(f_summ)
                print("Current article's similarity:: ",cosine)
                su = cosine+su
                print()
                print()
                if (l>=221):
                    break
        print("Average:: ",(su/c))
    