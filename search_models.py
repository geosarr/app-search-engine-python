from dataclasses import dataclass, field
from indices import InvertedIndex
from typing import Union
from preprocess import inverted_index_preprocessing
from model_utils import rank_documents
from numpy import log10, mean
# from tqdm import tqdm




@dataclass
class Arguments:
    index: InvertedIndex = InvertedIndex() 
    top: int=5
    correct_query: bool=False 
    args: dict=field(default_factory=dict)


@dataclass
class BM25(Arguments):
    k: Union[float, int]=1.5
    b: Union[float, int]=0.75


    def retrieval(self, query, clusters):
        '''
        Using binary independence extensions model to rank the documents, accounting for the term frequencies, document
        lengths. bm25 is known to be the best among the three extensions: bm25 (when k!=0 and b!=0), bm11 (when b=1 and k!=0), 
        two poisson (when b=0 and k!=0)
        '''
        if type(self.index)!=InvertedIndex:
            raise TypeError ("bim_ext only support an InvertedIndex type")

        # if self.correct_query:
        #     query_correction(query, self.index)

        doc_scores={ID: 0 for ID in self.index.documents}
        preprocessed_query=inverted_index_preprocessing(query)
        K=len(self.index.documents)
        l_avg=mean([len(self.index.raw_freq[ID]) for ID in self.index.documents])
        clusters_score={ID: 0 for ID in clusters}
        for term in preprocessed_query:
            if term in self.index.index:
                doc_ids=set(self.index.index[term]).intersection(set(clusters.keys()))
                for doc_id in doc_ids:
                    freq=self.index.raw_freq[doc_id][term]
                    l_doc=len(self.index.raw_freq[doc_id])
                    adjustment=freq*(self.k+1)/(self.k*(1-self.b)+freq+self.k*l_doc*self.b/l_avg)
                    clusters_score[doc_id]+=adjustment*log10(0.5*K/len(doc_ids))

        top_cluster=rank_documents(clusters_score, self.top)

        if len(top_cluster)==0:
            return []

        else:
            top_cluster=top_cluster[0][0]
            for term in preprocessed_query:
                if term in self.index.index:
                    doc_ids=set(self.index.index[term]).intersection(clusters[top_cluster])
                    for doc_id in doc_ids:
                        freq=self.index.raw_freq[doc_id][term]
                        l_doc=len(self.index.raw_freq[doc_id])
                        adjustment=freq*(self.k+1)/(self.k*(1-self.b)+freq+self.k*l_doc*self.b/l_avg)
                        doc_scores[doc_id]+=adjustment*log10(0.5*K/len(doc_ids))
        
        return rank_documents(doc_scores, self.top)
