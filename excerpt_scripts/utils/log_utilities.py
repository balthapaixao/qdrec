import logging

# set logs
import datetime
import functools
import logging
import os
import time

from .file_utilities import get_path

path = get_path()

date = datetime.datetime.now().strftime("%Y%m%d%H%M")


LOGGING_FORMAT = os.environ.get(
    'LOGGING_FORMAT', '[%(asctime)s][%(pathname)s:%(lineno)d][%(levelname)s] - %(message)s')
LOGGING_LEVEL = os.environ.get('LOGGING_LEVEL', 'INFO')
LOGGING_DATE_FORMAT = os.environ.get(
    'LOGGING_DATE_FORMAT', '%Y-%m-%d %H:%M:%S')
LOGGING_FILE = os.environ.get(
    'LOGGING_FILE', f'{path}/logs/script-cleaning-{date}.log')
LOCAL_SAVE_FOLDER = os.environ.get('LOCAL_SAVE_FOLDER', './tmp')
# Import Here Environment Variables


def set_basic_logs():
    """
    set basic logs
    :return: None
    """
    logging.basicConfig(filename=f'{LOGGING_FILE}',
                        level=logging.INFO,
                        format=LOGGING_FORMAT)


set_basic_logs()

logger = logging.getLogger(__name__)


def log_execution(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"Executing {func.__name__}")
        result = func(*args, **kwargs)
        logger.info(f"Finished executing {func.__name__}")
        return result
    return wrapper


def timing_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logger.info(
            f"Function {func.__name__} took {end_time - start_time} seconds to run.")
        return result
    return wrapper
