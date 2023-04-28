from .clean_text_utilities import (remove_special_characters, remove_dash_n,
                                   remove_lots_of_points, remove_bad_chars,
                                   spaced_letters, dots_that_mess_segmentation,
                                   remove_spaces, join_words, separate_words,
                                   remove_page_breaker, remove_multiple_dashes,
                                   clean_text, find_dashes_and_replace_words,
                                   read_dicionario_br)
from multiprocessing import cpu_count, Pool
import numpy as np
import pandas as pd
from ..log_utilities import log_execution, timing_decorator


@timing_decorator
@log_execution
def preprocess_text(text: str) -> str:
    """Preprocess text.
    Args:
        text: a string
    Returns:
        a string
    """

    text = remove_special_characters(text)
    text = remove_dash_n(text)
    text = remove_lots_of_points(text)
    text = remove_bad_chars(text)
    text = spaced_letters(text)
    text = dots_that_mess_segmentation(text)
    text = remove_spaces(text)
    text = join_words(text)
    text = separate_words(text)
    text = remove_page_breaker(text)
    text = remove_special_characters(text)
    text = remove_multiple_dashes(text)

    text = clean_text(text)

    return text


def posprocess_text(text: str) -> str:
    """Posprocess text.
    Args:
        text: a string
    Returns:
        a string
    """
    df_ptbr = read_dicionario_br()

    text = find_dashes_and_replace_words(text,
                                         df_ptbr)

    return text


def transform_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Transform a dataframe.
    Args:
        df: a pandas DataFrame
    Returns:
        a pandas DataFrame
    """

    df['cleaned_text'] = df['excerpt'].map(preprocess_text)
    df['cleaned_text'] = df['cleaned_text'].apply(posprocess_text)

    return df


def paralelize_transform(df: pd.DataFrame,
                         n_jobs: int = cpu_count()) -> pd.DataFrame:
    """
    Multiprocess a function that takes a DataFrame as input
    :param df: DataFrame
    :param func: function
    :param n_jobs: number of processes
    :return: DataFrame
    """
    df_split = np.array_split(df, n_jobs - 1)
    with Pool(n_jobs) as pool:
        df = pd.concat(pool.map(transform_dataframe,
                                df_split))

    return df
