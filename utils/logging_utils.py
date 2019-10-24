import logging
import os
from logging.handlers import RotatingFileHandler


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    if 'LOG_FILE' in os.environ:
        fh = RotatingFileHandler(os.environ.get('LOG_FILE'), maxBytes=10**7)
        fh.setLevel(logging.DEBUG)

        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger