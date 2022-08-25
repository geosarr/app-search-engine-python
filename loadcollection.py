from collection import Document
# import re
# from datasets import load_dataset
from tqdm import tqdm
import os
import gzip
from lxml import etree
import random as rd

# Taken and adapted from https://github.com/bartdegoede/python-searchengine/blob/master/load.py
def load_collection_wiki_abstract(nb_docs=int(1e6), judgments=None, version=None, split=None):
    file_path=os.path.abspath(os.path.dirname(__file__))
    gzip_file_path=os.path.join(file_path, 'data/wiki-abstract.xml.gz')
    if not os.path.exists(gzip_file_path):
        os.popen(f"wget https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-abstract.xml.gz -O {gzip_file_path}").read()
    print("\nData download ... OK")
    print("\nStart indexing")
    with gzip.open(gzip_file_path, 'rb') as f:
        doc_id = 0
        with tqdm(total=nb_docs, desc="Indexation ") as pbar:
            for _, element in etree.iterparse(f, events=('end',), tag='doc'):
                if doc_id>nb_docs: break
                title = element.findtext('./title')
                url = element.findtext('./url')
                abstract = element.findtext('./abstract')
                if len(abstract.split())>=10 and rd.randint(0,2) in {0,1}:
                    yield Document(ID=doc_id+1, content=abstract, url=url, title=title)
                    doc_id += 1
                    pbar.update(1)
                element.clear()
