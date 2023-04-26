import pendulum
from sqlalchemy import create_engine
from .clean_text_utilities import (clean_text, read_dicionario_br,
                                   find_dashes_and_replace_words)
from .transform_utilities import preprocess
import logging

import pandas as pd

from copy import deepcopy


def clean_and_save(text_list: list,
                   output_name: str = "excerpts_cleaned") -> None:
    date = pendulum.datetime.now().strftime("%d%m%Y%H00")
    output_name += date
    with open(f"{output_name}.csv",
              "a+",
              encoding='utf-8') as f:
        for text in text_list:
            new_text = clean_text(text)
            f.write(f'{text}\t{new_text}\n')
    print("DONE!")


def pipeline(df_path: str) -> None:
    date = pendulum.datetime.now().strftime("%d%m%Y%H00")

    logging.basicConfig(filename=f'QD-scrap_google-{date}.log',
                        level=logging.INFO)
    df = pd.read_csv(df_path)

    df_ptbr = read_dicionario_br()

    df['cleaned_text'] = df['excerpt'].map(preprocess)
    df['cleaned_text'] = df['cleaned_text'].apply(lambda txt:
                                                  find_dashes_and_replace_words(txt,
                                                                                df_ptbr)
                                                  )

    unique_text_list = df['cleaned_text'].unique()

    clean_and_save(unique_text_list)


def pipeline_multiprocess(df: pd.DataFrame) -> None:
    date = pendulum.datetime.now().strftime("%d%m%Y%H:%M")

    df_unique_texts = deepcopy(df.drop_duplicates(subset=['excerpt']))

    logging.basicConfig(filename=f'QD-scrap_google-{date}.log',
                        level=logging.INFO)

    df_ptbr = read_dicionario_br()

    df_unique_texts['cleaned_text'] = df_unique_texts['excerpt'].map(
        preprocess)
    df_unique_texts['cleaned_text'] = df_unique_texts['cleaned_text'].apply(lambda txt:
                                                                            find_dashes_and_replace_words(txt,
                                                                                                          df_ptbr))

    unique_text_list = df_unique_texts['cleaned_text'].unique()

    clean_and_save(unique_text_list)

    return df_unique_texts
