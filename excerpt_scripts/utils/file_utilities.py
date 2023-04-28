import os


def get_path() -> str:
    """
    Get the path of the current file

    Arguments:
        None

    Returns:
        path: str"""

    try:
        path = os.path.dirname(os.path.realpath(__file__))

    except:
        path = os.path.dirname(os.path.realpath('__file__'))

    return path
