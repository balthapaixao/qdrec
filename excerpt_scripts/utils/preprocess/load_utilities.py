import pendulum
from sqlalchemy import create_engine

import pandas as pd


def save_to_csv(df: pd.DataFrame,
                output_name: str = "excerpts_cleaned") -> None:
    """
    Salvando o dataframe em um arquivo csv

    Arguments:
        df: pandas DataFrame
        output_name: str

    Returns:
        None

    """
    date = pendulum.datetime.now().strftime("%d%m%Y%H00")
    output_name += date
    with open(f"{output_name}.csv",
              "a+",
              encoding='utf-8') as f:
        df.to_csv(f,
                  index=False,
                  header=False)
    print("DONE!")
    return None
