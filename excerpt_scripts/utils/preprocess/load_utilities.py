import pendulum
from .clean_text_utilities import clean_text, read_dicionario_br, find_dashes_and_replace_words
import logging


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


def clean(texts: pd.Series) -> pd.Series:
    return texts.apply(lambda txt: clean_text(txt))


def clean_and_insert(df_splitted: pd.DataFrame()) -> None:
    engine = create_engine(f"sqlite:///queridodiario.db")
    for index, row in df_splitted.iterrows():

        row['cleaned_text'] = clean_text(row['cleaned_text'])

        row.to_sql("excerpts",
                   engine,
                   schema=None,
                   if_exists='replace',
                   index=False,
                   index_label=False)

# dev
    # df_splitted['cleaned_text'] = df_splitted['cleaned_text'].apply(lambda row: clean_text(row))
    # df_splitted.to_sql("excerpts",
    #                     engine,
    #                     schema=None,
    #                     if_exists='replace',
    #                     index=False,
    #                     index_label=False)
    # insert into sqlite

    # return texts.apply(lambda txt: clean_text(txt))


def pipeline_multiprocess_db(df: pd.DataFrame) -> pd.DataFrame:
    date = pendulum.datetime.now().strftime("%d%m%Y%H:%M")

    df_unique_texts = deepcopy(df.drop_duplicates(subset=['excerpt']))
    df_unique_texts = df_unique_texts[[
        'excerptId', 'excerpt', 'state', 'city', 'source_date']]
    # falta vetorização

    logging.basicConfig(filename=f'QD-scrap_google-{date}.log',
                        level=logging.INFO)

    df_ptbr = read_dicionario_br()

    df_unique_texts['cleaned_text'] = df_unique_texts['excerpt'].map(
        preprocess)
    df_unique_texts['cleaned_text'] = df_unique_texts['cleaned_text'].apply(lambda txt:
                                                                            find_dashes_and_replace_words(txt,
                                                                                                          df_ptbr))

    clean_and_insert(df_unique_texts)

    return df_unique_texts
