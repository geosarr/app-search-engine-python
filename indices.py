from dataclasses import dataclass, field
import bisect
from preprocess import simple_preprocessing, inverted_index_preprocessing, character_ngram, clean
from collections import Counter
from tqdm import tqdm


@dataclass
class InvertedIndex:
    index: dict=field(default_factory=dict)  # stores the postings
    raw_freq: dict=field(default_factory=dict) # stores the number of occurrences of tokens in the documents they appear
    documents: dict=field(default_factory=dict) # stores the documents by ID, used when retrieving the relevant documents
    sort_postings : bool=True  # says whether or not the postings are sorted
    char_t_index: dict=field(default_factory=dict) # character to term index 
    t_char_index: dict=field(default_factory=dict) # term to character index
    include_char_index: bool=False # says whether or not to include the (term to) character (to term) index
    ngram: int=2 # the number of characters to consider for the character n-gram index
    
    def index_document(self, document):
        '''
        index the documents with or without sorted posting lists
        '''
        if document.ID not in self.documents:
            self.documents[document.ID] = document
        
        # Character indexing the document
        if self.include_char_index:
            cleaned_doc_terms=clean(document.content.strip()).split()
            for term in cleaned_doc_terms:
                chars=character_ngram(term, self.ngram)
                self.t_char_index[term]= chars
                for char in chars:
                    if char not in self.char_t_index:
                        self.char_t_index[char]=set()
                    self.char_t_index[char].add(term)
                
        # Invert indexing the document   
        terms= inverted_index_preprocessing(document.content)
        for token in set(terms):
            if self.sort_postings:
                if token not in self.index:
                    self.index[token] = list()
                self.index[token].append(document.ID) # works if the documents are indexed iteratively with increasing IDs.
                # bisect.insort(self.index[token], document.ID) # more robust
            else:
                if token not in self.index:
                    self.index[token] = set()
                self.index[token].add(document.ID) 

        self.raw_freq[document.ID]=terms
