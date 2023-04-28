# @title Setup common imports and functions
from itertools import islice
import numpy as np
import pandas as pd
import nltk
from IPython.display import HTML, display
from tqdm.notebook import tqdm

from copy import deepcopy

import tensorflow.compat.v2 as tf
import tensorflow_hub as hub
from tensorflow_text import SentencepieceTokenizer


nltk.download('punkt')

# "https://tfhub.dev/google/universal-sentence-encoder/4" #@param ["https://tfhub.dev/google/universal-sentence-encoder/4", "https://tfhub.dev/google/universal-sentence-encoder-large/5"]
module_url = "https://tfhub.dev/google/universal-sentence-encoder-multilingual/3"
model = hub.load(module_url)
print(f"module {module_url} loaded")


def embed(input):
    return model(input)


def get_k_elements(n: int, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))


# pd.read_csv("./de-para-total-20221108.csv")
df_messages = pd.read_csv("./dataset_processado_20221109.csv")
df_messages.head(1)

messages = df_messages['processado'].dropna().tolist()
len(messages)


def get_recommendations(message_input: str,
                        messages: list,
                        k: int = 5) -> dict:
    aux_messages = deepcopy(messages)
    aux_messages.append(message_input)

    message_embeddings = embed(aux_messages)

    corr = np.inner(message_embeddings,
                    message_embeddings)

    positions_to_recommend = {i: val for i, val in enumerate(corr[-1])}

    positions_to_recommend = dict(sorted(positions_to_recommend.items(),
                                         key=lambda item: item[1],
                                         reverse=True))

    message_input_index = max(positions_to_recommend.keys())
    del positions_to_recommend[message_input_index]

    positions_to_recommend = get_k_elements(k, positions_to_recommend.items())

    dict_recomendations = {i+1: {"score": f"{elem[1]}",
                                 "text": f"{aux_messages[elem[0]]}"} for i, elem in enumerate(positions_to_recommend)}

    return dict_recomendations


if __name__ == '__main__':
    message_inputs = ["Perigo do coronavirus nas cidades brasileiras",
                      "aumento na tarifa de energia elétrica",
                      "crime federal",
                      "desmatamento na Amazônia",
                      "covid 19",
                      "meio ambiente",
                      "escolas criadas",
                      "compras de computadores",
                      "internet nas escolas",
                      "merenda escolar"]

    for msg in message_inputs:
        print(msg.upper())
        recs = get_recommendations(message_input=msg,
                                   messages=messages,
                                   k=3)

        for r in recs.values():
            print(r)
            print()

        print()
        print()
