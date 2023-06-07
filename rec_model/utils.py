#@title Setup common imports and functions
import numpy as np
import os
import pandas as pd 
import json
import nltk
import os
import pprint
import random
import simpleneighbors
import urllib
import re
import seaborn as sns
from copy import deepcopy

import tensorflow.compat.v2 as tf
import tensorflow_hub as hub
from tensorflow_text import SentencepieceTokenizer
from itertools import islice

nltk.download('punkt')

def load_model():
    module_url = "https://tfhub.dev/google/universal-sentence-encoder-multilingual/3"#"https://tfhub.dev/google/universal-sentence-encoder/4" #@param ["https://tfhub.dev/google/universal-sentence-encoder/4", "https://tfhub.dev/google/universal-sentence-encoder-large/5"]
    model = hub.load(module_url)
    print (f"module {module_url} loaded")

    return model
    
def embed_term(term:str):
    model=load_model()

    return model(term)

def get_k_elements(n:int, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))

def find_recommendations(term:str, 
                         excerpts:dict,
                         k:int=100):
    
    df = pd.DataFrame(excerpts)

    embed_term = embed_term(term)

    excerpt_vectors = df['excerpt_vectors'].to_list()
    excerpt_vectors.append(embed_term)

    corr = np.inner(excerpt_vectors, 
                    excerpt_vectors)

    positions_to_recommend = {i:val for i, val in enumerate(corr[-1])}

    #criar df com os valores de correlação
    # ordenar df por correlação
    # retornar os k primeiros valores