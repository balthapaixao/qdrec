import numpy as np

from _old.preprocess_qd import pipeline_multiprocess
from .utils.preprocess.extract_utilities import read_file
import sys


def main():
    filepath = sys.argv[1]
    df = read_file(filepath)


if __name__ == '__main__':
    main()
