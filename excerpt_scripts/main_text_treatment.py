import sys

from utils.preprocess.extract_utilities import read_file
from utils.preprocess.transform_utilities import paralelize_transform
from utils.preprocess.load_utilities import save_to_csv
from utils.log_utilities import timing_decorator


@timing_decorator
def main():
    filepath = sys.argv[1]
    print(f'Processing {filepath}...')
    df = read_file(filepath)

    df = paralelize_transform(df)

    save_to_csv(df)


if __name__ == '__main__':
    main()
