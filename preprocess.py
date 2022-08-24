import string
import re
from nltk.stem import PorterStemmer
import nltk
nltk.download("words")
nltk.download('stopwords')
from nltk.corpus import stopwords

from collections import Counter

def clean(text):     
    punctuations= ''.join(string.punctuation)         
    preproc_text=text.lower().replace('\n', " ").replace("\t", " ").translate(str.maketrans(' ', ' ', punctuations))

    # dropping multiple whitespaces
    preproc_text=re.sub(' +', ' ', preproc_text)
        
    return preproc_text

def simple_preprocessing(text):
    '''
    Simpler version of preprocessing
    with this version indexing is much faster, i.e the stemming part is time consuming -> Is it worth doing it ?
    It depends on the result of the search engine.
    '''
    return clean(text).split()


def inverted_index_preprocessing(text):
    '''
    Preprocessing the documents for inverted indexing purpose.
    '''
    preproc_text=clean(text)
    count=Counter(preproc_text.split())
    tokens=set(count)-set(stopwords.words('english'))
    stem={(PorterStemmer().stem(token), token) for token in tokens}
    return {term: count[token] for term ,token in stem}
    


def character_ngram(word,n=2):
    '''
    Returning the character n-grams of word
    '''
    w=word.strip()
    if n>=len(w):
        return {w}
    return {w[i:i+n] for i in range(len(w)-n+1)}