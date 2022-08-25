import os
import sys
one_level_up=os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(one_level_up)
from search_models import BM25 
from saveload import read_pickle, indexing, to_pickle
from numpy import random as rd
from numpy import mean, log10, Inf
from tqdm import tqdm
import streamlit as st


def get_model(top=100):
    data_dir=os.path.join(one_level_up, "data")
    if os.path.exists(os.path.join(data_dir,"inv.pickle")):
        print("\nLoading the index")
        try:
            index = read_pickle("inv", os.path.join(one_level_up, "data"))
            print("..... OK\n")
        except Exception as e:
            print(f"\nFailed to load the data : {e}")
    else:
        index, _ = indexing(dataset="wiki", save_load_path=data_dir, index_type="inv", nb_docs=int(1e5))
    model=BM25(index=index, top=top)
    return model

def cluster_docs(index, k=1.5, b=0.75, n_centers=500, save=True, save_path=os.path.join(one_level_up, "data")):
    file_path = os.path.join(one_level_up, "data", "doc_clusters_bm25.pickle")
    if not os.path.exists(file_path):
        K=len(index.documents)
        l_avg=mean([len(index.raw_freq[ID]) for ID in index.documents])
        centers = set(rd.randint(1,len(index.documents), n_centers))
        doc_ids = set(index.documents)-set(centers)
        centers_terms={ID: set(index.raw_freq[ID].keys()) for ID in centers}
        clusters={ID: set() for ID in centers}

        for doc_id in tqdm(doc_ids, desc="Document clustering"):
            doc_score, clust=-Inf,0
            doc_terms=set(index.raw_freq[doc_id].keys())
            for c in centers:
                overlap_terms = doc_terms.intersection(set(centers_terms[c]))
                l_doc=len(index.raw_freq[c])
                score = sum({(index.raw_freq[c][term]*(k+1)/(k*(1-b)+index.raw_freq[c][term]+k*l_doc*b/l_avg)) * \
                            log10(0.5*K/len(index.index[term]))
                            for term in overlap_terms})
                if score>=doc_score:
                    clust=c
                    doc_score=score
            if clust==0:
                clusters[rd.choice(list(centers))].add(doc_id)
            else:
                clusters[clust].add(doc_id)
        
        if save:
            to_pickle(clusters, "doc_clusters_bm25", save_path)

    else:
        clusters = read_pickle("doc_clusters_bm25", os.path.join(one_level_up, "data"))
    return clusters

                

	
def design_output(text_results, words_to_highlight):
    if len(text_results)==0:
        return '''<div>No result found</div>'''
    words_to_highlight=list(map(lambda x: x.lower().strip(), words_to_highlight))
    template= '''<div> <br>'''
    for pos, (text, url, title) in enumerate(text_results):
        template+=f'''<a href={url}>{url if len(url)<=100 else url[:100]+ '...'}</a><br>'''
        for w in text.split():
            if w.lower().strip() in words_to_highlight:
                template+=f''' <b>{w}</b>'''
            else:
                template+=f''' {w}'''
        template+='''<br><br>'''
    template+=''' </div>'''
    return template

def empty_result():
    return '''<div>'''



with st.sidebar:
    with st.spinner("Loading the index ..."):
        model=get_model(top=100)
        clusters=cluster_docs(index=model.index)
    st.success("Index loaded!")
