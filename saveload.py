import pickle
from collection import index_collection
from loadcollection import load_collection_wiki_abstract 
from indices import InvertedIndex
import pickle
import os
from config import * 

def to_pickle(obj, name, path='./data'):
    '''
    Saving an object to pickle
    '''
    with open(path+'/'+name+'.pickle', 'wb') as outp:
        pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)
        

        
def read_pickle(name, path='./data'):
    '''
    Loading a pickle object
    '''
    with open(path+'/'+name+'.pickle', 'rb') as inp:
        return pickle.load(inp)


def indexing(dataset="wiki", save_load_path="./data", index_type="inv", nb_docs=int(1e6), judgments=None, version=None, split=None):
    data={#"ms_marco": load_collection_ms_marco, 
          "wiki": load_collection_wiki_abstract}
    idx={"inv": InvertedIndex}

    if index_type not in INDEX_TYPES:
        raise ValueError (f"The function supports only values {INDEX_TYPES} for index_type")

    elif dataset not in DATA:
        raise ValueError (f"The only supported values for argument dataset are {DATA}")

    elif dataset!="ms_marco" and (version is not None or split is not None):
        raise ValueError ("Set the arguments split and version to None if dataset='ms_marco' is not used")

    print("\n")
    print(" Collection indexation in progress ".center(50, "#"))
    index, judgments=index_collection(data[dataset](nb_docs=nb_docs, judgments=judgments, version=version, split=split), \
                                     idx[index_type](include_char_index=True, ngram=3))

    file_path=os.path.abspath(os.path.dirname(__file__))
    if not os.path.exists(os.path.join(file_path, f"./data/{index_type}.pickle")):
        try:
            to_pickle(index, index_type, save_load_path)
            print("\nSuccessfully saved the index")
        except Exception as e:
            print(f"\nFailed to save the index : {e}")
    else:
        print("\nLoading the data")
        try:
            index=read_pickle(index_type, save_load_path)
        except Exception as e:
            print(f"\nFailed to load the data : {e}")
    
    return index, judgments
