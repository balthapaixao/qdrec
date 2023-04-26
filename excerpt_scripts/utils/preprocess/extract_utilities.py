import pandas as pd


def read_file(filepath: str) -> pd.DataFrame:
    """
    Read the file and return the text

    Arguments:
        filepath: str

    Returns:
        text: str"""
    df = pd.read_csv(filepath)

    return df
